import React, { useState, useEffect } from 'react';
import { 
  Search, Filter, Shield, Activity, CheckCircle2, AlertTriangle, 
  XCircle, ShieldAlert, Cpu, Layers, ExternalLink, RefreshCw, Sliders,
  Check, Copy, ArrowRight, UserCheck
} from 'lucide-react';
import { registryApi, trustApi } from '../api';
import { SectionHeader, TrustBadge, HealthBadge, StatusBadge, LoadingState, ErrorState, EmptyState } from './ui/States';
import AgentInvestigationDrawer from './AgentInvestigationDrawer';
import { Link } from 'react-router-dom';

export default function DiscoveryCenter() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [selectedCapability, setSelectedCapability] = useState('ALL');
  const [minTrustScore, setMinTrustScore] = useState(0.5);
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [selectedHealth, setSelectedHealth] = useState('ALL');
  const [showEligibleOnly, setShowEligibleOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Investigation drawer state
  const [investigatingDid, setInvestigatingDid] = useState(null);
  const [copiedDid, setCopiedDid] = useState(null);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await registryApi.getAgents();
      setAgents(Array.isArray(res) ? res : []);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to discover agents from registry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleCopy = (did) => {
    navigator.clipboard.writeText(did);
    setCopiedDid(did);
    setTimeout(() => setCopiedDid(null), 2000);
  };

  // Collect all unique capabilities
  const availableCapabilities = Array.from(new Set(
    agents.flatMap(a => (a.capabilities || '').split(',').map(c => c.trim().toLowerCase())).filter(Boolean)
  )).sort();

  // Evaluate eligibility for each agent based on filter rules
  const evaluatedAgents = agents.map(agent => {
    const caps = (agent.capabilities || '').toLowerCase().split(',').map(c => c.trim());
    const trustScore = agent.trust_score ?? 1.0;
    const trustState = (agent.trust_state || 'TRUSTED').toUpperCase();
    const opStatus = (agent.operational_status || 'AVAILABLE').toUpperCase();
    const healthStatus = (agent.health_status || 'HEALTHY').toUpperCase();

    // Capability check
    const matchesCapability = selectedCapability === 'ALL' || caps.includes(selectedCapability.toLowerCase());

    // Trust check
    const meetsTrustThreshold = trustScore >= minTrustScore;
    const isQuarantined = trustState === 'QUARANTINED';
    const isRevoked = trustState === 'REVOKED';

    // Status check
    const matchesStatus = selectedStatus === 'ALL' || opStatus === selectedStatus.toUpperCase();

    // Health check
    const matchesHealth = selectedHealth === 'ALL' || healthStatus === selectedHealth.toUpperCase();

    // Determine overall eligibility and primary exclusion reason
    let isEligible = false;
    let reason = '';
    let exclusionType = 'policy'; // 'policy' | 'threshold' | 'capability' | 'status' | 'health'

    if (isRevoked) {
      reason = 'Excluded: Administratively Revoked by security authority.';
      exclusionType = 'policy';
    } else if (isQuarantined) {
      reason = 'Excluded: Under behavioral quarantine (T < 0.50).';
      exclusionType = 'policy';
    } else if (!meetsTrustThreshold) {
      reason = `Excluded: Trust score (${trustScore.toFixed(3)}) is below minimum threshold (${minTrustScore.toFixed(2)}).`;
      exclusionType = 'threshold';
    } else if (!matchesCapability) {
      reason = `Excluded: Missing capability '${selectedCapability}'.`;
      exclusionType = 'capability';
    } else if (!matchesStatus) {
      reason = `Excluded: Operational status is ${opStatus}.`;
      exclusionType = 'status';
    } else if (!matchesHealth) {
      reason = `Excluded: Endpoint health is ${healthStatus}.`;
      exclusionType = 'health';
    } else {
      isEligible = true;
      reason = 'Eligible: Meets capability, trust threshold, operational status & health criteria.';
    }

    return {
      ...agent,
      isEligible,
      reason,
      exclusionType,
      parsedCapabilities: caps
    };
  });

  // Apply search query and eligible-only filter
  let displayedAgents = evaluatedAgents.filter(a => {
    if (showEligibleOnly && !a.isEligible) return false;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      const did = (a.did || a.agent_did || '').toLowerCase();
      const name = (a.agent_name || '').toLowerCase();
      const caps = (a.capabilities || '').toLowerCase();
      if (!did.includes(q) && !name.includes(q) && !caps.includes(q)) {
        return false;
      }
    }
    return true;
  });

  // Sort: Eligible first, then descending by trust score
  displayedAgents.sort((a, b) => {
    if (a.isEligible !== b.isEligible) {
      return a.isEligible ? -1 : 1;
    }
    return (b.trust_score ?? 0) - (a.trust_score ?? 0);
  });

  const totalEligible = evaluatedAgents.filter(a => a.isEligible).length;
  const totalExcluded = evaluatedAgents.length - totalEligible;

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-in fade-in duration-300 font-sans">
      <SectionHeader 
        icon={Search}
        title="Agent Capability Discovery & Availability Engine"
        subtitle="Search, filter, and discover verified autonomous agents based on registered capabilities, live health checks, and security trust policies."
        badge="INVENTORY DISCOVERY"
      />

      {/* Discovery Filter Controls Panel */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div className="text-xs font-mono font-bold text-slate-700 dark:text-slate-300 uppercase tracking-widest flex items-center gap-2">
            <Filter size={13} className="text-tc-cyan" /> Discovery Search & Eligibility Filters
          </div>
          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="text-slate-500">
              Eligible: <strong className="text-emerald-600 dark:text-emerald-400">{totalEligible}</strong>
            </span>
            <span className="text-slate-500">
              Excluded: <strong className="text-amber-600 dark:text-amber-400">{totalExcluded}</strong>
            </span>
            <button
              onClick={fetchAgents}
              className="p-1 rounded text-slate-400 hover:text-tc-cyan transition-colors"
              title="Refresh Registry"
            >
              <RefreshCw size={13} />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Capability Selector */}
          <div>
            <label className="block text-[11px] font-mono text-slate-500 uppercase mb-1">
              Required Capability
            </label>
            <select
              value={selectedCapability}
              onChange={(e) => setSelectedCapability(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
            >
              <option value="ALL">All Capabilities (Broad Search)</option>
              {availableCapabilities.map(cap => (
                <option key={cap} value={cap}>
                  {cap.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Minimum Trust Threshold Slider */}
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 uppercase mb-1">
              <span>Min Trust T(t)</span>
              <span className="font-bold text-tc-cyan">{Number(minTrustScore).toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={minTrustScore}
              onChange={(e) => setMinTrustScore(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-tc-cyan"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-400 mt-1">
              <span>0.0 (Open)</span>
              <span>0.5 (Quarantine)</span>
              <span>0.8 (Trusted)</span>
              <span>1.0</span>
            </div>
          </div>

          {/* Operational Status Filter */}
          <div>
            <label className="block text-[11px] font-mono text-slate-500 uppercase mb-1">
              Operational Availability
            </label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
            >
              <option value="ALL">All Statuses (Available, Busy, Offline)</option>
              <option value="AVAILABLE">AVAILABLE ONLY</option>
              <option value="BUSY">BUSY ONLY</option>
              <option value="OFFLINE">OFFLINE ONLY</option>
            </select>
          </div>

          {/* Endpoint Health Filter */}
          <div>
            <label className="block text-[11px] font-mono text-slate-500 uppercase mb-1">
              Endpoint Health Status
            </label>
            <select
              value={selectedHealth}
              onChange={(e) => setSelectedHealth(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
            >
              <option value="ALL">All Health States</option>
              <option value="HEALTHY">HEALTHY ONLY</option>
              <option value="UNHEALTHY">UNHEALTHY / SLOW</option>
              <option value="OFFLINE">OFFLINE / UNREACHABLE</option>
            </select>
          </div>
        </div>

        {/* Secondary Search & View Mode Toggles */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2 border-t border-slate-200 dark:border-slate-800/60 font-mono text-xs">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={13} />
            <input
              type="text"
              placeholder="Filter by agent name or DID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded py-1.5 pl-9 pr-3 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
            />
          </div>

          <label className="flex items-center gap-2 cursor-pointer text-slate-700 dark:text-slate-300 select-none">
            <input
              type="checkbox"
              checked={showEligibleOnly}
              onChange={(e) => setShowEligibleOnly(e.target.checked)}
              className="rounded border-slate-300 text-tc-cyan focus:ring-tc-cyan"
            />
            <span className="font-semibold text-xs">Show Eligible Agents Only ({totalEligible})</span>
          </label>
        </div>
      </div>

      {/* Discovered Agents Output */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-[#080b13]/50">
          <div className="flex items-center gap-2 font-mono text-xs font-bold text-slate-800 dark:text-slate-200 uppercase">
            <Cpu size={14} className="text-tc-cyan" /> Evaluated Candidates Roster
          </div>
          <span className="text-[10px] font-mono text-slate-500">
            Showing {displayedAgents.length} of {agents.length} agents
          </span>
        </div>

        {loading ? (
          <LoadingState message="Discovering registered agents and evaluating eligibility..." />
        ) : error ? (
          <ErrorState error={error} retry={fetchAgents} />
        ) : displayedAgents.length === 0 ? (
          <EmptyState message="No candidate agents meet the specified discovery and eligibility criteria." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-slate-50 dark:bg-[#080b13] text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="p-3.5 font-bold">Eligibility</th>
                  <th className="p-3.5 font-bold">Agent Identity</th>
                  <th className="p-3.5 font-bold">Capabilities</th>
                  <th className="p-3.5 font-bold text-center">Trust T(t)</th>
                  <th className="p-3.5 font-bold text-center">Posture</th>
                  <th className="p-3.5 font-bold text-center">Availability</th>
                  <th className="p-3.5 font-bold">Evaluation Rationale</th>
                  <th className="p-3.5 font-bold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {displayedAgents.map((agent) => {
                  const did = agent.did || agent.agent_did;
                  const isEligible = agent.isEligible;

                  return (
                    <tr 
                      key={did} 
                      className={`hover:bg-slate-50/80 dark:hover:bg-[#121929]/70 transition-colors ${
                        isEligible ? 'bg-emerald-50/20 dark:bg-emerald-950/5' : 'bg-slate-50/40 dark:bg-slate-900/20'
                      }`}
                    >
                      {/* Eligibility Status Pill */}
                      <td className="p-3.5">
                        {isEligible ? (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-400 dark:border-emerald-800/60 shadow-xs">
                            <CheckCircle2 size={12} /> ELIGIBLE
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-800/50">
                            <XCircle size={11} /> EXCLUDED
                          </span>
                        )}
                      </td>

                      {/* Agent Identity */}
                      <td className="p-3.5">
                        <div className="font-bold text-slate-900 dark:text-slate-100 text-xs">
                          {agent.agent_name || `Agent ${did.slice(0, 16)}...`}
                        </div>
                        <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 text-[10px] mt-0.5">
                          <span className="truncate max-w-[130px]" title={did}>{did}</span>
                          <button
                            onClick={() => handleCopy(did)}
                            className="text-slate-400 hover:text-tc-cyan transition-colors"
                            title="Copy DID"
                          >
                            {copiedDid === did ? <Check size={11} className="text-tc-success" /> : <Copy size={11} />}
                          </button>
                        </div>
                      </td>

                      {/* Capabilities */}
                      <td className="p-3.5">
                        <div className="flex flex-wrap gap-1 max-w-[180px]">
                          {agent.parsedCapabilities.map((cap, i) => {
                            const isMatch = selectedCapability !== 'ALL' && cap === selectedCapability.toLowerCase();
                            return (
                              <span
                                key={i}
                                className={`px-1.5 py-0.5 rounded text-[9px] uppercase font-semibold border ${
                                  isMatch
                                    ? 'bg-tc-cyan/20 text-cyan-800 dark:text-tc-cyan border-tc-cyan/60 font-bold'
                                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                                }`}
                              >
                                {cap}
                              </span>
                            );
                          })}
                        </div>
                      </td>

                      {/* Trust Score */}
                      <td className="p-3.5 text-center font-bold text-sm">
                        <span className={agent.trust_score >= 0.8 ? 'text-tc-success' : agent.trust_score >= 0.5 ? 'text-tc-warning' : 'text-tc-danger'}>
                          {(agent.trust_score ?? 1.0).toFixed(3)}
                        </span>
                      </td>

                      {/* Posture & State */}
                      <td className="p-3.5 text-center">
                        <TrustBadge state={agent.trust_state} />
                      </td>

                      {/* Availability & Health */}
                      <td className="p-3.5 text-center">
                        <div className="flex flex-col items-center gap-1">
                          <StatusBadge status={agent.operational_status} />
                          <HealthBadge status={agent.health_status} />
                        </div>
                      </td>

                      {/* Rationale Explanation */}
                      <td className="p-3.5 text-[11px] max-w-[220px]">
                        <span className={isEligible ? 'text-emerald-700 dark:text-emerald-300' : 'text-rose-600 dark:text-rose-400'}>
                          {agent.reason}
                        </span>
                      </td>

                      {/* Action Buttons */}
                      <td className="p-3.5 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => setInvestigatingDid(did)}
                            className="px-2.5 py-1 text-[11px] font-mono rounded border border-slate-300 dark:border-slate-700 hover:border-tc-cyan hover:text-tc-cyan text-slate-700 dark:text-slate-300 transition-colors shadow-xs"
                            title="Investigate Full Details"
                          >
                            Investigate
                          </button>
                          {isEligible && (
                            <Link
                              to={`/collaboration`}
                              className="px-2.5 py-1 text-[11px] font-mono rounded bg-tc-cyan text-white dark:text-black font-bold uppercase tracking-wider hover:opacity-90 transition-opacity flex items-center gap-1"
                              title="Engage in Collaboration Session"
                            >
                              Engage <ArrowRight size={11} />
                            </Link>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Investigation Drawer Integration */}
      {investigatingDid && (
        <AgentInvestigationDrawer
          did={investigatingDid}
          onClose={() => setInvestigatingDid(null)}
          onRefreshList={fetchAgents}
        />
      )}
    </div>
  );
}
