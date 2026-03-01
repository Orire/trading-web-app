"use client";

import { useEffect, useState } from "react";
import { api, type Performance, type Position, type Signal } from "@/lib/api";
import { wsClient } from "@/lib/websocket";

export default function Dashboard() {
  const [performance, setPerformance] = useState<Performance | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);

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
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <h1 className="text-2xl font-bold text-indigo-600 flex items-center">
              📊 Trading Dashboard
            </h1>
            <div className="flex items-center space-x-4">
              <a href="/" className="text-gray-700 hover:text-indigo-600">
                Home
              </a>
              <a href="/strategy" className="text-gray-700 hover:text-indigo-600">
                Strategy
              </a>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">Total P&amp;L</div>
            <div className="text-2xl font-bold">
              ${performance?.total_pnl?.toFixed(2) || "0.00"}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">Win Rate</div>
            <div className="text-2xl font-bold">
              {performance?.win_rate?.toFixed(1) || "0.0"}%
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">Open Positions</div>
            <div className="text-2xl font-bold">{positions.length}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">Active Signals</div>
            <div className="text-2xl font-bold">{signals.length}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Open Positions</h2>
            {positions.length === 0 ? (
              <p className="text-gray-500">No open positions</p>
            ) : (
              <div className="space-y-4">
                {positions.map((pos) => (
                  <div key={pos.id} className="border-b pb-4">
                    <div className="flex justify-between">
                      <span className="font-medium">{pos.instrument_name}</span>
                      <span
                        className={
                          pos.unrealized_pnl >= 0 ? "text-green-600" : "text-red-600"
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

          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Recent Signals</h2>
            {signals.length === 0 ? (
              <p className="text-gray-500">No signals available</p>
            ) : (
              <div className="space-y-4">
                {signals.slice(0, 5).map((signal) => (
                  <div key={signal.id} className="border-b pb-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="font-medium">{signal.instrument_name}</span>
                        <span
                          className={`ml-2 px-2 py-1 rounded text-xs ${
                            signal.signal_type === "buy"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {signal.signal_type?.toUpperCase()}
                        </span>
                      </div>
                      <span className="text-sm text-gray-600">
                        Confidence: {signal.confidence?.toFixed(1)}/10
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
