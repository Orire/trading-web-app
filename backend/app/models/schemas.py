"""
Pydantic models for API requests/responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SignalType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class RiskTolerance(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


# Signal Models
class SignalResponse(BaseModel):
    id: str
    instrument_id: str
    instrument_name: str
    signal_type: SignalType
    confidence: float = Field(ge=0, le=10)
    current_price: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_amount: Optional[float] = None
    position_size: Optional[float] = None
    risk_reward_ratio: float
    reason: str
    indicators: Dict[str, Any]
    timestamp: datetime


# Position Models
class PositionResponse(BaseModel):
    id: str
    instrument_id: str
    instrument_name: str
    direction: str
    entry_price: float
    current_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    size: float
    unrealized_pnl: float
    opened_at: datetime
    last_updated: datetime


# Goal Models
class GoalCreate(BaseModel):
    initial_investment: float = Field(gt=0)
    target_amount: float = Field(gt=0)
    timeframe_days: int = Field(gt=0, le=365)
    risk_tolerance: RiskTolerance


class GoalRequirements(BaseModel):
    required_return_pct: float
    daily_target: float
    required_win_rate: float
    avg_profit_per_trade: float
    min_risk_reward_ratio: float
    feasibility: str
    recommended_trades_per_day: int
    recommended_position_size: float


class GoalProgress(BaseModel):
    current_amount: float
    progress_percentage: float
    days_remaining: int
    days_elapsed: int
    daily_target: float
    today_progress: float
    on_track: bool
    projected_completion_date: Optional[datetime] = None


class GoalResponse(BaseModel):
    id: str
    initial_investment: float
    target_amount: float
    timeframe_days: int
    risk_tolerance: RiskTolerance
    created_at: datetime
    status: GoalStatus
    progress: GoalProgress
    requirements: GoalRequirements


class GoalUpdate(BaseModel):
    target_amount: Optional[float] = None
    timeframe_days: Optional[int] = None
    risk_tolerance: Optional[RiskTolerance] = None
    status: Optional[GoalStatus] = None


# Strategy Models
class StrategyConfig(BaseModel):
    goal_id: str
    strategies: List[str]
    risk_per_trade: float
    max_positions: int
    instrument_types: List[str]
    position_sizing: str
    entry_criteria: Dict[str, Any]
    exit_criteria: Dict[str, Any]


# Performance Models
class PerformanceResponse(BaseModel):
    total_trades: int
    completed_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    average_pnl: float
    profit_factor: float
    max_drawdown: float


# Market Models
class MarketResponse(BaseModel):
    instrument_id: str
    name: str
    current_price: float
    change_24h: float
    change_24h_pct: float
    volume: float
    instrument_type: str


# Settings Models
class EtoroCredentialsCreate(BaseModel):
    api_key: str = Field(min_length=8)
    api_secret: str = Field(min_length=8)
    base_url: str = Field(min_length=8)
    environment: str = Field(default="sandbox")


class EtoroCredentialsResponse(BaseModel):
    configured: bool
    api_key_masked: Optional[str] = None
    base_url: Optional[str] = None
    environment: Optional[str] = None
    updated_at: Optional[datetime] = None


# Strategy Bot Models
class StrategyBotConfig(BaseModel):
    enabled: bool = True
    mode: str = "paper"
    interval_seconds: int = Field(default=300, ge=30, le=3600)
    max_risk_per_trade: float = Field(default=0.02, ge=0.001, le=0.1)
    max_positions: int = Field(default=3, ge=1, le=20)
    min_confidence: float = Field(default=6.0, ge=0, le=10)


class StrategyRecommendation(BaseModel):
    instrument_id: str
    instrument_name: str
    action: SignalType
    confidence: float = Field(ge=0, le=10)
    reason: str
    strategy: str
    risk_score: float = Field(ge=0, le=1)
    expected_rr: float = Field(ge=0.1, le=10)
    timestamp: datetime


class StrategyBotStatus(BaseModel):
    enabled: bool
    mode: str
    interval_seconds: int
    last_run_at: Optional[datetime] = None
    runs_count: int = 0
    recommendations_count: int = 0
    strategy_weights: Dict[str, float]


class StrategyLearningReport(BaseModel):
    total_runs: int
    recommendations_generated: int
    average_confidence: float
    top_strategies: List[str]
    strategy_weights: Dict[str, float]
    last_updated: Optional[datetime] = None
