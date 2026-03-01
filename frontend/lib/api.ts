const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export type Performance = {
  total_pnl: number;
  win_rate: number;
};

export type Position = {
  id: string;
  instrument_name: string;
  unrealized_pnl: number;
};

export type Signal = {
  id: string;
  instrument_name: string;
  signal_type: "buy" | "sell";
  confidence: number;
};

export type EtoroCredentialsStatus = {
  configured: boolean;
  api_key_masked?: string;
  base_url?: string;
  environment?: string;
  updated_at?: string;
};

export type EtoroCredentialsInput = {
  api_key: string;
  api_secret: string;
  base_url: string;
  environment: string;
};

export type BotStatus = {
  enabled: boolean;
  mode: string;
  interval_seconds: number;
  last_run_at?: string | null;
  runs_count: number;
  recommendations_count: number;
  strategy_weights: Record<string, number>;
};

export type BotRecommendation = {
  instrument_id: string;
  instrument_name: string;
  action: "buy" | "sell" | "hold";
  confidence: number;
  reason: string;
  strategy: string;
  risk_score: number;
  expected_rr: number;
  timestamp: string;
};

export type BotLearningReport = {
  total_runs: number;
  recommendations_generated: number;
  average_confidence: number;
  top_strategies: string[];
  strategy_weights: Record<string, number>;
  last_updated?: string | null;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API ${response.status}: ${detail}`);
  }

  return (await response.json()) as T;
}

export const api = {
  getPerformance: () => request<Performance>("/api/performance"),
  getPositions: () => request<Position[]>("/api/positions"),
  getSignals: () => request<Signal[]>("/api/signals"),
  getEtoroCredentialsStatus: () =>
    request<EtoroCredentialsStatus>("/api/settings/etoro-credentials"),
  saveEtoroCredentials: (payload: EtoroCredentialsInput) =>
    request<EtoroCredentialsStatus>("/api/settings/etoro-credentials", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getBotStatus: () => request<BotStatus>("/api/bot/status"),
  runBotCycle: () => request<{ status: BotStatus; ran_at: string; recommendations_generated: number }>("/api/bot/run", { method: "POST" }),
  getBotRecommendations: () => request<BotRecommendation[]>("/api/bot/recommendations"),
  getBotLearningReport: () => request<BotLearningReport>("/api/bot/learning-report"),
};
