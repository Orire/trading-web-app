"""
Strategy bot orchestrator with continuous improvement loop (paper mode by default).
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models.schemas import SignalType
from app.services.trading_bot import TradingBotService


class StrategyBotService:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._state_path = Path(__file__).resolve().parents[2] / "data" / "strategy_bot_state.json"
        self._history_path = Path(__file__).resolve().parents[2] / "data" / "strategy_bot_history.json"
        self._state: Dict[str, Any] = self._default_state()
        self._latest_recommendations: List[Dict[str, Any]] = []
        self._background_task: Optional[asyncio.Task] = None
        self._trading_bot = TradingBotService()
        self._load_state()

    @staticmethod
    def _default_state() -> Dict[str, Any]:
        return {
            "config": {
                "enabled": True,
                "mode": "paper",
                "interval_seconds": 300,
                "max_risk_per_trade": 0.02,
                "max_positions": 3,
                "min_confidence": 6.0,
            },
            "meta": {
                "last_run_at": None,
                "runs_count": 0,
            },
            "weights": {
                "momentum": 1.0,
                "mean_reversion": 1.0,
                "breakout": 1.0,
            },
        }

    def _ensure_parent(self) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> None:
        if self._state_path.exists():
            with self._state_path.open("r", encoding="utf-8") as f:
                self._state = json.load(f)

    def _save_state(self) -> None:
        self._ensure_parent()
        with self._state_path.open("w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def _append_history(self, run_record: Dict[str, Any]) -> None:
        self._ensure_parent()
        if self._history_path.exists():
            with self._history_path.open("r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

        history.append(run_record)
        history = history[-500:]

        with self._history_path.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self._state["config"]["enabled"],
            "mode": self._state["config"]["mode"],
            "interval_seconds": self._state["config"]["interval_seconds"],
            "last_run_at": self._state["meta"]["last_run_at"],
            "runs_count": self._state["meta"]["runs_count"],
            "recommendations_count": len(self._latest_recommendations),
            "strategy_weights": self._state["weights"],
        }

    def get_recommendations(self) -> List[Dict[str, Any]]:
        return self._latest_recommendations

    def update_config(self, config_updates: Dict[str, Any]) -> Dict[str, Any]:
        allowed = {
            "enabled",
            "mode",
            "interval_seconds",
            "max_risk_per_trade",
            "max_positions",
            "min_confidence",
        }
        for key, value in config_updates.items():
            if key in allowed:
                self._state["config"][key] = value
        self._save_state()
        return self.get_status()

    def get_learning_report(self) -> Dict[str, Any]:
        if self._history_path.exists():
            with self._history_path.open("r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

        total_recs = sum(len(item.get("recommendations", [])) for item in history)
        confidences = [
            rec.get("confidence", 0.0)
            for item in history
            for rec in item.get("recommendations", [])
        ]
        avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.0

        strategy_counts: Dict[str, int] = {}
        for item in history:
            for rec in item.get("recommendations", []):
                strategy = rec.get("strategy", "unknown")
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        top = [k for k, _ in sorted(strategy_counts.items(), key=lambda kv: kv[1], reverse=True)[:3]]

        return {
            "total_runs": len(history),
            "recommendations_generated": total_recs,
            "average_confidence": avg_conf,
            "top_strategies": top,
            "strategy_weights": self._state["weights"],
            "last_updated": self._state["meta"]["last_run_at"],
        }

    async def run_cycle(self) -> Dict[str, Any]:
        async with self._lock:
            markets = self._trading_bot.get_markets()
            config = self._state["config"]
            weights = self._state["weights"]
            now = self._now_iso()

            candidates: List[Dict[str, Any]] = []

            for market in markets:
                instrument_id = market.get("instrument_id", "UNKNOWN")
                instrument_name = market.get("name", instrument_id)
                change = float(market.get("change_24h_pct", 0.0))
                volume = float(market.get("volume", 0.0))

                # Strategy 1: momentum
                if abs(change) >= 1:
                    action = SignalType.BUY if change > 0 else SignalType.SELL
                    confidence = min(9.5, 5.0 + abs(change) * 0.6)
                    candidates.append(
                        self._build_candidate(
                            instrument_id,
                            instrument_name,
                            action,
                            confidence,
                            "momentum",
                            f"24h move {change:.2f}% supports momentum continuation",
                            weights["momentum"],
                        )
                    )

                # Strategy 2: mean reversion
                if abs(change) >= 3:
                    action = SignalType.SELL if change > 0 else SignalType.BUY
                    confidence = min(8.8, 4.8 + abs(change) * 0.5)
                    candidates.append(
                        self._build_candidate(
                            instrument_id,
                            instrument_name,
                            action,
                            confidence,
                            "mean_reversion",
                            f"Large move {change:.2f}% may revert",
                            weights["mean_reversion"],
                        )
                    )

                # Strategy 3: breakout proxy
                if volume >= 1_000_000_000 and abs(change) >= 2:
                    action = SignalType.BUY if change > 0 else SignalType.SELL
                    confidence = min(9.0, 5.2 + abs(change) * 0.4)
                    candidates.append(
                        self._build_candidate(
                            instrument_id,
                            instrument_name,
                            action,
                            confidence,
                            "breakout",
                            "High volume + directional move indicates breakout regime",
                            weights["breakout"],
                        )
                    )

            ranked = sorted(candidates, key=lambda c: c["score"], reverse=True)
            selected = [c for c in ranked if c["confidence"] >= config["min_confidence"]][: config["max_positions"]]

            self._latest_recommendations = [
                {
                    "instrument_id": item["instrument_id"],
                    "instrument_name": item["instrument_name"],
                    "action": item["action"],
                    "confidence": round(item["confidence"], 2),
                    "reason": item["reason"],
                    "strategy": item["strategy"],
                    "risk_score": round(item["risk_score"], 3),
                    "expected_rr": round(item["expected_rr"], 2),
                    "timestamp": now,
                }
                for item in selected
            ]

            # Lightweight learning update: reward strategy agreement with current direction proxy.
            for item in selected:
                aligned = (item["action"] == SignalType.BUY and item["market_change"] > 0) or (
                    item["action"] == SignalType.SELL and item["market_change"] < 0
                )
                delta = 0.02 if aligned else -0.02
                strategy = item["strategy"]
                weights[strategy] = round(min(1.6, max(0.4, weights[strategy] + delta)), 3)

            self._state["meta"]["last_run_at"] = now
            self._state["meta"]["runs_count"] += 1
            self._save_state()
            self._append_history(
                {
                    "run_at": now,
                    "config_snapshot": config,
                    "recommendations": self._latest_recommendations,
                    "weights_after_run": weights,
                }
            )

            return {
                "ran_at": now,
                "recommendations_generated": len(self._latest_recommendations),
                "status": self.get_status(),
            }

    def _build_candidate(
        self,
        instrument_id: str,
        instrument_name: str,
        action: SignalType,
        confidence: float,
        strategy: str,
        reason: str,
        strategy_weight: float,
    ) -> Dict[str, Any]:
        risk_score = min(1.0, max(0.1, 1 - (confidence / 12)))
        expected_rr = 1.3 + confidence / 8
        score = confidence * strategy_weight * (1.1 - risk_score)
        market = self._trading_bot.get_market(instrument_id) or {}
        market_change = float(market.get("change_24h_pct", 0.0))
        return {
            "instrument_id": instrument_id,
            "instrument_name": instrument_name,
            "action": action,
            "confidence": confidence,
            "strategy": strategy,
            "reason": reason,
            "risk_score": risk_score,
            "expected_rr": expected_rr,
            "score": score,
            "market_change": market_change,
        }

    async def _runner(self) -> None:
        while True:
            try:
                if self._state["config"]["enabled"]:
                    await self.run_cycle()
                await asyncio.sleep(self._state["config"]["interval_seconds"])
            except asyncio.CancelledError:
                raise
            except Exception:
                await asyncio.sleep(10)

    def start_background(self) -> None:
        if self._background_task and not self._background_task.done():
            return
        self._background_task = asyncio.create_task(self._runner())

    async def stop_background(self) -> None:
        if self._background_task and not self._background_task.done():
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass


strategy_bot_service = StrategyBotService()
