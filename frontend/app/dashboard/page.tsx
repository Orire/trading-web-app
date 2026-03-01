"use client";

import { useEffect, useState } from "react";
import {
  api,
  type Performance,
  type Position,
  type Signal,
  type BotStatus,
  type BotRecommendation,
  type BotLearningReport,
} from "@/lib/api";
import { wsClient } from "@/lib/websocket";

export default function Dashboard() {
  const [performance, setPerformance] = useState<Performance | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [botStatus, setBotStatus] = useState<BotStatus | null>(null);
  const [botRecommendations, setBotRecommendations] = useState<BotRecommendation[]>([]);
  const [botLearning, setBotLearning] = useState<BotLearningReport | null>(null);
  const [botRunning, setBotRunning] = useState(false);

  useEffect(() => {
    wsClient.connect();
    void loadData();

    wsClient.on("signal:new", (data: any) => {
      setSignals((prev) => [data, ...prev]);
    });

    wsClient.on("position:updated", (data: any) => {
      setPositions((prev) => prev.map((p) => (p.id === data.id ? data : p)));
    });

    return () => {
      wsClient.disconnect();
    };
  }, []);

  const loadData = async () => {
    try {
      const [perf, pos, sigs] = await Promise.all([
        api.getPerformance(),
        api.getPositions(),
        api.getSignals(),
      ]);
      setPerformance(perf);
      setPositions(pos);
      setSignals(sigs);
      const [status, recommendations, learning] = await Promise.all([
        api.getBotStatus(),
        api.getBotRecommendations(),
        api.getBotLearningReport(),
      ]);
      setBotStatus(status);
      setBotRecommendations(recommendations);
      setBotLearning(learning);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  const runBotNow = async () => {
    setBotRunning(true);
    try {
      await api.runBotCycle();
      await loadData();
    } catch (error) {
      console.error("Error running bot:", error);
    } finally {
      setBotRunning(false);
    }
  };

  return (
    <main className="mobile-shell pb-12">
      <div className="mx-auto max-w-5xl px-4 pt-6 sm:px-6">
        <div className="hero-card">
          <div className="flex items-center justify-between gap-3">
            <h1 className="text-2xl font-semibold text-slate-900">Trading Dashboard</h1>
            <a href="/settings" className="btn-secondary text-xs sm:text-sm">
              API Settings
            </a>
          </div>
          <p className="mt-2 text-sm text-slate-600">
            Real-time summary optimized for mobile: swipe, scan, decide.
          </p>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
          <div className="stat-card">
            <div className="stat-label">Total P&amp;L</div>
            <div className="stat-value">
              ${performance?.total_pnl?.toFixed(2) || "0.00"}
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Win Rate</div>
            <div className="stat-value">
              {performance?.win_rate?.toFixed(1) || "0.0"}%
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Open Positions</div>
            <div className="stat-value">{positions.length}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Active Signals</div>
            <div className="stat-value">{signals.length}</div>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div className="tile-card">
            <h2 className="tile-title">Open Positions</h2>
            {positions.length === 0 ? (
              <p className="tile-copy">No open positions</p>
            ) : (
              <div className="mt-3 space-y-3">
                {positions.map((pos) => (
                  <div key={pos.id} className="rounded-xl border border-slate-200 p-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-800">{pos.instrument_name}</span>
                      <span
                        className={
                          pos.unrealized_pnl >= 0
                            ? "text-sm font-semibold text-emerald-600"
                            : "text-sm font-semibold text-rose-600"
                        }
                      >
                        ${pos.unrealized_pnl?.toFixed(2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="tile-card">
            <h2 className="tile-title">Recent Signals</h2>
            {signals.length === 0 ? (
              <p className="tile-copy">No signals available</p>
            ) : (
              <div className="mt-3 space-y-3">
                {signals.slice(0, 5).map((signal) => (
                  <div key={signal.id} className="rounded-xl border border-slate-200 p-3">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-sm font-medium text-slate-800">{signal.instrument_name}</span>
                        <span
                          className={`ml-2 rounded px-2 py-1 text-[11px] font-semibold ${
                            signal.signal_type === "buy"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {signal.signal_type?.toUpperCase()}
                        </span>
                      </div>
                      <span className="text-xs text-slate-600">
                        Confidence: {signal.confidence?.toFixed(1)}/10
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div className="tile-card">
            <div className="flex items-center justify-between gap-3">
              <h2 className="tile-title">Strategy Bot</h2>
              <button
                onClick={runBotNow}
                disabled={botRunning}
                className="btn-primary text-xs disabled:opacity-60"
              >
                {botRunning ? "Running..." : "Run now"}
              </button>
            </div>
            {!botStatus ? (
              <p className="tile-copy">Loading bot status...</p>
            ) : (
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-700">
                <p>
                  <span className="font-semibold">Mode:</span> {botStatus.mode}
                </p>
                <p>
                  <span className="font-semibold">Enabled:</span>{" "}
                  {botStatus.enabled ? "Yes" : "No"}
                </p>
                <p>
                  <span className="font-semibold">Runs:</span> {botStatus.runs_count}
                </p>
                <p>
                  <span className="font-semibold">Recs:</span>{" "}
                  {botStatus.recommendations_count}
                </p>
              </div>
            )}
          </div>

          <div className="tile-card">
            <h2 className="tile-title">Learning Snapshot</h2>
            {!botLearning ? (
              <p className="tile-copy">Loading learning report...</p>
            ) : (
              <div className="mt-3 space-y-1 text-xs text-slate-700">
                <p>
                  <span className="font-semibold">Total runs:</span>{" "}
                  {botLearning.total_runs}
                </p>
                <p>
                  <span className="font-semibold">Avg confidence:</span>{" "}
                  {botLearning.average_confidence}
                </p>
                <p>
                  <span className="font-semibold">Top strategies:</span>{" "}
                  {botLearning.top_strategies.join(", ") || "n/a"}
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="mt-5 tile-card">
          <h2 className="tile-title">Bot Recommendations</h2>
          {botRecommendations.length === 0 ? (
            <p className="tile-copy">No recommendations yet. Run bot once to generate.</p>
          ) : (
            <div className="mt-3 space-y-2">
              {botRecommendations.map((rec) => (
                <div
                  key={`${rec.instrument_id}-${rec.timestamp}-${rec.strategy}`}
                  className="rounded-xl border border-slate-200 p-3"
                >
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-900">
                      {rec.instrument_name}
                    </p>
                    <span
                      className={`rounded px-2 py-1 text-[11px] font-semibold ${
                        rec.action === "buy"
                          ? "bg-emerald-100 text-emerald-700"
                          : rec.action === "sell"
                            ? "bg-rose-100 text-rose-700"
                            : "bg-slate-200 text-slate-700"
                      }`}
                    >
                      {rec.action.toUpperCase()}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">{rec.reason}</p>
                  <p className="mt-1 text-[11px] text-slate-500">
                    {rec.strategy} · confidence {rec.confidence.toFixed(1)} · RR{" "}
                    {rec.expected_rr.toFixed(2)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
