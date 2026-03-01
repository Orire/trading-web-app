"use client";

import { useEffect } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

export default function Home() {
  useEffect(() => {
    // Test API connection
    api.getPerformance()
      .then(() => console.log("API connected"))
      .catch((e) => console.log("API not available:", e));
  }, []);

  return (
    <main className="mobile-shell pb-12">
      <div className="mx-auto max-w-4xl px-4 pt-6 sm:px-6">
        <div className="hero-card">
          <p className="inline-flex items-center rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-700">
            Beginner Friendly
          </p>
          <h1 className="mt-3 text-3xl font-bold text-slate-900 sm:text-4xl">
            TradingAPP_Ri
          </h1>
          <p className="mt-2 text-sm text-slate-600 sm:text-base">
            Mobile-first trading control center for signals, performance, and personalized goals.
          </p>
          <div className="mt-4 grid grid-cols-2 gap-3 sm:flex sm:flex-wrap">
            <Link href="/dashboard" className="btn-primary text-center">
              Open dashboard
            </Link>
            <Link href="/settings" className="btn-secondary text-center">
              Connect eToro API
            </Link>
          </div>
        </div>

        <section className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <Link href="/dashboard" className="tile-card">
            <h2 className="tile-title">Live Dashboard</h2>
            <p className="tile-copy">Positions, P&L, and new signals in one place.</p>
          </Link>
          <Link href="/settings" className="tile-card">
            <h2 className="tile-title">API Connection</h2>
            <p className="tile-copy">Save your eToro API key and secret securely on backend.</p>
          </Link>
          <Link href="/strategy" className="tile-card">
            <h2 className="tile-title">Goal Strategy</h2>
            <p className="tile-copy">Define return goals and suggested plan shape.</p>
          </Link>
          <Link href="/learn" className="tile-card">
            <h2 className="tile-title">Learning Hub</h2>
            <p className="tile-copy">Quick guidance and practical next steps.</p>
          </Link>
        </section>
      </div>
    </main>
  );
}
