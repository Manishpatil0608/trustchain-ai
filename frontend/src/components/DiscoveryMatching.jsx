import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Sliders, CheckCircle2, ShieldAlert, Cpu, Zap, Star, Filter } from 'lucide-react';
import { SectionHeader, TrustBadge, HealthBadge, StatusBadge, LoadingState, ErrorState, EmptyState } from './ui/States';

const API_BASE = 'http://localhost:8050/api/v1';

export default function DiscoveryMatching() {
  const [agents, setAgents] = useState([]);
  const [capabilityQuery, setCapabilityQuery] = useState('analysis');
  const [minTrustScore, setMinTrustScore] = useState(0.5);
  const [matchingResults, setMatchingResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDiscovery = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await axios.get(`${API_BASE}/registry/discover?capability=${encodeURIComponent(capabilityQuery)}`);
      setAgents(res.data);
    } catch (err) {
      setError(err.message || 'Failed to discover agents');
    } finally {
      setLoading(false);
    }
  };

  const handleMatch = async (e) => {
    if (e) e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      const res = await axios.post(`${API_BASE}/registry/matching`, {
        required_capability: capabilityQuery,
        min_trust_score: parseFloat(minTrustScore)
      });
      setMatchingResults(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Matching failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiscovery();
    handleMatch();
  }, [capabilityQuery]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <SectionHeader 
        icon={Search}
        title="Agent Discovery & Trust-Aware Matching"
        subtitle="Dynamic capability resolution, endpoint health evaluation, and transparent trust candidate ranking."
        badge="SECURITY POLICY FILTERED"
      />

      {/* Filter Controls Bar */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-5 rounded-lg space-y-4 shadow-sm">
        <div className="text-[10px] font-mono text-tc-cyan uppercase tracking-widest flex items-center gap-1.5 font-semibold">
          <Filter size={12} /> Candidate Discovery Criteria
        </div>
        <form onSubmit={handleMatch} className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Required Capability</label>
            <select 
              value={capabilityQuery}
              onChange={(e) => setCapabilityQuery(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs text-slate-900 dark:text-slate-200 font-mono outline-none focus:border-tc-cyan">
              <option value="analysis">Analysis & Reasoning</option>
              <option value="research">Research & Retrieval</option>
              <option value="coding">Coding & Implementation</option>
              <option value="planning">Execution Planning</option>
              <option value="verification">Verification & Security</option>
              <option value="compute">General Compute</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Min Trust Threshold T(t)</label>
            <input 
              type="number" step="0.05" min="0.0" max="1.0"
              value={minTrustScore}
              onChange={(e) => setMinTrustScore(e.target.value)}
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs text-slate-900 dark:text-slate-200 font-mono outline-none focus:border-tc-cyan"
            />
          </div>

          <div className="flex items-end">
            <button 
              type="submit"
              className="w-full bg-tc-cyan text-white dark:text-black py-2 rounded font-mono font-bold text-xs uppercase tracking-wider hover:bg-cyan-600 dark:hover:bg-cyan-300 transition-all shadow-[0_0_15px_rgba(0,240,255,0.2)]">
              Execute Trust-Aware Matching
            </button>
          </div>
        </form>
      </div>

      {/* Candidate Ranking Output Table */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-6 space-y-4 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
          <h3 className="text-xs font-mono font-bold uppercase text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Zap size={14} className="text-tc-cyan" /> Transparent Candidate Ranking & Security Decision Matrix
          </h3>
          <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Total Candidates Scored: {matchingResults.length}</span>
        </div>

        {loading ? (
          <LoadingState message="Evaluating Security Policies & Candidate Match Scores..." />
        ) : error ? (
          <ErrorState error={error} retry={handleMatch} />
        ) : matchingResults.length === 0 ? (
          <EmptyState message="No candidates found matching the specified capability criteria." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest bg-slate-50 dark:bg-[#080b13]">
                  <th className="p-3">Decision</th>
                  <th className="p-3">Agent Name</th>
                  <th className="p-3">DID</th>
                  <th className="p-3">Match Score</th>
                  <th className="p-3">Trust T(t)</th>
                  <th className="p-3">Reputation</th>
                  <th className="p-3">Health</th>
                  <th className="p-3">Policy Reason</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {matchingResults.map((cand, idx) => {
                  const isSelected = cand.decision === 'SELECTED';
                  const isRejectedPolicy = cand.decision.includes('POLICY') || cand.trust_state === 'QUARANTINED' || cand.trust_state === 'REVOKED';

                  return (
                    <tr key={idx} className={`hover:bg-slate-50 dark:hover:bg-[#121929]/80 transition-colors ${isSelected ? 'bg-sky-50 dark:bg-cyan-950/20 border-l-2 border-l-tc-cyan' : isRejectedPolicy ? 'bg-rose-50/50 dark:bg-rose-950/10' : ''}`}>
                      <td className="p-3 font-bold">
                        <span className={`px-2 py-0.5 rounded text-[9px] uppercase font-semibold ${isSelected ? 'bg-tc-cyan text-white dark:text-black' : isRejectedPolicy ? 'bg-rose-100 text-rose-800 border border-rose-300 dark:bg-rose-950 dark:text-rose-400 dark:border-rose-800' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'}`}>
                          {cand.decision}
                        </span>
                      </td>
                      <td className="p-3 font-bold text-slate-900 dark:text-slate-200">{cand.agent_name}</td>
                      <td className="p-3 text-slate-500 dark:text-slate-400 text-[10px] truncate max-w-[150px]" title={cand.did}>{cand.did}</td>
                      <td className="p-3 text-tc-cyan font-bold">{cand.match_score.toFixed(3)}</td>
                      <td className="p-3">
                        <TrustBadge state={cand.trust_state} />
                      </td>
                      <td className="p-3 text-amber-500 dark:text-amber-400 font-bold">{cand.reputation_score}/5.0</td>
                      <td className="p-3"><HealthBadge status={cand.health_status} /></td>
                      <td className="p-3 text-[10px] text-slate-600 dark:text-slate-400 max-w-[250px] truncate" title={cand.reason}>{cand.reason}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Transparent Match Score Math Card */}
      <div className="bg-slate-50 dark:bg-[#080b13] border border-slate-200 dark:border-slate-800 p-5 rounded-lg font-mono space-y-2 text-xs">
        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest border-b border-slate-200 dark:border-slate-800 pb-2">
          TRANSPARENT MATCHING EQUATION
        </div>
        <p className="text-tc-cyan font-semibold">
          MatchScore = 0.4 &middot; TrustScore + 0.3 &middot; (Reputation / 5.0) + 0.2 &middot; SuccessRate + 0.1 &middot; (1 &minus; LatencyPenalty)
        </p>
        <p className="text-slate-600 dark:text-slate-400 text-[11px]">
          * Note: Agents in QUARANTINED or REVOKED trust state fail the hard security boundary policy check and receive MatchScore = 0.0 with REJECTED status.
        </p>
      </div>
    </div>
  );
}
