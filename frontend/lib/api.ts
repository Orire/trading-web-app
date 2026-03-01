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
};
