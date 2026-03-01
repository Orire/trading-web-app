"use client";

import { type FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { api, type EtoroCredentialsStatus } from "@/lib/api";

const DEFAULT_BASE_URL = "https://api.etoro.com";

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [baseUrl, setBaseUrl] = useState(DEFAULT_BASE_URL);
  const [environment, setEnvironment] = useState("sandbox");
  const [status, setStatus] = useState<EtoroCredentialsStatus | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    void api
      .getEtoroCredentialsStatus()
      .then(setStatus)
      .catch((e) => setError(String(e)));
  }, []);

  const onSave = async (event: FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setSuccess("");
    try {
      const result = await api.saveEtoroCredentials({
        api_key: apiKey,
        api_secret: apiSecret,
        base_url: baseUrl,
        environment,
      });
      setStatus(result);
      setApiSecret("");
      setSuccess("Credentials saved successfully.");
    } catch (e) {
      setError(String(e));
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="mobile-shell pb-12">
      <div className="mx-auto max-w-2xl px-4 pt-6 sm:px-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-slate-900">eToro API Settings</h1>
          <Link href="/" className="text-sm font-medium text-indigo-600">
            Back
          </Link>
        </div>

        <p className="mt-2 text-sm text-slate-600">
          Connect your own eToro account credentials. Values are stored server-side for this
          tenant only.
        </p>

        <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900">Current status</h2>
          {!status ? (
            <p className="mt-2 text-sm text-slate-600">Loading...</p>
          ) : status.configured ? (
            <div className="mt-3 space-y-1 text-sm text-slate-700">
              <p>
                <span className="font-medium">Configured:</span> Yes
              </p>
              <p>
                <span className="font-medium">API key:</span> {status.api_key_masked}
              </p>
              <p>
                <span className="font-medium">Base URL:</span> {status.base_url}
              </p>
              <p>
                <span className="font-medium">Environment:</span> {status.environment}
              </p>
            </div>
          ) : (
            <p className="mt-2 text-sm text-amber-700">Not configured yet.</p>
          )}
        </section>

        <form onSubmit={onSave} className="mt-6 space-y-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900">Update credentials</h2>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">API Key</span>
            <input
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              required
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none ring-indigo-200 focus:border-indigo-500 focus:ring"
              placeholder="Paste your eToro API key"
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">API Secret</span>
            <input
              value={apiSecret}
              onChange={(e) => setApiSecret(e.target.value)}
              required
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none ring-indigo-200 focus:border-indigo-500 focus:ring"
              placeholder="Paste your eToro API secret"
              type="password"
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Base URL</span>
            <input
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              required
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none ring-indigo-200 focus:border-indigo-500 focus:ring"
              placeholder="https://api.etoro.com"
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Environment</span>
            <select
              value={environment}
              onChange={(e) => setEnvironment(e.target.value)}
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none ring-indigo-200 focus:border-indigo-500 focus:ring"
            >
              <option value="sandbox">Sandbox</option>
              <option value="production">Production</option>
            </select>
          </label>

          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          {success ? <p className="text-sm text-emerald-700">{success}</p> : null}

          <button
            type="submit"
            disabled={saving}
            className="w-full rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {saving ? "Saving..." : "Save credentials"}
          </button>
        </form>
      </div>
    </main>
  );
}
