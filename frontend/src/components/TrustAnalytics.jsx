import React, { useState } from 'react';
import { 
  Activity, Zap, ArrowUpDown, Filter, Shield, CheckCircle2, 
  AlertTriangle, ShieldAlert, XCircle, Search, Info 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, ReferenceLine, Cell 
} from 'recharts';
import { useAgents } from '../hooks/useApi';
import { useTheme } from '../context/ThemeContext';
import { LoadingState, ErrorState, EmptyState, SectionHeader, TrustBadge } from './ui/States';

export default function TrustAnalytics() {
  const { data: agents, loading, error } = useAgents();
  const { isDark, chartTheme } = useTheme();

  const [sortBy, setSortBy] = useState('score_desc');
  const [stateFilter, setStateFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  if (loading) return <LoadingState message="COMPILING TRUST INTELLIGENCE ENGINE ANALYTICS..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;

  const allAgents = agents || [];

  // Active agents (excluding REVOKED) for trust score average calculation
  const activeAgents = allAgents.filter((a) => a.trust_state !== 'REVOKED');
  const stats = {
    total: allAgents.length,
    trusted: allAgents.filter((a) => a.trust_state === 'TRUSTED').length,
    suspicious: allAgents.filter((a) => a.trust_state === 'SUSPICIOUS').length,
    quarantined: allAgents.filter((a) => a.trust_state === 'QUARANTINED').length,
    revoked: allAgents.filter((a) => a.trust_state === 'REVOKED').length,
    avgTrust: activeAgents.length
      ? (activeAgents.reduce((sum, a) => sum + (a.trust_score || 0), 0) / activeAgents.length).toFixed(4)
      : '0.0000',
  };

  // State order mapping for sorting
  const stateWeight = { TRUSTED: 4, SUSPICIOUS: 3, QUARANTINED: 2, REVOKED: 1, UNKNOWN: 0 };

  // Filter & Sort for Cross-Sectional Bar Chart
  let chartList = allAgents.map((a) => {
    const did = a.did || a.agent_did || 'unknown';
    const shortDid = did.length > 16 ? `...${did.slice(-8)}` : did;
    const displayName = a.agent_name ? `${a.agent_name} (${shortDid})` : shortDid;
    return {
      agent_name: a.agent_name || 'Agent',
      full_did: did,
      short_did: shortDid,
      displayName,
      score: typeof a.trust_score === 'number' ? a.trust_score : parseFloat(a.trust_score) || 0,
      state: (a.trust_state || 'TRUSTED').toUpperCase(),
      last_updated: a.last_updated || a.last_active_at || null,
    };
  });

  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    chartList = chartList.filter(
      (a) => a.agent_name.toLowerCase().includes(q) || a.full_did.toLowerCase().includes(q)
    );
  }

  if (stateFilter !== 'ALL') {
    chartList = chartList.filter((a) => a.state === stateFilter);
  }

  chartList.sort((a, b) => {
    switch (sortBy) {
      case 'score_desc':
        return b.score - a.score;
      case 'score_asc':
        return a.score - b.score;
      case 'name_asc':
        return a.agent_name.localeCompare(b.agent_name);
      case 'state':
        return (stateWeight[b.state] || 0) - (stateWeight[a.state] || 0) || b.score - a.score;
      default:
        return b.score - a.score;
    }
  });

  const getBarColor = (state) => {
    switch (state) {
      case 'TRUSTED':
        return chartTheme.trusted;
      case 'SUSPICIOUS':
        return chartTheme.suspicious;
      case 'QUARANTINED':
        return chartTheme.quarantined;
      case 'REVOKED':
        return chartTheme.revoked;
      default:
        return chartTheme.accent;
    }
  };

  const dynamicChartHeight = Math.max(300, chartList.length * 48);

  const CustomBarTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div
          className="p-3.5 rounded-lg border font-mono text-xs shadow-2xl space-y-1.5"
          style={{
            backgroundColor: chartTheme.tooltipBg,
            borderColor: chartTheme.tooltipBorder,
            color: chartTheme.textPrimary,
          }}
        >
          <div className="font-bold text-sm text-cyan-400">{data.agent_name}</div>
          <div className="text-[11px] opacity-75 break-all max-w-xs">{data.full_did}</div>
          <div className="border-t border-slate-700/60 pt-1.5 flex items-center justify-between gap-4">
            <span className="text-slate-400">Trust Score T(t):</span>
            <span className="font-bold text-sm" style={{ color: getBarColor(data.state) }}>
              {data.score.toFixed(4)}
            </span>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-slate-400">Trust State:</span>
            <TrustBadge state={data.state} />
          </div>
          <div className="text-[10px] text-slate-500 pt-0.5">
            {data.state === 'TRUSTED' && 'Access Level: Full (Standard & Privileged)'}
            {data.state === 'SUSPICIOUS' && 'Access Level: Restricted (Privileged Denied)'}
            {data.state === 'QUARANTINED' && 'Access Level: HTTP 403 Forbidden'}
            {data.state === 'REVOKED' && 'Access Level: Administratively Terminated'}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans">
      <SectionHeader
        icon={Activity}
        title="Trust Intelligence Engine & Mathematical Posture"
        subtitle="Dynamic behavioral trust scoring, Exponentially Weighted Moving Average (EWMA) decay, and state boundary enforcement."
        badge="MATH MODEL ACTIVE"
      />

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">TOTAL AGENTS</p>
          <h3 className="text-2xl font-bold font-mono text-tc-cyan">{stats.total}</h3>
        </div>
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">TRUSTED</p>
          <h3 className="text-2xl font-bold font-mono text-emerald-400">{stats.trusted}</h3>
        </div>
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">SUSPICIOUS</p>
          <h3 className="text-2xl font-bold font-mono text-amber-400">{stats.suspicious}</h3>
        </div>
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">QUARANTINED</p>
          <h3 className="text-2xl font-bold font-mono text-rose-500">{stats.quarantined}</h3>
        </div>
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">REVOKED</p>
          <h3 className="text-2xl font-bold font-mono text-slate-500">{stats.revoked}</h3>
        </div>
        <div className="bg-[#0b101d] border border-slate-800 p-4 rounded-lg text-center shadow-sm">
          <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase mb-1">AVG TRUST T(t)</p>
          <h3 className="text-2xl font-bold font-mono text-slate-100">{stats.avgTrust}</h3>
          <span className="text-[8px] text-slate-500 block">Excl. Revoked</span>
        </div>
      </div>

      {/* Prominent Research Math Model Display Card */}
      <div className="bg-[#0b101d] border border-slate-800 p-6 rounded-lg space-y-4 font-mono shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-tc-cyan flex items-center gap-2">
            <Zap size={14} /> TrustChain-AI Mathematical Formulation
          </h3>
          <span className="text-[10px] text-slate-400">EWMA DECAY MODEL (&lambda; = 0.70)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          {/* Formulation Column 1 */}
          <div className="bg-[#080b13] border border-slate-800 p-4 rounded-lg space-y-2">
            <div className="text-[10px] text-slate-400 uppercase tracking-widest">
              Instantaneous Behavioral Score Pᵢ(t)
            </div>
            <div className="text-sm font-bold text-slate-100 bg-[#0b101d] p-3 rounded border border-slate-800/80">
              Pᵢ(t) = 0.6 &middot; Sᵢ(t) + 0.3 &middot; Cᵢ(t) + 0.1 &middot; (1 &minus; Lᵢ(t))
            </div>
            <div className="text-[10px] text-slate-400 space-y-0.5 pt-1">
              <p>&bull; Sᵢ(t): Task Success Rate (w₁ = 0.6)</p>
              <p>&bull; Cᵢ(t): Protocol Compliance (w₂ = 0.3)</p>
              <p>&bull; Lᵢ(t): Normalized Latency Penalty (w₃ = 0.1, max 2000ms)</p>
            </div>
          </div>

          {/* Formulation Column 2 */}
          <div className="bg-[#080b13] border border-slate-800 p-4 rounded-lg space-y-2">
            <div className="text-[10px] text-slate-400 uppercase tracking-widest">
              Temporal Trust Score Tᵢ(t) (EWMA Update)
            </div>
            <div className="text-sm font-bold text-tc-cyan bg-[#0b101d] p-3 rounded border border-slate-800/80">
              Tᵢ(t) = 0.7 &middot; Tᵢ(t&minus;1) + 0.3 &middot; Pᵢ(t)
            </div>
            <div className="text-[10px] text-slate-400 space-y-0.5 pt-1">
              <p>&bull; &lambda; = 0.7: Historical Memory Retention</p>
              <p>&bull; 1 &minus; &lambda; = 0.3: Instantaneous Weight</p>
              <p>&bull; T₀ = 1.0000: Initial Baseline Trust Score</p>
            </div>
          </div>
        </div>

        {/* State Threshold Boundaries */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 text-xs">
          <div className="bg-emerald-950/40 border border-emerald-800/60 p-3 rounded text-center">
            <div className="text-[10px] text-emerald-400 font-bold uppercase mb-1">TRUSTED STATE</div>
            <div className="text-sm font-bold text-slate-100">T(t) &ge; 0.80</div>
            <div className="text-[9px] text-emerald-400/80 mt-1">Full Access Granted</div>
          </div>
          <div className="bg-amber-950/40 border border-amber-800/60 p-3 rounded text-center">
            <div className="text-[10px] text-amber-400 font-bold uppercase mb-1">SUSPICIOUS STATE</div>
            <div className="text-sm font-bold text-slate-100">0.50 &le; T(t) &lt; 0.80</div>
            <div className="text-[9px] text-amber-400/80 mt-1">Privileged Denied / Monitored</div>
          </div>
          <div className="bg-rose-950/40 border border-rose-800/60 p-3 rounded text-center">
            <div className="text-[10px] text-rose-400 font-bold uppercase mb-1">QUARANTINED STATE</div>
            <div className="text-sm font-bold text-slate-100">T(t) &lt; 0.50</div>
            <div className="text-[9px] text-rose-400/80 mt-1">HTTP 403 Policy Block</div>
          </div>
          <div className="bg-slate-900 border border-slate-700 p-3 rounded text-center">
            <div className="text-[10px] text-slate-400 font-bold uppercase mb-1">REVOKED STATE</div>
            <div className="text-sm font-bold text-slate-300">ADMINISTRATIVE</div>
            <div className="text-[9px] text-slate-500 mt-1">Permanent Denial</div>
          </div>
        </div>
      </div>

      {/* Cross-Sectional Agent Trust Scores (Redesigned Bar Chart - No connecting lines) */}
      <div className="bg-[#0b101d] border border-slate-800 p-6 rounded-lg space-y-4 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-xs font-mono font-bold tracking-widest text-slate-100 uppercase flex items-center gap-2">
              <Activity size={15} className="text-tc-cyan" />
              Cross-Sectional Agent Trust Scores
            </h3>
            <p className="text-[11px] text-slate-400 font-mono mt-0.5">
              Discrete agent trust distribution. Independent scores with 0.80 & 0.50 policy boundaries.
            </p>
          </div>

          {/* Controls: Search, Sort, Filter */}
          <div className="flex flex-wrap items-center gap-2.5">
            <div className="relative">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500" size={12} />
              <input
                type="text"
                placeholder="Filter agent..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-[#080b13] border border-slate-700 rounded text-[11px] font-mono text-slate-200 py-1.5 pl-8 pr-2.5 focus:outline-none focus:border-tc-cyan w-36 sm:w-44 shadow-inner"
              />
            </div>

            <div className="flex items-center gap-1.5 bg-[#080b13] border border-slate-700 rounded px-2 py-1">
              <Filter size={11} className="text-slate-400" />
              <select
                value={stateFilter}
                onChange={(e) => setStateFilter(e.target.value)}
                className="bg-transparent text-[11px] font-mono text-slate-200 focus:outline-none cursor-pointer"
              >
                <option value="ALL">All States ({allAgents.length})</option>
                <option value="TRUSTED">TRUSTED ({stats.trusted})</option>
                <option value="SUSPICIOUS">SUSPICIOUS ({stats.suspicious})</option>
                <option value="QUARANTINED">QUARANTINED ({stats.quarantined})</option>
                <option value="REVOKED">REVOKED ({stats.revoked})</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 bg-[#080b13] border border-slate-700 rounded px-2 py-1">
              <ArrowUpDown size={11} className="text-slate-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-transparent text-[11px] font-mono text-slate-200 focus:outline-none cursor-pointer"
              >
                <option value="score_desc">Trust Score (High &rarr; Low)</option>
                <option value="score_asc">Trust Score (Low &rarr; High)</option>
                <option value="name_asc">Agent Name (A &rarr; Z)</option>
                <option value="state">Trust State Priority</option>
              </select>
            </div>
          </div>
        </div>

        {chartList.length === 0 ? (
          <EmptyState message="No registered agents match the current filter criteria." />
        ) : (
          <div className="space-y-2">
            {/* Legend & Threshold Guide */}
            <div className="flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-400 px-2 py-1 bg-[#080b13] border border-slate-800/80 rounded">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span> TRUSTED (&ge; 0.80)
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-sm bg-amber-500"></span> SUSPICIOUS (0.50 - 0.79)
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-sm bg-rose-500"></span> QUARANTINED (&lt; 0.50)
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-sm bg-slate-500"></span> REVOKED (Terminal)
                </span>
              </div>
              <span className="text-[10px] text-slate-500">Showing {chartList.length} of {allAgents.length} agents</span>
            </div>

            {/* Scrollable Container for Agents Bar Chart */}
            <div className="max-h-[520px] overflow-y-auto custom-scrollbar pr-2 border border-slate-800/50 rounded-lg p-2 bg-[#080b13]/40">
              <div style={{ height: `${dynamicChartHeight}px`, width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    layout="vertical"
                    data={chartList}
                    margin={{ top: 20, right: 60, left: 140, bottom: 20 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} horizontal={false} />
                    <XAxis
                      type="number"
                      domain={[0, 1]}
                      tickCount={6}
                      stroke={chartTheme.text}
                      fontSize={11}
                      fontFamily="monospace"
                      tickFormatter={(val) => val.toFixed(2)}
                    />
                    <YAxis
                      type="category"
                      dataKey="displayName"
                      stroke={chartTheme.text}
                      fontSize={11}
                      fontFamily="monospace"
                      width={130}
                      tickLine={false}
                    />
                    <Tooltip content={<CustomBarTooltip />} />

                    {/* Policy Threshold Lines */}
                    <ReferenceLine
                      x={0.8}
                      stroke={chartTheme.trusted}
                      strokeDasharray="4 4"
                      strokeWidth={1.5}
                      label={{
                        position: 'top',
                        value: 'TRUSTED (0.80)',
                        fill: chartTheme.trusted,
                        fontSize: 10,
                        fontFamily: 'monospace',
                        fontWeight: 'bold',
                      }}
                    />
                    <ReferenceLine
                      x={0.5}
                      stroke={chartTheme.quarantined}
                      strokeDasharray="4 4"
                      strokeWidth={1.5}
                      label={{
                        position: 'top',
                        value: 'QUARANTINE (0.50)',
                        fill: chartTheme.quarantined,
                        fontSize: 10,
                        fontFamily: 'monospace',
                        fontWeight: 'bold',
                      }}
                    />

                    <Bar
                      dataKey="score"
                      radius={[0, 4, 4, 0]}
                      barSize={18}
                      label={{
                        position: 'right',
                        formatter: (val) => Number(val).toFixed(4),
                        fill: chartTheme.textPrimary,
                        fontSize: 10,
                        fontFamily: 'monospace',
                      }}
                    >
                      {chartList.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getBarColor(entry.state)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Trust Calculation Pipeline Visual */}
      <div className="bg-[#0b101d] border border-slate-800 p-6 rounded-lg space-y-4 font-mono text-xs shadow-xl">
        <div className="text-[10px] text-slate-400 uppercase tracking-widest border-b border-slate-800 pb-2">
          TRUST CALCULATION & GOVERNANCE PIPELINE
        </div>
        <div className="flex flex-col md:flex-row items-center justify-between gap-3 text-center">
          <div className="bg-[#080b13] border border-slate-800 p-3 rounded flex-1 w-full">
            <span className="text-tc-cyan font-bold block mb-1">Signals (S, C, L)</span>
            <span className="text-[10px] text-slate-400">Success, Compliance, Latency</span>
          </div>
          <span className="text-tc-cyan font-bold">&rarr;</span>
          <div className="bg-[#080b13] border border-slate-800 p-3 rounded flex-1 w-full">
            <span className="text-tc-cyan font-bold block mb-1">Behavioral Pᵢ(t)</span>
            <span className="text-[10px] text-slate-400">Weighted Performance</span>
          </div>
          <span className="text-tc-cyan font-bold">&rarr;</span>
          <div className="bg-[#080b13] border border-slate-800 p-3 rounded flex-1 w-full">
            <span className="text-tc-cyan font-bold block mb-1">Temporal Tᵢ(t)</span>
            <span className="text-[10px] text-slate-400">EWMA Score Update</span>
          </div>
          <span className="text-tc-cyan font-bold">&rarr;</span>
          <div className="bg-[#080b13] border border-slate-800 p-3 rounded flex-1 w-full">
            <span className="text-tc-cyan font-bold block mb-1">Trust State</span>
            <span className="text-[10px] text-slate-400">Trusted / Quarantined</span>
          </div>
          <span className="text-tc-cyan font-bold">&rarr;</span>
          <div className="bg-[#080b13] border border-slate-800 p-3 rounded flex-1 w-full">
            <span className="text-tc-cyan font-bold block mb-1">Adaptive Policy</span>
            <span className="text-[10px] text-slate-400">HTTP 200 / 403 Access</span>
          </div>
        </div>
      </div>
    </div>
  );
}
