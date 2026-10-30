import React, { useEffect, useState } from 'react';
import { 
  Server, 
  Activity, 
  Database, 
  ShieldCheck, 
  AlertCircle, 
  RefreshCw, 
  Cpu 
} from 'lucide-react';
import { trustApi } from '../api';
import { SectionHeader, HealthBadge } from './ui/States';

export default function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [latency, setLatency] = useState(0);
  const [lastChecked, setLastChecked] = useState(null);

  const checkHealth = () => {
    setLoading(true);
    const start = performance.now();
    trustApi
      .getHealth()
      .then((res) => {
        setHealth(res);
        setLatency(Math.round(performance.now() - start));
        setLastChecked(new Date().toLocaleTimeString());
      })
      .catch((err) => {
        setHealth({ 
          status: 'error', 
          error: err?.message || 'Failed to connect to FastAPI backend on port 8050' 
        });
        setLatency(Math.round(performance.now() - start));
        setLastChecked(new Date().toLocaleTimeString());
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    checkHealth();
  }, []);

  // 1. Authoritative Backend Status Resolver
  const getBackendStatus = () => {
    if (loading) return { status: 'CHECKING', message: 'Pinging FastAPI ASGI gateway...', isOk: false };
    if (!health || health.status === 'error' || health.error) {
      return { 
        status: 'OFFLINE', 
        message: health?.error || 'FastAPI backend (:8050) unreachable', 
        isOk: false,
        isDegraded: false 
      };
    }
    const comp = health.components?.fastapi;
    if (comp) {
      const isOk = comp.status === 'ok';
      const isDegraded = comp.status === 'degraded';
      return {
        status: isOk ? 'ONLINE' : (isDegraded ? 'DEGRADED' : 'OFFLINE'),
        message: comp.message || `Port ${comp.port || 8050} / Uvicorn ASGI`,
        isOk,
        isDegraded,
        version: comp.version || '1.0.0'
      };
    }
    if (health.status === 'ok') {
      return { status: 'ONLINE', message: 'Port 8050 / Uvicorn ASGI operational', isOk: true, isDegraded: false };
    }
    return { status: 'UNKNOWN', message: 'Unrecognized backend health response', isOk: false, isDegraded: true };
  };

  // 2. Authoritative Database Status Resolver
  const getDatabaseStatus = () => {
    if (loading) return { status: 'CHECKING', message: 'Executing database connection probe...', isOk: false };
    if (!health || health.status === 'error' || health.error) {
      return { 
        status: 'UNREACHABLE', 
        message: 'Host backend unreachable (check skipped)', 
        isOk: false,
        isDegraded: false 
      };
    }
    const comp = health.components?.database;
    if (comp) {
      const isOk = comp.status === 'ok';
      const isDegraded = comp.status === 'degraded';
      return {
        status: isOk ? 'SYNCED' : (isDegraded ? 'DEGRADED' : 'ERROR'),
        message: comp.message || 'SQLite VDR database connected',
        latencyMs: comp.latency_ms,
        mode: comp.mode || 'WAL',
        error: comp.error,
        isOk,
        isDegraded
      };
    }
    // Fallback if legacy response without components
    if (health.status === 'ok') {
      return { status: 'SYNCED', message: 'WAL Mode / Active SQLite connection', isOk: true, isDegraded: false };
    }
    return { status: 'UNKNOWN', message: 'No database component probe in response', isOk: false, isDegraded: true };
  };

  // 3. Authoritative Trust Engine Status Resolver
  const getTrustStatus = () => {
    if (loading) return { status: 'INITIALIZING', message: 'Validating in-process math formulas...', isOk: false };
    if (!health || health.status === 'error' || health.error) {
      return { 
        status: 'UNREACHABLE', 
        message: 'Host backend unreachable (check skipped)', 
        isOk: false,
        isDegraded: false 
      };
    }
    const comp = health.components?.trust_engine;
    if (comp) {
      const isOk = comp.status === 'ok';
      const isDegraded = comp.status === 'degraded';
      return {
        status: isOk ? 'OPERATIONAL' : (isDegraded ? 'DEGRADED' : 'ERROR'),
        message: comp.message || 'Temporal EMA & Multi-Factor Core operational',
        weights: comp.weights,
        error: comp.error,
        isOk,
        isDegraded
      };
    }
    if (health.status === 'ok') {
      return { status: 'OPERATIONAL', message: 'Temporal EMA & Multi-Factor (In-process)', isOk: true, isDegraded: false };
    }
    return { status: 'UNKNOWN', message: 'No trust engine probe in response', isOk: false, isDegraded: true };
  };

  // 4. Latency Status Resolver
  const getLatencyInfo = () => {
    if (loading) return { rating: 'MEASURING...', color: 'text-tc-cyan', badge: 'PENDING' };
    if (!health || health.status === 'error' || health.error) {
      return { rating: 'CONNECTION FAILED', color: 'text-rose-500', badge: 'OFFLINE' };
    }
    if (latency < 50) return { rating: 'OPTIMAL (<50ms)', color: 'text-emerald-500 dark:text-emerald-400', badge: 'OPTIMAL' };
    if (latency < 150) return { rating: 'NORMAL (<150ms)', color: 'text-tc-cyan', badge: 'NORMAL' };
    return { rating: 'ELEVATED (>150ms)', color: 'text-amber-500', badge: 'SLOW' };
  };

  const backend = getBackendStatus();
  const database = getDatabaseStatus();
  const trustCore = getTrustStatus();
  const latencyInfo = getLatencyInfo();

  const isDegradedOrOffline = (!backend.isOk && !loading) || (!database.isOk && !loading) || (!trustCore.isOk && !loading);
  const activeError = health?.error || database.error || trustCore.error;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={Server}
        title="System Diagnostics & Telemetry"
        subtitle="AUTHORITATIVE PLATFORM INFRASTRUCTURE, VDR, AND ENGINE PROBES"
        action={
          <div className="flex items-center gap-3">
            {lastChecked && (
              <span className="text-[10px] font-mono text-slate-500 hidden sm:inline">
                Last probe: {lastChecked}
              </span>
            )}
            <button
              onClick={checkHealth}
              disabled={loading}
              className="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-100 hover:bg-slate-200 text-cyan-700 dark:text-cyan-400 font-mono text-xs border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700 transition-colors disabled:opacity-50 cursor-pointer shadow-xs"
            >
              <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
              RUN DIAGNOSTICS
            </button>
          </div>
        }
      />

      {/* Degradation / Error Alert Banner */}
      {isDegradedOrOffline && (
        <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/80 dark:bg-rose-950/30 text-rose-900 dark:text-rose-200 text-xs font-mono flex items-start gap-3 shadow-xs">
          <AlertCircle size={18} className="text-rose-600 dark:text-rose-400 mt-0.5 shrink-0" />
          <div className="space-y-1">
            <div className="font-bold uppercase tracking-wider">Infrastructure Alert — Subsystem Degradation Detected</div>
            <div className="text-slate-600 dark:text-slate-300 text-[11px]">
              {activeError || 'One or more authoritative subsystem probes reported abnormal status. Review telemetry below for details.'}
            </div>
          </div>
        </div>
      )}

      {/* 4 Health Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Backend Card */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 flex flex-col items-center text-center shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center mb-3">
            <Server
              size={24}
              className={
                backend.isOk 
                  ? 'text-emerald-500' 
                  : (backend.isDegraded ? 'text-amber-500' : (loading ? 'text-tc-cyan animate-pulse' : 'text-rose-500'))
              }
            />
          </div>
          <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-3">FastAPI Backend</h3>
          {loading ? (
            <span className="animate-pulse text-[10px] text-tc-cyan font-mono tracking-widest">PINGING...</span>
          ) : (
            <HealthBadge status={backend.status} />
          )}
          <div className="mt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400">{backend.message}</div>
        </div>

        {/* SQLite VDR Card */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 flex flex-col items-center text-center shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center mb-3">
            <Database
              size={24}
              className={
                database.isOk 
                  ? 'text-tc-cyan' 
                  : (database.isDegraded ? 'text-amber-500' : (loading ? 'text-tc-cyan animate-pulse' : 'text-rose-500'))
              }
            />
          </div>
          <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-3">SQLite VDR</h3>
          {loading ? (
            <span className="animate-pulse text-[10px] text-tc-cyan font-mono tracking-widest">CHECKING...</span>
          ) : (
            <HealthBadge status={database.status} />
          )}
          <div className="mt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400">
            {database.latencyMs !== undefined ? `WAL Mode • Query Latency ${database.latencyMs}ms` : database.message}
          </div>
        </div>

        {/* API Latency Card */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 flex flex-col items-center text-center shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center mb-3">
            <Activity size={24} className={loading ? 'text-tc-cyan animate-pulse' : latencyInfo.color} />
          </div>
          <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-2">Roundtrip Latency</h3>
          {loading ? (
            <span className="animate-pulse text-[10px] text-tc-cyan font-mono tracking-widest">MEASURING...</span>
          ) : (
            <span className="text-2xl font-mono font-bold text-slate-900 dark:text-slate-100">
              {health?.status === 'error' ? '---' : latency} <span className="text-xs text-tc-cyan font-normal">ms</span>
            </span>
          )}
          <div className="mt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400">
            {latencyInfo.rating}
          </div>
        </div>

        {/* Trust Engine Card */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 flex flex-col items-center text-center shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center mb-3">
            <ShieldCheck
              size={24}
              className={
                trustCore.isOk 
                  ? 'text-emerald-500' 
                  : (trustCore.isDegraded ? 'text-amber-500' : (loading ? 'text-tc-cyan animate-pulse' : 'text-slate-500'))
              }
            />
          </div>
          <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-3">Trust Math Core</h3>
          {loading ? (
            <span className="animate-pulse text-[10px] text-tc-cyan font-mono tracking-widest">INITIALIZING...</span>
          ) : (
            <HealthBadge status={trustCore.status} />
          )}
          <div className="mt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400">
            {trustCore.weights ? `Multi-Factor EMA (w1=0.6, λ=0.7)` : trustCore.message}
          </div>
        </div>
      </div>

      {/* Authoritative Subsystem Verification Table */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-xs">
        <div className="px-5 py-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/40 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Cpu size={14} className="text-tc-cyan" />
            <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
              Subsystem Verification & Health Audit
            </h4>
          </div>
          <span className="text-[10px] font-mono text-slate-500">
            Probe Target: http://localhost:8050/health
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-[10px] text-slate-500 uppercase tracking-wider bg-slate-50/30 dark:bg-slate-900/20">
                <th className="py-2.5 px-4 font-semibold">Subsystem</th>
                <th className="py-2.5 px-4 font-semibold">Architecture Boundary</th>
                <th className="py-2.5 px-4 font-semibold">Authoritative Health Probe</th>
                <th className="py-2.5 px-4 font-semibold">Diagnostic Output</th>
                <th className="py-2.5 px-4 font-semibold text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {/* Row 1: FastAPI */}
              <tr className="hover:bg-slate-50 dark:hover:bg-slate-900/30 transition-colors">
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Server size={14} className="text-slate-400" />
                  FastAPI Application Server
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-400">
                  Uvicorn ASGI Gateway (:8050)
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-300">
                  <span className="text-slate-500 dark:text-slate-400 font-mono text-[11px]">HTTP GET /health → 200 OK</span>
                </td>
                <td className="py-3 px-4 text-[11px] text-slate-600 dark:text-slate-400">
                  {backend.message}
                </td>
                <td className="py-3 px-4 text-right">
                  <HealthBadge status={backend.status} />
                </td>
              </tr>

              {/* Row 2: SQLite VDR */}
              <tr className="hover:bg-slate-50 dark:hover:bg-slate-900/30 transition-colors">
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Database size={14} className="text-slate-400" />
                  SQLite Verifiable Data Registry
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-400">
                  vdr.db • WAL Journaling Mode
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-300">
                  <span className="text-slate-500 dark:text-slate-400 font-mono text-[11px]">SQL: SELECT 1 execution test</span>
                </td>
                <td className="py-3 px-4 text-[11px] text-slate-600 dark:text-slate-400">
                  {database.latencyMs !== undefined ? `Query execution verified in ${database.latencyMs}ms` : database.message}
                </td>
                <td className="py-3 px-4 text-right">
                  <HealthBadge status={database.status} />
                </td>
              </tr>

              {/* Row 3: Trust Math Core */}
              <tr className="hover:bg-slate-50 dark:hover:bg-slate-900/30 transition-colors">
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <ShieldCheck size={14} className="text-slate-400" />
                  Trust Intelligence Math Core
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-400">
                  In-Process Behavioral Math Engine
                </td>
                <td className="py-3 px-4 text-slate-600 dark:text-slate-300">
                  <span className="text-slate-500 dark:text-slate-400 font-mono text-[11px]">P_i(t) & T_i(t) formula verification</span>
                </td>
                <td className="py-3 px-4 text-[11px] text-slate-600 dark:text-slate-400">
                  Weights: w1=0.6, w2=0.3, w3=0.1 | Decay λ=0.7
                </td>
                <td className="py-3 px-4 text-right">
                  <HealthBadge status={trustCore.status} />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
