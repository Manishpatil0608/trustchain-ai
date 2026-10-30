import React, { useState } from 'react';
import { Database, CheckCircle2, XCircle, Clock, Filter, Search, Activity, Zap } from 'lucide-react';
import { useAllTelemetry } from '../hooks/useApi';
import { LoadingState, ErrorState, EmptyState, SectionHeader } from './ui/States';

export default function TelemetryCenter() {
  const { data: telemetry, loading, error } = useAllTelemetry();
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  if (loading) return <LoadingState message="STREAMING BEHAVIORAL TELEMETRY STREAM..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;

  const rawEvents = telemetry || [];
  let filtered = [...rawEvents];

  if (filter === 'SUCCESS') filtered = filtered.filter(t => t.success);
  if (filter === 'FAILURE') filtered = filtered.filter(t => !t.success);
  if (search) filtered = filtered.filter(t => t.agent_did.toLowerCase().includes(search.toLowerCase()) || t.task_id.toLowerCase().includes(search.toLowerCase()));

  const totalEvents = rawEvents.length;
  const successCount = rawEvents.filter(t => t.success).length;
  const failCount = totalEvents - successCount;
  const successRate = totalEvents ? ((successCount / totalEvents) * 100).toFixed(1) : '100.0';
  const avgLatency = totalEvents ? Math.round(rawEvents.reduce((acc, t) => acc + t.latency_ms, 0) / totalEvents) : 0;
  const compliantCount = rawEvents.filter(t => !t.compliance_event).length;
  const complianceRate = totalEvents ? ((compliantCount / totalEvents) * 100).toFixed(1) : '100.0';

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <SectionHeader 
        icon={Database}
        title="Behavioral Telemetry Center"
        subtitle="Raw execution event stream, task success tracking, latency metrics, and protocol compliance monitoring."
        badge="REAL-TIME TELEMETRY FEED"
      />

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 font-mono">
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">TOTAL EVENTS</p>
          <h3 className="text-2xl font-bold text-tc-cyan">{totalEvents}</h3>
        </div>
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">SUCCESS RATE</p>
          <h3 className="text-2xl font-bold text-emerald-500 dark:text-emerald-400">{successRate}%</h3>
        </div>
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">FAILED TASKS</p>
          <h3 className={`text-2xl font-bold ${failCount > 0 ? 'text-rose-500' : 'text-slate-400'}`}>{failCount}</h3>
        </div>
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">COMPLIANCE RATE</p>
          <h3 className="text-2xl font-bold text-slate-900 dark:text-slate-100">{complianceRate}%</h3>
        </div>
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">AVG LATENCY</p>
          <h3 className="text-2xl font-bold text-tc-cyan">{avgLatency} ms</h3>
        </div>
      </div>

      {/* Controls & Filter Bar */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4 font-mono text-xs shadow-sm">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-tc-cyan" size={14} />
          <input 
            type="text" 
            placeholder="Search by Agent DID or Task ID..." 
            value={search} 
            onChange={e => setSearch(e.target.value)} 
            className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded py-2 pl-9 pr-3 text-xs text-slate-900 dark:text-slate-200 outline-none focus:border-tc-cyan font-mono" 
          />
        </div>
        <div className="flex items-center gap-3">
          <span className="text-[10px] text-slate-600 dark:text-slate-400 uppercase">Filter:</span>
          <select 
            value={filter} 
            onChange={e => setFilter(e.target.value)} 
            className="bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded text-xs text-cyan-700 dark:text-tc-cyan py-2 px-3 font-mono focus:border-tc-cyan outline-none cursor-pointer">
            <option value="ALL">ALL TELEMETRY EVENTS</option>
            <option value="SUCCESS">SUCCESSFUL EVENTS ONLY</option>
            <option value="FAILURE">FAILED EVENTS ONLY</option>
          </select>
        </div>
      </div>

      {/* Telemetry Log Table */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden font-mono shadow-sm">
        {filtered.length === 0 ? (
          <div className="p-8"><EmptyState message="No telemetry logs match the current search filter." /></div>
        ) : (
          <div className="max-h-[550px] overflow-y-auto custom-scrollbar">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-[#080b13] text-slate-500 dark:text-slate-400 font-mono text-[10px] uppercase tracking-widest border-b border-slate-200 dark:border-slate-800 sticky top-0 z-10">
                <tr>
                  <th className="p-3.5">Timestamp (UTC)</th>
                  <th className="p-3.5">Agent DID</th>
                  <th className="p-3.5">Task ID</th>
                  <th className="p-3.5 text-center">Task Status</th>
                  <th className="p-3.5">Protocol Compliance</th>
                  <th className="p-3.5 text-right">Execution Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {filtered.map(t => (
                  <tr key={t.id} className="hover:bg-slate-50 dark:hover:bg-[#121929]/80 transition-colors">
                    <td className="p-3.5 text-slate-500 dark:text-slate-400 text-[11px] whitespace-nowrap">{new Date(t.timestamp).toLocaleString()}</td>
                    <td className="p-3.5 text-tc-cyan font-bold truncate max-w-[180px]" title={t.agent_did}>{t.agent_did}</td>
                    <td className="p-3.5 text-slate-500 dark:text-slate-400 truncate max-w-[160px]">{t.task_id}</td>
                    <td className="p-3.5 text-center">
                      {t.success ? (
                        <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-950/60 px-2.5 py-0.5 rounded text-[10px] border border-emerald-300 dark:border-emerald-800 font-bold">
                          <CheckCircle2 size={11} /> SUCCESS
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-rose-700 bg-rose-50 dark:text-rose-400 dark:bg-rose-950/60 px-2.5 py-0.5 rounded text-[10px] border border-rose-300 dark:border-rose-800 font-bold">
                          <XCircle size={11} /> FAILED
                        </span>
                      )}
                    </td>
                    <td className="p-3.5 text-slate-600 dark:text-slate-400 text-[11px]">
                      {t.compliance_event ? (
                        <span className="text-amber-600 dark:text-amber-400 font-bold">{t.compliance_event}</span>
                      ) : (
                        <span className="text-emerald-600 dark:text-emerald-400/80 font-semibold">COMPLIANT (1.0)</span>
                      )}
                    </td>
                    <td className="p-3.5 text-right font-bold text-slate-900 dark:text-slate-200">
                      <div className="flex items-center justify-end gap-1">
                        <Clock size={12} className={t.latency_ms > 1500 ? 'text-rose-500' : 'text-tc-cyan'} />
                        <span className={t.latency_ms > 1500 ? 'text-rose-600 dark:text-rose-400' : ''}>{t.latency_ms} ms</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
