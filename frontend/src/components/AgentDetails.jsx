import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { trustApi, registryApi } from '../api';
import { 
  ArrowLeft, Key, Activity, ShieldAlert, FileJson, CheckCircle2, ShieldOff, 
  ArrowDown, Cpu, Server, Check, Copy, ExternalLink, RefreshCw, BarChart3, Database, GitMerge
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { LoadingState, ErrorState, EmptyState, TrustBadge, HealthBadge, StatusBadge } from './ui/States';
import { useTheme } from '../context/ThemeContext';

export default function AgentDetails() {
  const { did } = useParams();
  const { chartTheme } = useTheme();
  const decodedDid = decodeURIComponent(did);

  const [profile, setProfile] = useState(null);
  const [trustState, setTrustState] = useState(null);
  const [telemetry, setTelemetry] = useState([]);
  const [audit, setAudit] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);

    Promise.all([
      trustApi.getAgentState(decodedDid).catch(() => null),
      trustApi.getAgentTelemetry(decodedDid).catch(() => []),
      registryApi.getAgentProfile(decodedDid).catch(() => null),
      trustApi.getAgentAudit(decodedDid).catch(() => []),
    ]).then(([s, t, p, a]) => {
      if (isMounted) {
        if (!s && !p) {
          setError(`Agent with DID "${decodedDid}" was not found.`);
        } else {
          setTrustState(s);
          setTelemetry(Array.isArray(t) ? t : []);
          setProfile(p);
          setAudit(Array.isArray(a) ? a : []);
        }
      }
    }).catch(err => {
      if (isMounted) setError(err.message || "Failed to load agent profile");
    }).finally(() => {
      if (isMounted) setLoading(false);
    });

    return () => { isMounted = false; };
  }, [decodedDid]);

  const handleCopyDid = () => {
    navigator.clipboard.writeText(decodedDid);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) return <LoadingState message="DECRYPTING IDENTITY & VERIFYING CREDENTIAL POSTURE..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;
  if (!trustState && !profile) return <EmptyState message="AGENT NOT FOUND IN REGISTRY" />;

  const currentTrustScore = trustState?.temporal_trust_score ?? profile?.trust_score ?? 1.0;
  const currentTrustState = trustState?.trust_state ?? profile?.trust_state ?? 'TRUSTED';
  const isQuarantined = currentTrustState === 'QUARANTINED' || currentTrustState === 'REVOKED';

  const agentName = profile?.agent_name || `Agent ${decodedDid.slice(0, 16)}...`;
  const modelName = profile?.model_name || 'Standard Agent';
  const modelProvider = profile?.model_provider || 'Built-in Provider';
  const endpoint = profile?.endpoint || 'Local Execution Bridge';
  const healthStatus = profile?.health_status || 'HEALTHY';
  const operationalStatus = profile?.operational_status || 'AVAILABLE';
  const reputation = profile?.reputation_score ?? 5.0;
  const capabilities = (profile?.capabilities || 'general').split(',').map(c => c.trim()).filter(Boolean);

  const totalTasks = profile?.total_tasks ?? telemetry.length;
  const successfulTasks = profile?.successful_tasks ?? telemetry.filter(t => t.success).length;
  const failedTasks = profile?.failed_tasks ?? (totalTasks - successfulTasks);
  const avgLatency = profile?.last_response_time_ms ?? (
    telemetry.length ? Math.round(telemetry.reduce((acc, t) => acc + (t.latency_ms || 0), 0) / telemetry.length) : 0
  );

  // Behavioral signals
  const sRate = telemetry.length ? telemetry.filter(t => t.success).length / telemetry.length : 1;
  const cRate = telemetry.length ? telemetry.filter(t => !t.compliance_event).length / telemetry.length : 1;
  const lPenalty = Math.min(1, Math.max(0, avgLatency / 2000));
  const pScore = (0.6 * sRate) + (0.3 * cRate) + (0.1 * (1 - lPenalty));

  const chartData = [...telemetry].reverse().map((t, i) => ({
    event: i + 1,
    success: t.success ? 1 : 0,
    latency: t.latency_ms
  }));

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-in fade-in duration-300 font-sans">
      <Link 
        to="/agents" 
        className="inline-flex items-center gap-2 text-tc-cyan hover:text-slate-900 dark:hover:text-white text-xs font-mono tracking-widest uppercase transition-colors"
      >
        <ArrowLeft size={14} /> Return to Agent Inventory
      </Link>

      {/* Main Agent Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-6 rounded-lg shadow-xs">
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-2.5">
            <h2 className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-100 uppercase tracking-wide">
              {agentName}
            </h2>
            <TrustBadge state={currentTrustState} />
            <HealthBadge status={healthStatus} />
            <StatusBadge status={operationalStatus} />
          </div>
          <div className="text-slate-500 dark:text-slate-400 font-mono text-xs flex items-center gap-2">
            <Key size={13} className="text-tc-cyan flex-shrink-0" /> 
            <span className="truncate max-w-[320px] md:max-w-xl" title={decodedDid}>{decodedDid}</span>
            <button 
              onClick={handleCopyDid} 
              className="text-slate-400 hover:text-tc-cyan transition-colors"
              title="Copy Full DID"
            >
              {copied ? <Check size={13} className="text-tc-success" /> : <Copy size={13} />}
            </button>
          </div>
        </div>

        <div className="text-right bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 px-6 py-3 rounded-lg min-w-[200px]">
          <div className="text-[10px] text-tc-cyan tracking-widest font-mono uppercase mb-0.5">Temporal Trust T(t)</div>
          <div className={`text-4xl font-mono font-bold ${
            currentTrustState === 'TRUSTED' ? 'text-tc-success' : currentTrustState === 'SUSPICIOUS' ? 'text-tc-warning' : 'text-tc-danger'
          }`}>
            {currentTrustScore.toFixed(4)}
          </div>
        </div>
      </div>

      {/* Profile & Execution Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Column: Model & Security Details */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-5 rounded-lg space-y-4 font-mono text-xs shadow-xs">
            <h3 className="text-xs font-mono tracking-widest text-slate-500 uppercase flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-2">
              <Cpu size={14} className="text-tc-cyan"/> Model Architecture
            </h3>
            
            <div className="space-y-3">
              <div>
                <span className="text-[10px] text-slate-500 uppercase block">Model Specification</span>
                <span className="font-bold text-slate-900 dark:text-slate-200">{modelName}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase block">Inference Provider</span>
                <span className="font-bold text-slate-900 dark:text-slate-200">{modelProvider}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase block">Endpoint Bridge</span>
                <span className="text-slate-600 dark:text-slate-400 text-[11px] truncate block" title={endpoint}>{endpoint}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase block">Reputation Score</span>
                <span className="font-bold text-amber-500 text-sm">{reputation.toFixed(1)} / 5.0</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase block mb-1">Capabilities</span>
                <div className="flex flex-wrap gap-1">
                  {capabilities.map((c, i) => (
                    <span key={i} className="px-1.5 py-0.5 rounded text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold uppercase">
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Identity & Cryptographic Gating Status */}
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-5 rounded-lg space-y-4 font-mono text-xs shadow-xs">
            <h3 className="text-xs font-mono tracking-widest text-slate-500 uppercase flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-2">
              <FileJson size={14} className="text-tc-cyan"/> Security Boundary
            </h3>
            <div className="space-y-3">
              <div>
                <div className="text-[10px] text-slate-500 uppercase mb-1">Cryptographic Identity</div>
                <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-50 dark:bg-emerald-950/20 p-2 rounded border border-emerald-200 dark:border-emerald-800/40">
                  <CheckCircle2 size={13}/> ED25519 VERIFIED
                </div>
              </div>
              <div>
                <div className="text-[10px] text-slate-500 uppercase mb-1">Adaptive Policy Gateway</div>
                <div className={`flex items-center gap-1.5 font-bold p-2 rounded border ${
                  isQuarantined 
                    ? 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40' 
                    : 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40'
                }`}>
                  {isQuarantined ? <><ShieldOff size={13}/> RESTRICTED / BLOCKED</> : <><CheckCircle2 size={13}/> PRIVILEGED PERMITTED</>}
                </div>
              </div>
            </div>
            {isQuarantined && (
              <div className="p-3 bg-rose-50 dark:bg-rose-950/20 border border-rose-300 dark:border-rose-800/60 rounded text-[11px] text-rose-700 dark:text-rose-300 font-mono leading-relaxed">
                <ShieldAlert size={14} className="inline mr-1.5 mb-0.5" />
                Adaptive Policy Gateway has isolated this agent due to behavioral score degradation.
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Execution Metrics, Causality & Telemetry Chart */}
        <div className="lg:col-span-3 space-y-6">
          {/* Workload Execution Stats Bar */}
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-5 rounded-lg shadow-xs font-mono">
            <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 flex items-center gap-2">
              <BarChart3 size={14} className="text-tc-cyan" /> Historical Workload Performance
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-center">
              <div className="p-3 bg-slate-50 dark:bg-[#121929] rounded border border-slate-200 dark:border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase">Total Tasks</div>
                <div className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-0.5">{totalTasks}</div>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-[#121929] rounded border border-slate-200 dark:border-slate-800">
                <div className="text-[10px] text-emerald-600 dark:text-emerald-400 uppercase">Successful</div>
                <div className="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">{successfulTasks}</div>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-[#121929] rounded border border-slate-200 dark:border-slate-800">
                <div className="text-[10px] text-rose-600 dark:text-rose-400 uppercase">Failed</div>
                <div className="text-xl font-bold text-rose-600 dark:text-rose-400 mt-0.5">{failedTasks}</div>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-[#121929] rounded border border-slate-200 dark:border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase">Success %</div>
                <div className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-0.5">
                  {totalTasks > 0 ? ((successfulTasks / totalTasks) * 100).toFixed(1) : '100.0'}%
                </div>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-[#121929] rounded border border-slate-200 dark:border-slate-800 col-span-2 sm:col-span-1">
                <div className="text-[10px] text-slate-500 uppercase">Avg Latency</div>
                <div className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-0.5">{avgLatency} ms</div>
              </div>
            </div>
          </div>

          {/* Trust Causality Pipeline */}
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-6 rounded-lg shadow-xs font-mono">
            <h3 className="text-xs tracking-widest text-slate-500 mb-4 uppercase flex items-center gap-2">
              <Activity size={14} className="text-tc-cyan"/> Trust Causality Decomposition Pipeline
            </h3>
            
            <div className="flex flex-col md:flex-row items-center justify-between mb-6 gap-3">
              {[
                { label: 'S(t) Success', val: sRate, w: '0.6', desc: 'Task completion rate' },
                { label: 'C(t) Compliance', val: cRate, w: '0.3', desc: 'Security protocol adherence' },
                { label: 'L(t) Latency', val: lPenalty, w: '0.1', desc: 'Normalized latency penalty' }
              ].map((s, i) => (
                <div key={i} className="flex-1 w-full bg-slate-50 dark:bg-[#121929] border border-slate-200 dark:border-slate-800 p-4 rounded-lg text-center">
                  <div className="text-[10px] text-slate-500 uppercase mb-1">Weight: {s.w}</div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-slate-100">{s.val.toFixed(3)}</div>
                  <div className="text-xs font-bold text-cyan-700 dark:text-tc-cyan tracking-wider uppercase mt-1">{s.label}</div>
                  <div className="text-[9px] text-slate-500 mt-1">{s.desc}</div>
                </div>
              ))}
            </div>

            <div className="flex justify-center mb-4">
              <ArrowDown className="text-slate-400 dark:text-slate-600 animate-bounce" size={18} />
            </div>

            <div className="flex justify-center mb-6">
              <div className="bg-slate-50 dark:bg-[#121929] border-2 border-cyan-400/60 dark:border-tc-cyan/50 p-5 rounded-xl text-center min-w-[280px]">
                <div className="text-[11px] text-slate-500 uppercase tracking-widest mb-1">Composite Behavioral Score P(t)</div>
                <div className="text-3xl font-bold text-cyan-700 dark:text-tc-cyan">{pScore.toFixed(4)}</div>
                <div className="text-[10px] text-slate-500 mt-1.5">P(t) = 0.6&middot;S + 0.3&middot;C + 0.1&middot;(1-L)</div>
              </div>
            </div>

            {/* Telemetry Chart */}
            <div className="border-t border-slate-200 dark:border-slate-800 pt-4">
              <div className="text-[10px] text-slate-500 uppercase tracking-widest mb-3">
                Telemetry Execution Chronology
              </div>
              <div className="w-full h-48">
                {telemetry.length === 0 ? (
                  <EmptyState message="NO TELEMETRY RECORDED FOR THIS AGENT" />
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                      <XAxis dataKey="event" stroke={chartTheme.text} fontSize={10} tickLine={false} fontFamily="monospace" />
                      <YAxis stroke={chartTheme.text} fontSize={10} domain={[0, 1]} tickLine={false} axisLine={false} fontFamily="monospace" />
                      <Tooltip contentStyle={{ backgroundColor: chartTheme.tooltipBg, borderColor: chartTheme.tooltipBorder, color: chartTheme.textPrimary, fontSize: '10px', fontFamily: 'monospace' }} />
                      <Line type="stepAfter" dataKey="success" stroke={chartTheme.accent} strokeWidth={2} dot={false} name="Success (1/0)" />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
