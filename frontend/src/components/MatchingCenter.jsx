import React, { useState, useEffect } from 'react';
import { 
  Sliders, Zap, Award, CheckCircle2, ShieldAlert, Cpu, AlertTriangle, 
  ChevronDown, ChevronUp, ArrowRight, Shield, RefreshCw, Copy, Check, Info, FileText
} from 'lucide-react';
import { registryApi } from '../api';
import { SectionHeader, TrustBadge, HealthBadge, StatusBadge, LoadingState, ErrorState, EmptyState } from './ui/States';
import AgentInvestigationDrawer from './AgentInvestigationDrawer';
import { useNavigate } from 'react-router-dom';

export default function MatchingCenter() {
  const navigate = useNavigate();

  // Task Input States
  const [taskPrompt, setTaskPrompt] = useState(
    'Conduct automated cryptographic code security review and identify reentrancy vulnerabilities.'
  );
  const [requiredCapability, setRequiredCapability] = useState('coding');
  const [minTrustScore, setMinTrustScore] = useState(0.60);
  const [taskUrgency, setTaskUrgency] = useState('NORMAL');

  // Execution States
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasExecuted, setHasExecuted] = useState(false);

  // UI States
  const [showIneligible, setShowIneligible] = useState(false);
  const [investigatingDid, setInvestigatingDid] = useState(null);
  const [copiedDid, setCopiedDid] = useState(null);

  const presets = [
    {
      title: 'Cryptographic Audit',
      cap: 'verification',
      prompt: 'Execute formal verification on cryptographic signature verification paths and validate non-repudiation.',
      minTrust: 0.70
    },
    {
      title: 'Threat Intel Retrieval',
      cap: 'research',
      prompt: 'Synthesize decentralized identity vulnerability disclosures and correlate MITRE ATT&CK patterns.',
      minTrust: 0.50
    },
    {
      title: 'Automated Code Synthesis',
      cap: 'coding',
      prompt: 'Synthesize robust Python verification scripts with comprehensive pytest test vectors.',
      minTrust: 0.60
    },
    {
      title: 'Multi-Agent Session Planning',
      cap: 'planning',
      prompt: 'Decompose complex analytics task into sequential execution pipeline nodes with trust gating.',
      minTrust: 0.65
    }
  ];

  const handleApplyPreset = (preset) => {
    setRequiredCapability(preset.cap);
    setTaskPrompt(preset.prompt);
    setMinTrustScore(preset.minTrust);
  };

  const handleExecuteMatching = async (e) => {
    if (e) e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      const res = await registryApi.matchAgents({
        required_capability: requiredCapability,
        min_trust_score: parseFloat(minTrustScore),
        task_description: taskPrompt
      });
      setCandidates(Array.isArray(res) ? res : []);
      setHasExecuted(true);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Candidate matching execution failed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleExecuteMatching();
  }, []);

  const handleCopy = (did) => {
    navigator.clipboard.writeText(did);
    setCopiedDid(did);
    setTimeout(() => setCopiedDid(null), 2000);
  };

  const handleAssignTask = (agent) => {
    // Navigate to Collaboration Center with pre-filled target agent and task description
    navigate('/collaboration', {
      state: {
        targetDid: agent.did,
        targetName: agent.agent_name,
        taskPrompt: taskPrompt
      }
    });
  };

  // Group candidates
  const bestMatch = candidates.find(c => c.decision === 'SELECTED');
  const eligibleCandidates = candidates.filter(c => c.decision === 'ELIGIBLE');
  const ineligibleCandidates = candidates.filter(c => c.decision.includes('REJECTED'));

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-in fade-in duration-300 font-sans">
      <SectionHeader 
        icon={Sliders}
        title="Task-Driven Agent Matchmaker & Recommender"
        subtitle="Formally compute multi-factor candidate compatibility scores and rank verified agents against specific workload requirements."
        badge="TRANSPARENT ALGORITHM"
      />

      {/* Task Specification Input Form */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div className="text-xs font-mono font-bold text-slate-700 dark:text-slate-300 uppercase tracking-widest flex items-center gap-2">
            <Zap size={13} className="text-tc-cyan" /> Workload Requirements Specification
          </div>
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-[10px] font-mono text-slate-400 mr-1">Presets:</span>
            {presets.map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleApplyPreset(p)}
                className="px-2 py-0.5 text-[10px] font-mono rounded bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
              >
                {p.title}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleExecuteMatching} className="space-y-4 font-mono text-xs">
          <div>
            <label className="block text-[11px] uppercase text-slate-500 mb-1 font-semibold">
              Operational Task Prompt / Workload Description
            </label>
            <textarea
              rows={2}
              value={taskPrompt}
              onChange={(e) => setTaskPrompt(e.target.value)}
              placeholder="Describe the specific objective, required context, and constraints for this workload..."
              className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2.5 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-[11px] uppercase text-slate-500 mb-1 font-semibold">
                Primary Required Capability
              </label>
              <select
                value={requiredCapability}
                onChange={(e) => setRequiredCapability(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
              >
                <option value="coding">Coding & Implementation</option>
                <option value="analysis">Analysis & Reasoning</option>
                <option value="research">Research & Retrieval</option>
                <option value="planning">Execution Planning</option>
                <option value="verification">Verification & Security</option>
                <option value="compute">General Compute</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] uppercase text-slate-500 mb-1 font-semibold">
                Minimum Trust Threshold T(t)
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="number"
                  step="0.05"
                  min="0.0"
                  max="1.0"
                  value={minTrustScore}
                  onChange={(e) => setMinTrustScore(e.target.value)}
                  className="w-24 bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
                />
                <span className="text-[10px] text-slate-400">
                  {minTrustScore >= 0.8 ? 'Strict (Trusted only)' : minTrustScore >= 0.5 ? 'Moderate' : 'Permissive'}
                </span>
              </div>
            </div>

            <div>
              <label className="block text-[11px] uppercase text-slate-500 mb-1 font-semibold">
                Task Priority & Urgency
              </label>
              <select
                value={taskUrgency}
                onChange={(e) => setTaskUrgency(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded p-2 text-xs font-mono text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none"
              >
                <option value="NORMAL">Standard Routine Execution</option>
                <option value="HIGH">High Priority Workload</option>
                <option value="CRITICAL">Mission-Critical Security Operation</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading}
              className="bg-tc-cyan text-white dark:text-black px-6 py-2.5 rounded font-mono font-bold text-xs uppercase tracking-wider hover:opacity-90 transition-opacity shadow-[0_0_15px_rgba(0,240,255,0.25)] flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              <Zap size={14} />
              {loading ? 'Evaluating Policy & Computing Scores...' : 'Compute Best-Match Recommendation'}
            </button>
          </div>
        </form>
      </div>

      {/* Main Results Display */}
      {loading ? (
        <LoadingState message="Scoring Candidate Agents via Multi-Factor Algorithm..." />
      ) : error ? (
        <ErrorState error={error} retry={handleExecuteMatching} />
      ) : candidates.length === 0 && hasExecuted ? (
        <EmptyState message="No candidate agents found in registry." />
      ) : (
        <div className="space-y-6">
          {/* TOP RECOMMENDED AGENT SPOTLIGHT */}
          {bestMatch && (
            <div className="bg-gradient-to-r from-cyan-500/10 via-sky-500/5 to-transparent border-2 border-tc-cyan dark:border-tc-cyan/80 rounded-xl p-6 shadow-[0_0_25px_rgba(0,240,255,0.15)] relative overflow-hidden font-mono">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-tc-cyan/30 pb-4 mb-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-tc-cyan text-white dark:text-black flex items-center gap-1.5 shadow-xs">
                      <Award size={12} /> TOP RECOMMENDED AGENT
                    </span>
                    <TrustBadge state={bestMatch.trust_state} />
                    <HealthBadge status={bestMatch.health_status} />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
                    {bestMatch.agent_name}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                    <span className="truncate max-w-[260px]" title={bestMatch.did}>{bestMatch.did}</span>
                    <button
                      onClick={() => handleCopy(bestMatch.did)}
                      className="text-slate-400 hover:text-tc-cyan transition-colors"
                      title="Copy DID"
                    >
                      {copiedDid === bestMatch.did ? <Check size={12} className="text-tc-success" /> : <Copy size={12} />}
                    </button>
                  </div>
                </div>

                <div className="flex flex-col items-end">
                  <span className="text-[10px] uppercase tracking-widest text-tc-cyan font-bold">Composite Match Score</span>
                  <div className="text-4xl font-bold text-cyan-600 dark:text-tc-cyan">
                    {bestMatch.match_score.toFixed(3)}
                  </div>
                  <span className="text-[10px] text-slate-400">Max theoretical: 1.000</span>
                </div>
              </div>

              {/* Rationale explanation */}
              <div className="bg-white/80 dark:bg-[#0b101d]/80 border border-tc-cyan/20 rounded-lg p-3 text-xs mb-5">
                <strong className="text-tc-cyan block uppercase mb-1">Recommendation Rationale:</strong>
                <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
                  {bestMatch.reason} Agent exhibits verified competence in <strong>{bestMatch.capabilities}</strong> with high trust resilience (T = {bestMatch.trust_score.toFixed(3)}) and consistent endpoint health.
                </p>
              </div>

              {/* Mathematical Score Contributions Breakdown */}
              <div className="space-y-2 mb-6">
                <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">
                  Transparent Score Breakdown (Sum = MatchScore)
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs">
                  <div className="p-3 bg-white dark:bg-[#0b101d] rounded-lg border border-slate-200 dark:border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Trust (w=0.4)</div>
                    <div className="text-base font-bold text-slate-900 dark:text-slate-100 mt-0.5">
                      +{bestMatch.score_breakdown?.trust_contribution?.toFixed(3) ?? (0.4 * bestMatch.trust_score).toFixed(3)}
                    </div>
                    <div className="text-[9px] text-slate-400 mt-0.5">0.4 &times; {bestMatch.trust_score.toFixed(3)}</div>
                  </div>

                  <div className="p-3 bg-white dark:bg-[#0b101d] rounded-lg border border-slate-200 dark:border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Reputation (w=0.3)</div>
                    <div className="text-base font-bold text-amber-500 mt-0.5">
                      +{bestMatch.score_breakdown?.reputation_contribution?.toFixed(3) ?? (0.3 * (bestMatch.reputation_score / 5.0)).toFixed(3)}
                    </div>
                    <div className="text-[9px] text-slate-400 mt-0.5">0.3 &times; ({bestMatch.reputation_score}/5.0)</div>
                  </div>

                  <div className="p-3 bg-white dark:bg-[#0b101d] rounded-lg border border-slate-200 dark:border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Success Rate (w=0.2)</div>
                    <div className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
                      +{bestMatch.score_breakdown?.success_contribution?.toFixed(3) ?? '0.200'}
                    </div>
                    <div className="text-[9px] text-slate-400 mt-0.5">0.2 &times; &sigma;</div>
                  </div>

                  <div className="p-3 bg-white dark:bg-[#0b101d] rounded-lg border border-slate-200 dark:border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase">Latency Factor (w=0.1)</div>
                    <div className="text-base font-bold text-slate-900 dark:text-slate-100 mt-0.5">
                      +{bestMatch.score_breakdown?.latency_contribution?.toFixed(3) ?? '0.100'}
                    </div>
                    <div className="text-[9px] text-slate-400 mt-0.5">0.1 &times; (1 - &lambda;)</div>
                  </div>
                </div>
              </div>

              {/* Actions on Best Match */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-tc-cyan/20">
                <button
                  type="button"
                  onClick={() => setInvestigatingDid(bestMatch.did)}
                  className="px-3.5 py-2 text-xs rounded border border-slate-300 dark:border-slate-700 hover:border-tc-cyan hover:text-tc-cyan text-slate-700 dark:text-slate-300 transition-colors flex items-center gap-1.5"
                >
                  <Shield size={13} /> Investigate Full Telemetry & History
                </button>

                <button
                  type="button"
                  onClick={() => handleAssignTask(bestMatch)}
                  className="px-5 py-2 rounded bg-tc-cyan text-white dark:text-black font-bold uppercase tracking-wider hover:opacity-90 transition-opacity flex items-center gap-2 shadow-xs"
                >
                  Assign Task & Initiate Collaboration <ArrowRight size={13} />
                </button>
              </div>
            </div>
          )}

          {/* OTHER ELIGIBLE CANDIDATES TABLE */}
          {eligibleCandidates.length > 0 && (
            <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4 shadow-xs font-mono">
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-widest flex items-center gap-2">
                  <CheckCircle2 size={13} className="text-emerald-500" /> Additional Eligible Candidates ({eligibleCandidates.length})
                </h4>
                <span className="text-[10px] text-slate-400">Ranked by Composite Match Score</span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-xs">
                  <thead className="bg-slate-50 dark:bg-[#080b13] text-[10px] text-slate-500 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                    <tr>
                      <th className="p-3">Rank</th>
                      <th className="p-3">Agent Name</th>
                      <th className="p-3">DID</th>
                      <th className="p-3 text-center">Match Score</th>
                      <th className="p-3 text-center">Trust T(t)</th>
                      <th className="p-3 text-center">Reputation</th>
                      <th className="p-3 text-center">Health</th>
                      <th className="p-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                    {eligibleCandidates.map((cand, idx) => (
                      <tr key={cand.did} className="hover:bg-slate-50 dark:hover:bg-[#121929]/70 transition-colors">
                        <td className="p-3 font-bold text-slate-400">#{idx + 2}</td>
                        <td className="p-3 font-bold text-slate-900 dark:text-slate-100">{cand.agent_name}</td>
                        <td className="p-3 text-slate-500 text-[10px] truncate max-w-[150px]" title={cand.did}>{cand.did}</td>
                        <td className="p-3 text-center font-bold text-cyan-600 dark:text-tc-cyan">{cand.match_score.toFixed(3)}</td>
                        <td className="p-3 text-center font-bold text-slate-800 dark:text-slate-200">{cand.trust_score.toFixed(3)}</td>
                        <td className="p-3 text-center text-amber-500 font-bold">{cand.reputation_score}/5.0</td>
                        <td className="p-3 text-center"><HealthBadge status={cand.health_status} /></td>
                        <td className="p-3 text-right">
                          <div className="flex items-center justify-end gap-1.5">
                            <button
                              onClick={() => setInvestigatingDid(cand.did)}
                              className="px-2 py-1 text-[10px] rounded border border-slate-300 dark:border-slate-700 hover:text-tc-cyan"
                            >
                              Inspect
                            </button>
                            <button
                              onClick={() => handleAssignTask(cand)}
                              className="px-2.5 py-1 text-[10px] rounded bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 hover:bg-tc-cyan hover:text-black font-semibold"
                            >
                              Assign
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* EXPANDABLE INELIGIBLE CANDIDATES SECTION */}
          {ineligibleCandidates.length > 0 && (
            <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs font-mono">
              <button
                type="button"
                onClick={() => setShowIneligible(!showIneligible)}
                className="w-full p-4 flex items-center justify-between bg-slate-50 dark:bg-[#080b13] hover:bg-slate-100 dark:hover:bg-[#121929]/50 transition-colors text-left"
              >
                <div className="flex items-center gap-2">
                  <ShieldAlert size={14} className="text-amber-500" />
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200">
                    Filtered & Ineligible Candidates ({ineligibleCandidates.length})
                  </span>
                  <span className="text-[10px] text-slate-400">
                    (Restricted by security policy, capability mismatch, or trust threshold)
                  </span>
                </div>
                {showIneligible ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>

              {showIneligible && (
                <div className="p-4 border-t border-slate-200 dark:border-slate-800 overflow-x-auto">
                  <table className="w-full text-left font-mono text-xs">
                    <thead className="text-[10px] text-slate-400 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                      <tr>
                        <th className="p-2.5">Agent Identity</th>
                        <th className="p-2.5">Trust State</th>
                        <th className="p-2.5 text-center">Score T(t)</th>
                        <th className="p-2.5">Exclusion / Policy Rejection Reason</th>
                        <th className="p-2.5 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                      {ineligibleCandidates.map((cand) => (
                        <tr key={cand.did} className="hover:bg-slate-50/50 dark:hover:bg-[#121929]/40 transition-colors">
                          <td className="p-2.5">
                            <div className="font-bold text-slate-800 dark:text-slate-200">{cand.agent_name}</div>
                            <div className="text-[10px] text-slate-400 truncate max-w-[140px]">{cand.did}</div>
                          </td>
                          <td className="p-2.5">
                            <TrustBadge state={cand.trust_state} />
                          </td>
                          <td className="p-2.5 text-center font-bold text-slate-600 dark:text-slate-400">
                            {cand.trust_score.toFixed(3)}
                          </td>
                          <td className="p-2.5 text-[11px] text-rose-600 dark:text-rose-400 max-w-sm">
                            {cand.reason}
                          </td>
                          <td className="p-2.5 text-right">
                            <button
                              onClick={() => setInvestigatingDid(cand.did)}
                              className="px-2 py-0.5 text-[10px] rounded border border-slate-300 dark:border-slate-700 hover:text-tc-cyan"
                            >
                              Audit
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* FORMAL MATHEMATICAL MATCHING EQUATION CARD */}
          <div className="bg-slate-50 dark:bg-[#080b13] border border-slate-200 dark:border-slate-800 p-5 rounded-lg font-mono text-xs space-y-2">
            <div className="text-[10px] uppercase font-bold text-slate-500 tracking-widest border-b border-slate-200 dark:border-slate-800 pb-2 flex items-center gap-1.5">
              <Info size={13} className="text-tc-cyan" /> Mathematical Matching Formulation & Zero-Trust Governance
            </div>
            <p className="text-cyan-700 dark:text-tc-cyan font-bold text-sm">
              MatchScore = 0.4 &middot; T(t) + 0.3 &middot; (r / 5.0) + 0.2 &middot; &sigma; + 0.1 &middot; (1 &minus; &lambda;)
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-600 dark:text-slate-400 pt-1">
              <div>
                &bull; <strong>T(t)</strong>: Live temporal trust score [0.0, 1.0]<br/>
                &bull; <strong>r</strong>: Historical reputation rating [1.0, 5.0]
              </div>
              <div>
                &bull; <strong>&sigma;</strong>: Cumulative task success rate [0.0, 1.0]<br/>
                &bull; <strong>&lambda;</strong>: Normalized latency penalty = min(latency_ms / 2000, 1.0)
              </div>
            </div>
            <p className="text-[10px] text-slate-500 dark:text-slate-500 pt-1">
              Hard Boundary Rule: Any agent in QUARANTINED or REVOKED trust state immediately triggers zero-score rejection regardless of reputation or latency metrics.
            </p>
          </div>
        </div>
      )}

      {/* Investigation Drawer Modal */}
      {investigatingDid && (
        <AgentInvestigationDrawer
          did={investigatingDid}
          onClose={() => setInvestigatingDid(null)}
          onRefreshList={handleExecuteMatching}
        />
      )}
    </div>
  );
}
