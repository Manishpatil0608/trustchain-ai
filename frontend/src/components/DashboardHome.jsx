import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Shield, ShieldAlert, Activity, GitMerge, Server, Lock, Layers, 
  CheckCircle2, ArrowRight, AlertTriangle, TrendingUp, BarChart3, 
  Clock, User, ExternalLink, XCircle, ChevronRight, Info
} from 'lucide-react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, ReferenceLine 
} from 'recharts';
import { useAgents, useAllTelemetry, useAllAudit, useHealth } from '../hooks/useApi';
import { trustApi } from '../api';
import { useTheme } from '../context/ThemeContext';
import { LoadingState, ErrorState, EmptyState, TrustBadge } from './ui/States';

export default function DashboardHome() {
  const navigate = useNavigate();
  const { isDark, chartTheme } = useTheme();

  const agentsQuery = useAgents();
  const telemetryQuery = useAllTelemetry();
  const auditQuery = useAllAudit();
  const healthQuery = useHealth();

  // Active view mode: 'trajectory' (time-series) or 'ranking' (cross-sectional horizontal bar)
  const [viewMode, setViewMode] = useState('trajectory');
  const [selectedDid, setSelectedDid] = useState('');
  const [agentTelemetry, setAgentTelemetry] = useState([]);
  const [loadingTelemetry, setLoadingTelemetry] = useState(false);

  const agents = agentsQuery.data || [];
  const telemetry = telemetryQuery.data || [];
  const audits = auditQuery.data || [];
  const health = healthQuery.data || { status: 'error' };

  // Set default selected agent when agents list loads
  useEffect(() => {
    if (agents.length > 0 && (!selectedDid || !agents.some(a => (a.agent_did || a.did) === selectedDid))) {
      setSelectedDid(agents[0].agent_did || agents[0].did);
    }
  }, [agents, selectedDid]);

  // Fetch telemetry history specifically for the selected agent
  useEffect(() => {
    if (!selectedDid) {
      setAgentTelemetry([]);
      return;
    }

    let isMounted = true;
    setLoadingTelemetry(true);

    trustApi.getAgentTelemetry(selectedDid)
      .then((data) => {
        if (isMounted) {
          setAgentTelemetry(data || []);
        }
      })
      .catch(() => {
        if (isMounted) {
          // Fallback: filter from all telemetry in memory
          const fallback = telemetry.filter((t) => t.agent_did === selectedDid);
          setAgentTelemetry(fallback);
        }
      })
      .finally(() => {
        if (isMounted) setLoadingTelemetry(false);
      });

    return () => { isMounted = false; };
  }, [selectedDid, telemetry]);

  if (agentsQuery.loading || telemetryQuery.loading || auditQuery.loading || healthQuery.loading) {
    return <LoadingState message="INITIALIZING SECURITY OPERATIONS CENTER..." />;
  }
  if (agentsQuery.error) {
    return <ErrorState error={agentsQuery.error} retry={() => window.location.reload()} />;
  }

  // Active agents (excluding REVOKED) for average trust score calculation
  const activeAgents = agents.filter(a => a.trust_state !== 'REVOKED');
  const stats = {
    total: agents.length,
    trusted: agents.filter(a => a.trust_state === 'TRUSTED').length,
    suspicious: agents.filter(a => a.trust_state === 'SUSPICIOUS').length,
    quarantined: agents.filter(a => a.trust_state === 'QUARANTINED').length,
    revoked: agents.filter(a => a.trust_state === 'REVOKED').length,
    avg: activeAgents.length
      ? (activeAgents.reduce((acc, a) => acc + (a.trust_score ?? 0), 0) / activeAgents.length).toFixed(4)
      : '0.0000',
  };

  const selectedAgent = agents.find(a => (a.agent_did || a.did) === selectedDid) || agents[0];

  // Part A: Distribution data for Donut Chart
  const pieData = [
    { name: 'TRUSTED', value: stats.trusted, color: chartTheme.trusted },
    { name: 'SUSPICIOUS', value: stats.suspicious, color: chartTheme.suspicious },
    { name: 'QUARANTINED', value: stats.quarantined, color: chartTheme.quarantined },
    { name: 'REVOKED', value: stats.revoked, color: chartTheme.revoked },
  ].filter(d => d.value > 0);

  // Cross-Sectional Ranking Data (Sorted Horizontal Bar Chart)
  const rankingData = [...agents]
    .map(a => {
      const did = a.agent_did || a.did || '';
      const shortDid = did.length > 14 ? `...${did.slice(-8)}` : did;
      const label = a.agent_name ? `${a.agent_name} (${shortDid})` : shortDid;
      return {
        did,
        name: a.agent_name || 'Agent',
        label,
        score: typeof a.trust_score === 'number' ? parseFloat(a.trust_score.toFixed(4)) : parseFloat(a.trust_score) || 0,
        state: a.trust_state || 'TRUSTED',
      };
    })
    .sort((a, b) => b.score - a.score);

  // Part B: Time-Series Data Reconstruction for the Selected Agent
  // Computes the chronological trust trajectory strictly for this agent
  const timeSeriesData = (() => {
    if (!agentTelemetry || agentTelemetry.length === 0) {
      return [];
    }

    // Sort telemetry chronologically (oldest first)
    const sorted = [...agentTelemetry].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    const points = [];
    let prevTrust = 1.0; // Baseline initial trust

    sorted.forEach((event, idx) => {
      // Sliding window of up to 10 events up to current event (same as backend trust engine)
      const windowEvents = sorted.slice(Math.max(0, idx - 9), idx + 1);
      const sRate = windowEvents.filter(e => e.success).length / windowEvents.length;
      const cRate = windowEvents.filter(e => !e.compliance_event).length / windowEvents.length;
      const avgLat = windowEvents.reduce((acc, e) => acc + (e.latency_ms || 0), 0) / windowEvents.length;
      const lPenalty = Math.min(1.0, Math.max(0.0, avgLat / 2000.0));
      const pScore = (0.6 * sRate) + (0.3 * cRate) + (0.1 * (1.0 - lPenalty));
      const newTrust = (0.7 * prevTrust) + (0.3 * pScore);
      prevTrust = newTrust;

      let pointState = 'TRUSTED';
      if (newTrust < 0.5) pointState = 'QUARANTINED';
      else if (newTrust < 0.8) pointState = 'SUSPICIOUS';

      const d = new Date(event.timestamp);
      const formattedTime = !isNaN(d.getTime())
        ? d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
        : `T+${idx + 1}`;

      points.push({
        index: idx + 1,
        time: formattedTime,
        timestamp: event.timestamp,
        score: parseFloat(newTrust.toFixed(4)),
        rawScore: newTrust,
        state: pointState,
        taskId: event.task_id,
        success: event.success ? 'SUCCESS' : 'FAILED',
        compliance: event.compliance_event || 'COMPLIANT',
        latency: event.latency_ms,
        pScore: parseFloat(pScore.toFixed(4)),
        agentDid: selectedDid,
      });
    });

    return points;
  })();

  const formatShortDid = (did) => {
    if (!did) return 'unknown';
    return did.length > 18 ? `${did.slice(0, 10)}...${did.slice(-6)}` : did;
  };

  // State color mapping
  const getStateColor = (state) => {
    switch (state) {
      case 'TRUSTED': return chartTheme.trusted;
      case 'SUSPICIOUS': return chartTheme.suspicious;
      case 'QUARANTINED': return chartTheme.quarantined;
      case 'REVOKED': return chartTheme.revoked;
      default: return chartTheme.accent;
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-[10px] font-mono text-tc-cyan uppercase tracking-widest mb-1">
            <Shield size={14} /> TRUSTCHAIN-AI OPERATIONS CENTER
          </div>
          <h1 className="text-2xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">
            TrustChain-AI
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5">
            AI Agent Trust & Security Operations Center
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded">
            <Server size={14} className={health.status === 'ok' ? 'text-emerald-500 dark:text-emerald-400' : 'text-rose-500'} />
            <span className="text-[10px] text-slate-700 dark:text-slate-300 font-mono tracking-widest uppercase">
              {health.status === 'ok' ? 'VDR DATABASE ONLINE' : 'VDR OFFLINE'}
            </span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded">
            <span className="w-2 h-2 rounded-full bg-emerald-500 dark:bg-emerald-400 animate-pulse shadow-[0_0_8px_#10b981]"></span>
            <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono tracking-widest uppercase">
              LIVE RECOVERY SYNC
            </span>
          </div>
        </div>
      </div>

      {/* Top Status Banner */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-3.5 rounded-lg flex flex-col sm:flex-row sm:items-center justify-between gap-2 font-mono text-xs text-slate-600 dark:text-slate-300">
        <div className="flex flex-wrap items-center gap-2">
          <CheckCircle2 size={16} className="text-emerald-500 dark:text-emerald-400 flex-shrink-0" />
          <span className="font-bold text-slate-900 dark:text-slate-100">SYSTEM OPERATIONAL</span>
          <span className="text-slate-400 dark:text-slate-600">|</span>
          <span className="text-slate-600 dark:text-slate-400">Trust Engine active</span>
          <span className="text-slate-400 dark:text-slate-600">•</span>
          <span className="text-slate-600 dark:text-slate-400">Agent Registry connected</span>
          <span className="text-slate-400 dark:text-slate-600">•</span>
          <span className="text-slate-600 dark:text-slate-400">Audit logging active</span>
        </div>
        <span className="text-[10px] text-tc-cyan font-bold uppercase tracking-widest">HTTP 200 OK</span>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { 
            label: 'TOTAL AGENTS', 
            value: stats.total, 
            sub: 'Registered fleet', 
            color: 'text-tc-cyan', 
            onClick: () => navigate('/agents') 
          },
          { 
            label: 'TRUSTED', 
            value: stats.trusted, 
            sub: `${stats.total ? ((stats.trusted / stats.total) * 100).toFixed(0) : 0}% of fleet`, 
            color: 'text-emerald-500 dark:text-emerald-400', 
            onClick: () => navigate('/agents') 
          },
          { 
            label: 'SUSPICIOUS', 
            value: stats.suspicious, 
            sub: `${stats.total ? ((stats.suspicious / stats.total) * 100).toFixed(0) : 0}% of fleet`, 
            color: 'text-amber-500 dark:text-amber-400', 
            onClick: () => navigate('/agents') 
          },
          { 
            label: 'QUARANTINED', 
            value: stats.quarantined, 
            sub: `${stats.total ? ((stats.quarantined / stats.total) * 100).toFixed(0) : 0}% of fleet`, 
            color: 'text-rose-500', 
            onClick: () => navigate('/agents') 
          },
          { 
            label: 'REVOKED', 
            value: stats.revoked, 
            sub: `${stats.total ? ((stats.revoked / stats.total) * 100).toFixed(0) : 0}% of fleet`, 
            color: 'text-slate-500', 
            onClick: () => navigate('/agents') 
          },
          { 
            label: 'AVG TRUST T(t)', 
            value: stats.avg, 
            sub: 'Excl. Revoked', 
            color: 'text-slate-900 dark:text-slate-100', 
            onClick: () => navigate('/analytics') 
          },
        ].map((stat, i) => (
          <div 
            key={i} 
            onClick={stat.onClick}
            className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-3.5 rounded-lg text-center cursor-pointer hover:border-tc-cyan/50 transition-all shadow-sm">
            <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono tracking-widest uppercase mb-1">
              {stat.label}
            </p>
            <h3 className={`text-2xl font-bold font-mono ${stat.color}`}>{stat.value}</h3>
            <p className="text-[9px] text-slate-400 dark:text-slate-500 font-mono mt-0.5">{stat.sub}</p>
          </div>
        ))}
      </div>

      {/* Main Trust Intelligence Section (Parts A & B) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dynamic Visualization: Historical Time-Series or Cross-Sectional Ranking */}
        <div className="lg:col-span-2 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 flex flex-col space-y-4 shadow-sm">
          {/* Header & Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Activity size={16} className="text-tc-cyan flex-shrink-0" />
              <div>
                <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
                  Trust Intelligence Overview & Agent Posture
                </h3>
                <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {viewMode === 'trajectory' 
                    ? 'Individual Agent Historical EWMA Trust Score Trajectory Over Time' 
                    : 'Fleet Cross-Sectional Trust Score Comparison (Horizontal Bar)'}
                </p>
              </div>
            </div>

            {/* View Switcher Pills */}
            <div className="flex items-center gap-1.5 bg-slate-100 dark:bg-[#080b13] p-1 rounded-md border border-slate-200 dark:border-slate-800 font-mono text-[10px]">
              <button
                type="button"
                onClick={() => setViewMode('trajectory')}
                className={`px-2.5 py-1 rounded font-bold transition-colors ${
                  viewMode === 'trajectory'
                    ? 'bg-tc-cyan text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                }`}
              >
                Time-Series
              </button>
              <button
                type="button"
                onClick={() => setViewMode('ranking')}
                className={`px-2.5 py-1 rounded font-bold transition-colors ${
                  viewMode === 'ranking'
                    ? 'bg-tc-cyan text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                }`}
              >
                Fleet Ranking
              </button>
            </div>
          </div>

          {/* Sub-bar: Agent Selector (When in Time-Series Mode) */}
          {viewMode === 'trajectory' && (
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50 dark:bg-[#080b13] p-2.5 rounded border border-slate-200 dark:border-slate-800 text-xs font-mono">
              <div className="flex items-center gap-2 flex-1">
                <span className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest whitespace-nowrap">
                  TARGET AGENT:
                </span>
                <select
                  value={selectedDid}
                  onChange={(e) => setSelectedDid(e.target.value)}
                  className="bg-white dark:bg-[#0b101d] border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded px-2.5 py-1 text-xs font-mono focus:outline-none focus:border-tc-cyan flex-1 max-w-md shadow-sm"
                >
                  {agents.map((a) => {
                    const did = a.agent_did || a.did;
                    const name = a.agent_name || 'Agent';
                    return (
                      <option key={did} value={did}>
                        {name} ({did.slice(0, 12)}...{did.slice(-4)}) — [{a.trust_state || 'TRUSTED'} : {(a.trust_score ?? 1).toFixed(3)}]
                      </option>
                    );
                  })}
                </select>
              </div>

              {selectedAgent && (
                <div className="flex items-center gap-2 self-end sm:self-auto">
                  <span className="text-[10px] text-slate-500 dark:text-slate-400">CURRENT:</span>
                  <span className="font-bold text-slate-900 dark:text-slate-100">
                    {(selectedAgent.trust_score ?? 1).toFixed(4)}
                  </span>
                  <TrustBadge state={selectedAgent.trust_state || 'TRUSTED'} />
                </div>
              )}
            </div>
          )}

          {/* Main Chart Area */}
          <div className="h-72 w-full pt-1">
            {agents.length === 0 ? (
              <EmptyState message="No registered agents available for trust scoring visualization." />
            ) : viewMode === 'trajectory' ? (
              /* PART B: Individual Agent Time-Series Chart */
              loadingTelemetry ? (
                <LoadingState message="RETRIEVING AGENT HISTORICAL TELEMETRY..." />
              ) : timeSeriesData.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center p-6 text-center border border-dashed border-slate-300 dark:border-slate-800 rounded bg-slate-50/50 dark:bg-[#080b13]/40">
                  <Clock size={28} className="text-slate-400 mb-2 opacity-60" />
                  <p className="text-xs font-mono font-bold text-slate-700 dark:text-slate-300 mb-1">
                    NO HISTORICAL TELEMETRY EVENTS RECORDED YET
                  </p>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 max-w-md font-mono leading-relaxed mb-3">
                    Target agent has current baseline posture of{' '}
                    <strong className="text-tc-cyan">
                      {(selectedAgent?.trust_score ?? 1.0).toFixed(4)} ({selectedAgent?.trust_state || 'TRUSTED'})
                    </strong>
                    . Telemetry history will populate automatically as tasks execute or events are logged.
                  </p>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => navigate('/telemetry')}
                      className="px-3 py-1 bg-tc-cyan/10 border border-tc-cyan text-tc-cyan hover:bg-tc-cyan/20 rounded text-[10px] font-mono uppercase tracking-wider transition-colors"
                    >
                      Go to Telemetry Center
                    </button>
                    <button
                      type="button"
                      onClick={() => setViewMode('ranking')}
                      className="px-3 py-1 bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded text-[10px] font-mono uppercase tracking-wider hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors"
                    >
                      View Fleet Ranking
                    </button>
                  </div>
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timeSeriesData} margin={{ top: 12, right: 30, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                    <XAxis 
                      dataKey="time" 
                      stroke={chartTheme.text} 
                      fontSize={10} 
                      tickLine={false} 
                      axisLine={false} 
                      fontFamily="monospace"
                    />
                    <YAxis 
                      stroke={chartTheme.text} 
                      fontSize={10} 
                      domain={[0, 1]} 
                      ticks={[0, 0.25, 0.5, 0.75, 1.0]} 
                      tickLine={false} 
                      axisLine={false} 
                      fontFamily="monospace"
                    />
                    {/* Security Threshold Reference Lines */}
                    <ReferenceLine 
                      y={0.80} 
                      stroke={chartTheme.trusted} 
                      strokeDasharray="4 4" 
                      label={{ 
                        value: 'Trusted Threshold (0.80)', 
                        fill: chartTheme.trusted, 
                        fontSize: 9, 
                        position: 'top',
                        fontFamily: 'monospace'
                      }} 
                    />
                    <ReferenceLine 
                      y={0.50} 
                      stroke={chartTheme.quarantined} 
                      strokeDasharray="4 4" 
                      label={{ 
                        value: 'Quarantine Threshold (0.50)', 
                        fill: chartTheme.quarantined, 
                        fontSize: 9, 
                        position: 'top',
                        fontFamily: 'monospace'
                      }} 
                    />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (!active || !payload || !payload.length) return null;
                        const pt = payload[0].payload;
                        return (
                          <div 
                            style={{ 
                              backgroundColor: chartTheme.tooltipBg, 
                              borderColor: chartTheme.tooltipBorder, 
                              color: chartTheme.textPrimary 
                            }}
                            className="p-3 border rounded shadow-xl font-mono text-[11px] space-y-1.5 min-w-[210px]"
                          >
                            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-1">
                              <span className="font-bold text-tc-cyan">OBSERVATION #{pt.index}</span>
                              <span className="text-[10px] text-slate-500">{pt.time}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-slate-500">Trust Score T(t):</span>
                              <span className="font-bold text-slate-900 dark:text-slate-100">{pt.score.toFixed(4)}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-slate-500">Resulting State:</span>
                              <span className="font-bold" style={{ color: getStateColor(pt.state) }}>{pt.state}</span>
                            </div>
                            <div className="pt-1 border-t border-slate-200 dark:border-slate-800 text-[10px] space-y-0.5 text-slate-600 dark:text-slate-400">
                              <div>Task: <span className="font-bold">{pt.taskId}</span></div>
                              <div>Execution: <span className={pt.success === 'SUCCESS' ? 'text-emerald-500' : 'text-rose-500 font-bold'}>{pt.success}</span></div>
                              <div>Protocol: <span>{pt.compliance}</span></div>
                              <div>Latency: <span>{pt.latency} ms</span></div>
                            </div>
                          </div>
                        );
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="score" 
                      stroke={chartTheme.accent} 
                      strokeWidth={2.5} 
                      dot={{ r: 4, fill: chartTheme.bg, stroke: chartTheme.accent, strokeWidth: 2 }} 
                      activeDot={{ r: 6, fill: chartTheme.accent }} 
                      name="Trust Score T(t)" 
                    />
                  </LineChart>
                </ResponsiveContainer>
              )
            ) : (
              /* PART B ALTERNATIVE: Cross-Sectional Ranking (Horizontal Bar Chart) */
              <ResponsiveContainer width="100%" height="100%">
                <BarChart 
                  layout="vertical" 
                  data={rankingData} 
                  margin={{ top: 10, right: 30, left: 10, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} horizontal={false} />
                  <XAxis 
                    type="number" 
                    domain={[0, 1]} 
                    ticks={[0, 0.25, 0.5, 0.75, 1.0]} 
                    stroke={chartTheme.text} 
                    fontSize={10} 
                    tickLine={false} 
                    axisLine={false}
                    fontFamily="monospace"
                  />
                  <YAxis 
                    type="category" 
                    dataKey="name" 
                    stroke={chartTheme.text} 
                    fontSize={10} 
                    tickLine={false} 
                    axisLine={false}
                    width={110}
                    fontFamily="monospace"
                  />
                  <ReferenceLine 
                    x={0.80} 
                    stroke={chartTheme.trusted} 
                    strokeDasharray="4 4" 
                    label={{ value: '0.80', fill: chartTheme.trusted, fontSize: 9, position: 'top', fontFamily: 'monospace' }} 
                  />
                  <ReferenceLine 
                    x={0.50} 
                    stroke={chartTheme.quarantined} 
                    strokeDasharray="4 4" 
                    label={{ value: '0.50', fill: chartTheme.quarantined, fontSize: 9, position: 'top', fontFamily: 'monospace' }} 
                  />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (!active || !payload || !payload.length) return null;
                      const d = payload[0].payload;
                      return (
                        <div 
                          style={{ 
                            backgroundColor: chartTheme.tooltipBg, 
                            borderColor: chartTheme.tooltipBorder, 
                            color: chartTheme.textPrimary 
                          }}
                          className="p-2.5 border rounded shadow-xl font-mono text-xs space-y-1 min-w-[200px]"
                        >
                          <div className="font-bold text-tc-cyan">{d.name}</div>
                          <div className="text-[10px] text-slate-500 truncate" title={d.did}>{d.did}</div>
                          <div className="flex justify-between items-center pt-1 border-t border-slate-200 dark:border-slate-800">
                            <span className="text-slate-500">Trust Score:</span>
                            <span className="font-bold font-mono">{d.score.toFixed(4)}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-slate-500">Trust State:</span>
                            <span className="font-bold" style={{ color: getStateColor(d.state) }}>{d.state}</span>
                          </div>
                        </div>
                      );
                    }}
                  />
                  <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                    {rankingData.map((entry, index) => (
                      <Cell key={`bar-${index}`} fill={getStateColor(entry.state)} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Mathematical & Threshold Footer Legend */}
          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 dark:border-slate-800 pt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span>
                <span>TRUSTED (&ge; 0.80)</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-amber-500"></span>
                <span>SUSPICIOUS (0.50 - 0.79)</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-rose-500"></span>
                <span>QUARANTINED (&lt; 0.50)</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-slate-500"></span>
                <span>REVOKED</span>
              </span>
            </div>
            <div className="text-tc-cyan">
              Formula: T(t) = 0.70 &middot; T(t-1) + 0.30 &middot; P(t)
            </div>
          </div>
        </div>

        {/* Part A: Fleet Trust Distribution & Posture Breakdown */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 flex flex-col space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <ShieldAlert size={14} className="text-tc-cyan" /> Fleet Trust Distribution
            </h3>
            <span className="text-[10px] font-mono text-tc-cyan font-bold">
              {stats.total ? ((stats.trusted / stats.total) * 100).toFixed(0) : 0}% HEALTHY
            </span>
          </div>

          {/* Donut Chart with Center Metric */}
          <div className="h-44 w-full relative flex items-center justify-center">
            {pieData.length === 0 ? (
              <EmptyState message="No agents in registry" />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={46}
                    outerRadius={68}
                    paddingAngle={3}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`slice-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (!active || !payload || !payload.length) return null;
                      const d = payload[0];
                      const pct = stats.total ? ((d.value / stats.total) * 100).toFixed(1) : '0.0';
                      return (
                        <div 
                          style={{ 
                            backgroundColor: chartTheme.tooltipBg, 
                            borderColor: chartTheme.tooltipBorder, 
                            color: chartTheme.textPrimary 
                          }}
                          className="p-2 border rounded shadow-md font-mono text-xs"
                        >
                          <span className="font-bold" style={{ color: d.payload.color }}>{d.name}</span>: {d.value} agents ({pct}%)
                        </div>
                      );
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            )}

            {/* Center Label inside Donut */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-100">
                {stats.total}
              </span>
              <span className="text-[9px] font-mono uppercase tracking-widest text-slate-500">
                TOTAL
              </span>
            </div>
          </div>

          {/* Detailed State Breakdown Rows */}
          <div className="space-y-2.5 font-mono text-xs pt-1 border-t border-slate-200 dark:border-slate-800">
            {[
              { 
                label: 'TRUSTED', 
                count: stats.trusted, 
                color: chartTheme.trusted, 
                barBg: 'bg-emerald-500', 
                pct: stats.total ? (stats.trusted / stats.total) * 100 : 0,
                desc: 'Unrestricted execution & collaboration' 
              },
              { 
                label: 'SUSPICIOUS', 
                count: stats.suspicious, 
                color: chartTheme.suspicious, 
                barBg: 'bg-amber-500', 
                pct: stats.total ? (stats.suspicious / stats.total) * 100 : 0,
                desc: 'Monitored with stepped verification' 
              },
              { 
                label: 'QUARANTINED', 
                count: stats.quarantined, 
                color: chartTheme.quarantined, 
                barBg: 'bg-rose-500', 
                pct: stats.total ? (stats.quarantined / stats.total) * 100 : 0,
                desc: 'Privileges suspended; recovery required' 
              },
              { 
                label: 'REVOKED', 
                count: stats.revoked, 
                color: chartTheme.revoked, 
                barBg: 'bg-slate-500', 
                pct: stats.total ? (stats.revoked / stats.total) * 100 : 0,
                desc: 'Permanently blocked; non-recoverable' 
              },
            ].map((st, i) => (
              <div key={i} className="space-y-1">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-bold flex items-center gap-1.5" style={{ color: st.color }}>
                    <span className={`w-2 h-2 rounded-full ${st.barBg}`}></span>
                    {st.label}
                  </span>
                  <span className="text-slate-600 dark:text-slate-400 font-mono">
                    <strong className="text-slate-900 dark:text-slate-100">{st.count}</strong> ({st.pct.toFixed(1)}%)
                  </span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 dark:bg-slate-800 rounded overflow-hidden">
                  <div className={`h-full ${st.barBg} transition-all duration-500`} style={{ width: `${st.pct}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Security Events Stream & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Security Events Stream */}
        <div className="lg:col-span-2 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 flex flex-col space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <GitMerge size={14} className="text-tc-cyan" /> Recent Security Events & Audits
            </h3>
            <button
              type="button"
              onClick={() => navigate('/audit')}
              className="text-[10px] font-mono text-tc-cyan hover:underline flex items-center gap-1 uppercase tracking-wider"
            >
              View Full Audit Trail <ArrowRight size={10} />
            </button>
          </div>

          {audits.length === 0 ? (
            <EmptyState message="No audit trail events logged yet." />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[320px] overflow-y-auto custom-scrollbar pr-1">
              {audits.slice(0, 6).map((a) => (
                <div 
                  key={a.id} 
                  className="bg-slate-50 dark:bg-[#080b13] border border-slate-200 dark:border-slate-800 p-3 rounded font-mono text-xs space-y-1.5 shadow-sm"
                >
                  <div className="flex justify-between items-center text-[10px] text-slate-500">
                    <span>{new Date(a.timestamp).toLocaleTimeString()}</span>
                    <span className="text-tc-cyan font-bold truncate max-w-[130px]" title={a.agent_did}>
                      {formatShortDid(a.agent_did)}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 text-xs">
                    <span className="text-slate-500 dark:text-slate-400 font-semibold">{a.previous_state}</span>
                    <span className="text-tc-cyan font-bold">&rarr;</span>
                    <span 
                      className="font-bold"
                      style={{ color: getStateColor(a.new_state) }}
                    >
                      {a.new_state}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-600 dark:text-slate-400 truncate" title={a.reason}>
                    {a.reason}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Operations & Navigation Shortcuts */}
        <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 flex flex-col justify-between space-y-4 shadow-sm font-mono text-xs">
          <div className="border-b border-slate-200 dark:border-slate-800 pb-3">
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <Lock size={14} className="text-tc-cyan" /> Adaptive Security Gateway
            </h3>
            <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
              Zero-Trust Autonomous Governance Controls
            </p>
          </div>

          <div className="space-y-2">
            {[
              { title: 'Agent Registry & DID Inventory', path: '/agents', desc: 'Inspect did:key & Verifiable Credentials' },
              { title: 'Trust Analytics & EWMA Formulas', path: '/analytics', desc: 'View causal mathematical derivations' },
              { title: 'Multi-Agent Collaboration Center', path: '/collaboration', desc: 'Peer matching & session telemetry' },
              { title: 'Automated Workflow Center', path: '/workflows', desc: 'Sequential & parallel multi-agent pipelines' },
              { title: 'Zero-Trust Policy Visualizer', path: '/authorization', desc: 'Real-time adaptive RBAC/ABAC gateway' },
            ].map((nav, i) => (
              <div
                key={i}
                onClick={() => navigate(nav.path)}
                className="p-2.5 rounded bg-slate-50 dark:bg-[#080b13] border border-slate-200 dark:border-slate-800 hover:border-tc-cyan/50 cursor-pointer transition-colors flex items-center justify-between group"
              >
                <div>
                  <div className="font-bold text-slate-800 dark:text-slate-200 group-hover:text-tc-cyan transition-colors text-[11px]">
                    {nav.title}
                  </div>
                  <div className="text-[9px] text-slate-500 dark:text-slate-400">{nav.desc}</div>
                </div>
                <ChevronRight size={14} className="text-slate-400 group-hover:text-tc-cyan group-hover:translate-x-0.5 transition-all flex-shrink-0" />
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-slate-200 dark:border-slate-800 text-[10px] text-slate-500 flex items-center justify-between">
            <span>SOC Engine v2.0-Production</span>
            <span className="text-emerald-500 font-bold">100% Policy Enforced</span>
          </div>
        </div>
      </div>

      {/* Architectural Flow Visual */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-5 rounded-lg space-y-3 font-mono shadow-sm">
        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest border-b border-slate-200 dark:border-slate-800 pb-2 flex items-center justify-between">
          <span>TRUSTCHAIN-AI ADAPTIVE ARCHITECTURAL GOVERNANCE FLOW</span>
          <span className="text-tc-cyan font-bold">END-TO-END PIPELINE</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-center text-xs">
          {[
            { step: '1. AGENT IDENTITY', detail: 'W3C did:key & VC' },
            { step: '2. TELEMETRY', detail: 'Success, Compliance, Latency' },
            { step: '3. TRUST ENGINE', detail: 'EWMA Score T(t)' },
            { step: '4. TRUST STATE', detail: 'Trusted / Quarantine' },
            { step: '5. AUTHORIZATION', detail: 'Adaptive Policy Check' },
            { step: '6. AUDIT TRAIL', detail: 'Immutable Event Log' },
          ].map((item, idx) => (
            <div 
              key={idx} 
              className="bg-slate-50 dark:bg-[#080b13] border border-slate-200 dark:border-slate-800 p-3 rounded flex flex-col items-center justify-center"
            >
              <span className="font-bold text-tc-cyan text-[11px] mb-0.5">{item.step}</span>
              <span className="text-[9px] text-slate-500 dark:text-slate-400">{item.detail}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
