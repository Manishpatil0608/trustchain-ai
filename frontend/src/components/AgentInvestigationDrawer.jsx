import React, { useState, useEffect } from 'react';
import { 
  X, Copy, Check, Shield, Activity, Cpu, Server, Clock, CheckCircle2, 
  AlertTriangle, XCircle, ShieldAlert, ArrowDown, ExternalLink, RefreshCw,
  GitMerge, Database, BarChart3, Radio
} from 'lucide-react';
import { trustApi, registryApi } from '../api';
import { TrustBadge, HealthBadge, StatusBadge, LoadingState, ErrorState, EmptyState } from './ui/States';
import { Link } from 'react-router-dom';

export default function AgentInvestigationDrawer({ did, onClose, onRefreshList }) {
  const [profile, setProfile] = useState(null);
  const [trustState, setTrustState] = useState(null);
  const [telemetry, setTelemetry] = useState([]);
  const [audit, setAudit] = useState([]);
  const [activeTab, setActiveTab] = useState('telemetry'); // 'telemetry' | 'audit' | 'causality'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [checkingHealth, setCheckingHealth] = useState(false);

  useEffect(() => {
    if (!did) return;

    let isMounted = true;
    setLoading(true);
    setError(null);

    const loadData = async () => {
      try {
        const [profRes, stateRes, telemRes, auditRes] = await Promise.all([
          registryApi.getAgentProfile(did).catch(() => null),
          trustApi.getAgentState(did).catch(() => null),
          trustApi.getAgentTelemetry(did).catch(() => []),
          trustApi.getAgentAudit(did).catch(() => []),
        ]);

        if (!isMounted) return;

        if (!profRes && !stateRes) {
          throw new Error(`Agent with DID "${did}" could not be found.`);
        }

        setProfile(profRes);
        setTrustState(stateRes);
        setTelemetry(Array.isArray(telemRes) ? telemRes : []);
        setAudit(Array.isArray(auditRes) ? auditRes : []);
      } catch (err) {
        if (isMounted) {
          setError(err.response?.data?.detail || err.message || 'Failed to load agent investigation data.');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadData();

    // Close on Escape key press
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      isMounted = false;
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [did, onClose]);

  const handleCopyDid = () => {
    if (!did) return;
    navigator.clipboard.writeText(did);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleManualHealthCheck = async () => {
    if (!did || checkingHealth) return;
    try {
      setCheckingHealth(true);
      const res = await registryApi.checkAgentHealth(did);
      if (profile) {
        setProfile({
          ...profile,
          health_status: res.health_status,
          last_response_time_ms: res.response_time_ms,
          last_health_check: res.last_health_check,
          last_error: res.last_error,
        });
      }
      if (onRefreshList) onRefreshList();
    } catch (err) {
      console.error('Manual health check failed:', err);
    } finally {
      setCheckingHealth(false);
    }
  };

  if (!did) return null;

  // Resolve values prioritizing profile, falling back to trustState
  const agentName = profile?.agent_name || `Agent ${did.slice(0, 16)}...`;
  const currentTrustScore = trustState?.temporal_trust_score ?? profile?.trust_score ?? 1.0;
  const currentTrustState = trustState?.trust_state ?? profile?.trust_state ?? 'TRUSTED';
  const reputation = profile?.reputation_score ?? 5.0;
  const operationalStatus = profile?.operational_status ?? 'AVAILABLE';
  const healthStatus = profile?.health_status ?? 'HEALTHY';
  const modelName = profile?.model_name || 'Standard LLM';
  const modelProvider = profile?.model_provider || 'Built-in Connector';
  const endpoint = profile?.endpoint || 'Local Execution Bridge';
  const capabilities = (profile?.capabilities || 'general').split(',').map(c => c.trim()).filter(Boolean);

  // Execution Metrics
  const totalTasks = profile?.total_tasks ?? telemetry.length;
  const successfulTasks = profile?.successful_tasks ?? telemetry.filter(t => t.success).length;
  const failedTasks = profile?.failed_tasks ?? (totalTasks - successfulTasks);
  const successRate = totalTasks > 0 ? (successfulTasks / totalTasks) * 100 : 100;
  const avgLatency = profile?.last_response_time_ms ?? (
    telemetry.length > 0 
      ? Math.round(telemetry.reduce((acc, t) => acc + (t.latency_ms || 0), 0) / telemetry.length) 
      : 0
  );

  // Trust Math signals over recent telemetry
  const recentWindow = telemetry.slice(0, 10);
  const sRate = recentWindow.length ? recentWindow.filter(t => t.success).length / recentWindow.length : 1;
  const cRate = recentWindow.length ? recentWindow.filter(t => !t.compliance_event).length / recentWindow.length : 1;
  const windowAvgLat = recentWindow.length ? recentWindow.reduce((acc, t) => acc + (t.latency_ms || 0), 0) / recentWindow.length : 0;
  const lPenalty = Math.min(1, Math.max(0, windowAvgLat / 2000));
  const pScore = (0.6 * sRate) + (0.3 * cRate) + (0.1 * (1 - lPenalty));

  const isQuarantined = currentTrustState === 'QUARANTINED' || currentTrustState === 'REVOKED';

  return (
    <div 
      className="fixed inset-0 z-50 bg-black/60 dark:bg-black/80 backdrop-blur-xs flex justify-end animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        className="w-full max-w-2xl bg-white dark:bg-[#0b101d] border-l border-slate-200 dark:border-slate-800 h-full flex flex-col shadow-2xl overflow-hidden font-sans transition-all text-slate-900 dark:text-slate-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Header Bar */}
        <div className="p-5 border-b border-slate-200 dark:border-slate-800 flex items-start justify-between bg-slate-50/80 dark:bg-[#080b13]/80 backdrop-blur-md">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-tc-cyan/10 border border-tc-cyan/30 rounded text-tc-cyan">
                <Shield size={16} />
              </span>
              <h3 className="text-base font-bold font-mono tracking-wide uppercase">
                {agentName}
              </h3>
              <TrustBadge state={currentTrustState} />
            </div>
            <div className="flex items-center gap-2 text-xs font-mono text-slate-500 dark:text-slate-400">
              <span className="truncate max-w-[280px]" title={did}>{did}</span>
              <button 
                onClick={handleCopyDid} 
                className="text-slate-400 hover:text-tc-cyan transition-colors"
                title="Copy Agent DID"
              >
                {copied ? <Check size={13} className="text-tc-success" /> : <Copy size={13} />}
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link
              to={`/agents/${encodeURIComponent(did)}`}
              className="px-2.5 py-1 text-[11px] font-mono rounded border border-slate-300 dark:border-slate-700 hover:border-tc-cyan hover:text-tc-cyan text-slate-600 dark:text-slate-300 transition-colors flex items-center gap-1.5"
              title="Open Full Profile Page"
            >
              <ExternalLink size={12} /> Full View
            </Link>
            <button
              onClick={onClose}
              className="p-1.5 rounded-md text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-200/60 dark:hover:bg-slate-800/60 transition-colors"
              title="Close Panel [Esc]"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
          {loading ? (
            <LoadingState message="Decoupling Agent DID & Investigating Telemetry Logs..." />
          ) : error ? (
            <div className="space-y-4">
              <ErrorState error={error} retry={() => window.location.reload()} />
              <div className="text-center">
                <button
                  onClick={onClose}
                  className="px-4 py-1.5 text-xs font-mono rounded border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
                >
                  Return to Inventory
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Critical Alert if Quarantined or Revoked */}
              {isQuarantined && (
                <div className="p-4 bg-rose-50 dark:bg-rose-950/20 border border-rose-300 dark:border-rose-800/80 rounded-lg flex items-start gap-3 text-rose-800 dark:text-rose-300 text-xs font-mono">
                  <ShieldAlert size={18} className="text-rose-600 dark:text-rose-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <strong className="font-bold uppercase tracking-wider block">Security Isolation Enforced</strong>
                    <span>
                      {currentTrustState === 'REVOKED'
                        ? 'This agent identity has been administratively revoked. All collaboration and execution privileges are permanently terminated.'
                        : 'Behavioral trust threshold breached (T < 0.50). Adaptive policy gateway has placed this agent under Quarantine. Privileged actions are blocked.'}
                    </span>
                  </div>
                </div>
              )}

              {/* KPI Metrics Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 p-3 rounded-lg text-center">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Trust Score T(t)</div>
                  <div className={`text-2xl font-mono font-bold mt-1 ${
                    currentTrustScore >= 0.8 ? 'text-tc-success' : currentTrustScore >= 0.5 ? 'text-tc-warning' : 'text-tc-danger'
                  }`}>
                    {currentTrustScore.toFixed(4)}
                  </div>
                </div>

                <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 p-3 rounded-lg text-center">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Reputation</div>
                  <div className="text-2xl font-mono font-bold text-amber-500 mt-1">
                    {reputation.toFixed(1)}/5.0
                  </div>
                </div>

                <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 p-3 rounded-lg text-center">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Operation</div>
                  <div className="mt-2">
                    <StatusBadge status={operationalStatus} />
                  </div>
                </div>

                <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 p-3 rounded-lg text-center">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Endpoint Health</div>
                  <div className="mt-2">
                    <HealthBadge status={healthStatus} />
                  </div>
                </div>
              </div>

              {/* Identity & Model Profile Details */}
              <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 rounded-lg p-4 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
                  <span className="text-[10px] uppercase font-bold text-slate-500 flex items-center gap-1.5">
                    <Cpu size={13} className="text-tc-cyan" /> Model & Architecture Specification
                  </span>
                  <button
                    onClick={handleManualHealthCheck}
                    disabled={checkingHealth}
                    className="text-[10px] text-tc-cyan hover:underline flex items-center gap-1 cursor-pointer disabled:opacity-50"
                    title="Probe Live Model Endpoint"
                  >
                    <RefreshCw size={10} className={checkingHealth ? "animate-spin" : ""} />
                    {checkingHealth ? "Probing..." : "Test Health"}
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-[10px] text-slate-500 block uppercase">Model Name</span>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">{modelName}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-500 block uppercase">Model Provider</span>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">{modelProvider}</span>
                  </div>
                  <div className="col-span-2">
                    <span className="text-[10px] text-slate-500 block uppercase">Execution Endpoint</span>
                    <span className="text-slate-600 dark:text-slate-400 truncate block text-[11px]" title={endpoint}>
                      {endpoint}
                    </span>
                  </div>
                </div>

                <div>
                  <span className="text-[10px] text-slate-500 block uppercase mb-1.5">Registered Capabilities</span>
                  <div className="flex flex-wrap gap-1.5">
                    {capabilities.length > 0 ? (
                      capabilities.map((cap, i) => (
                        <span 
                          key={i} 
                          className="px-2 py-0.5 rounded text-[10px] font-mono bg-sky-50 dark:bg-cyan-950/40 text-cyan-700 dark:text-tc-cyan border border-sky-200 dark:border-cyan-800/60 font-semibold uppercase"
                        >
                          {cap}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-500 text-[11px]">No capabilities listed</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Task Execution Metrics */}
              <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 rounded-lg p-4 font-mono text-xs space-y-3">
                <div className="text-[10px] uppercase font-bold text-slate-500 flex items-center gap-1.5 border-b border-slate-200 dark:border-slate-800 pb-2">
                  <BarChart3 size={13} className="text-tc-cyan" /> Workload Execution Metrics
                </div>

                <div className="grid grid-cols-3 md:grid-cols-5 gap-3 text-center">
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800/80">
                    <div className="text-[9px] text-slate-500 uppercase">Total Tasks</div>
                    <div className="text-base font-bold text-slate-900 dark:text-slate-100">{totalTasks}</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800/80">
                    <div className="text-[9px] text-emerald-600 dark:text-emerald-400 uppercase">Success</div>
                    <div className="text-base font-bold text-emerald-600 dark:text-emerald-400">{successfulTasks}</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800/80">
                    <div className="text-[9px] text-rose-600 dark:text-rose-400 uppercase">Failed</div>
                    <div className="text-base font-bold text-rose-600 dark:text-rose-400">{failedTasks}</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800/80">
                    <div className="text-[9px] text-slate-500 uppercase">Success %</div>
                    <div className="text-base font-bold text-slate-900 dark:text-slate-100">{successRate.toFixed(1)}%</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800/80 col-span-2 md:col-span-1">
                    <div className="text-[9px] text-slate-500 uppercase">Avg Latency</div>
                    <div className="text-base font-bold text-slate-900 dark:text-slate-100">{avgLatency} ms</div>
                  </div>
                </div>
              </div>

              {/* Trust Causality Equation Breakdown */}
              <div className="bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 rounded-lg p-4 font-mono text-xs space-y-3">
                <div className="text-[10px] uppercase font-bold text-slate-500 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
                  <span className="flex items-center gap-1.5">
                    <Activity size={13} className="text-tc-cyan" /> Behavioral Trust Math Core (Last 10 Events)
                  </span>
                  <span className="text-tc-cyan font-bold">P(t) = {pScore.toFixed(4)}</span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-center text-[10px]">
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800">
                    <div className="text-slate-500">S(t) Success (w=0.6)</div>
                    <div className="text-sm font-bold text-slate-900 dark:text-slate-100 mt-0.5">{sRate.toFixed(3)}</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800">
                    <div className="text-slate-500">C(t) Policy (w=0.3)</div>
                    <div className="text-sm font-bold text-slate-900 dark:text-slate-100 mt-0.5">{cRate.toFixed(3)}</div>
                  </div>
                  <div className="p-2 bg-white dark:bg-[#0b101d] rounded border border-slate-200 dark:border-slate-800">
                    <div className="text-slate-500">L(t) Latency (w=0.1)</div>
                    <div className="text-sm font-bold text-slate-900 dark:text-slate-100 mt-0.5">{lPenalty.toFixed(3)}</div>
                  </div>
                </div>

                <div className="text-[10px] text-slate-500 dark:text-slate-400">
                  Formula: <span className="font-semibold text-slate-700 dark:text-slate-300">T(t) = 0.7 &middot; P(t) + 0.3 &middot; T(t-1)</span>
                </div>
              </div>

              {/* Tabs for Telemetry & Audit History */}
              <div className="space-y-3">
                <div className="flex border-b border-slate-200 dark:border-slate-800 font-mono text-xs">
                  <button
                    onClick={() => setActiveTab('telemetry')}
                    className={`px-4 py-2 font-bold uppercase transition-colors border-b-2 flex items-center gap-1.5 ${
                      activeTab === 'telemetry'
                        ? 'border-tc-cyan text-cyan-700 dark:text-tc-cyan'
                        : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'
                    }`}
                  >
                    <Database size={13} /> Recent Telemetry ({telemetry.length})
                  </button>
                  <button
                    onClick={() => setActiveTab('audit')}
                    className={`px-4 py-2 font-bold uppercase transition-colors border-b-2 flex items-center gap-1.5 ${
                      activeTab === 'audit'
                        ? 'border-tc-cyan text-cyan-700 dark:text-tc-cyan'
                        : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'
                    }`}
                  >
                    <GitMerge size={13} /> Trust Transitions ({audit.length})
                  </button>
                </div>

                {activeTab === 'telemetry' && (
                  <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
                    {telemetry.length === 0 ? (
                      <EmptyState message="No telemetry records captured for this agent yet." />
                    ) : (
                      <div className="overflow-x-auto max-h-60 custom-scrollbar">
                        <table className="w-full text-left font-mono text-xs">
                          <thead className="bg-slate-50 dark:bg-[#080b13] text-[10px] text-slate-500 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800 sticky top-0">
                            <tr>
                              <th className="p-2.5">Task ID</th>
                              <th className="p-2.5 text-center">Status</th>
                              <th className="p-2.5 text-center">Policy</th>
                              <th className="p-2.5 text-right">Latency</th>
                              <th className="p-2.5 text-right">Timestamp</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {telemetry.slice(0, 20).map((t, idx) => (
                              <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-[#0b101d] transition-colors">
                                <td className="p-2.5 text-[11px] font-bold text-slate-700 dark:text-slate-300 truncate max-w-[120px]" title={t.task_id}>
                                  {t.task_id}
                                </td>
                                <td className="p-2.5 text-center">
                                  {t.success ? (
                                    <span className="inline-flex items-center gap-1 text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
                                      <CheckCircle2 size={11} /> OK
                                    </span>
                                  ) : (
                                    <span className="inline-flex items-center gap-1 text-[10px] text-rose-600 dark:text-rose-400 font-bold">
                                      <XCircle size={11} /> FAIL
                                    </span>
                                  )}
                                </td>
                                <td className="p-2.5 text-center">
                                  {t.compliance_event ? (
                                    <span className="text-[10px] text-rose-600 dark:text-rose-400 font-bold" title="Policy Breach Flagged">
                                      BREACH
                                    </span>
                                  ) : (
                                    <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold">
                                      COMPLIANT
                                    </span>
                                  )}
                                </td>
                                <td className="p-2.5 text-right text-[11px] text-slate-600 dark:text-slate-400">
                                  {t.latency_ms} ms
                                </td>
                                <td className="p-2.5 text-right text-[10px] text-slate-400 truncate max-w-[100px]">
                                  {t.timestamp ? new Date(t.timestamp).toLocaleTimeString() : 'N/A'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'audit' && (
                  <div className="bg-white dark:bg-[#121929] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
                    {audit.length === 0 ? (
                      <EmptyState message="No trust state transitions recorded." />
                    ) : (
                      <div className="overflow-x-auto max-h-60 custom-scrollbar">
                        <table className="w-full text-left font-mono text-xs">
                          <thead className="bg-slate-50 dark:bg-[#080b13] text-[10px] text-slate-500 uppercase tracking-wider border-b border-slate-200 dark:border-slate-800 sticky top-0">
                            <tr>
                              <th className="p-2.5">Transition</th>
                              <th className="p-2.5">Reason</th>
                              <th className="p-2.5 text-right">Timestamp</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                            {audit.map((a, idx) => (
                              <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-[#0b101d] transition-colors">
                                <td className="p-2.5 text-[10px] font-bold">
                                  <span className="text-slate-500">{a.previous_state || 'INIT'}</span>
                                  <span className="mx-1 text-tc-cyan">&rarr;</span>
                                  <span className="text-slate-900 dark:text-slate-100">{a.new_state}</span>
                                </td>
                                <td className="p-2.5 text-[11px] text-slate-600 dark:text-slate-400 max-w-[200px] truncate" title={a.reason}>
                                  {a.reason || 'Telemetry driven state adjustment'}
                                </td>
                                <td className="p-2.5 text-right text-[10px] text-slate-400">
                                  {a.timestamp ? new Date(a.timestamp).toLocaleTimeString() : 'N/A'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#080b13] flex items-center justify-between font-mono text-xs">
          <div className="text-[11px] text-slate-500">
            Esc to exit inspection
          </div>
          <div className="flex items-center gap-2">
            <Link
              to={`/collaboration`}
              className="px-3 py-1.5 rounded bg-tc-cyan text-white dark:text-black font-bold uppercase tracking-wider hover:opacity-90 transition-opacity"
            >
              Initiate Collaboration
            </Link>
            <button
              onClick={onClose}
              className="px-3 py-1.5 rounded border border-slate-300 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 uppercase tracking-wider transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
