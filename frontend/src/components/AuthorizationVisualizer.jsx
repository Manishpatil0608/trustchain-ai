import React, { useState, useEffect } from 'react';
import { Lock, ShieldAlert, Ban, CheckCircle2, FileJson, ArrowRight, ShieldCheck } from 'lucide-react';
import { useAgents } from '../hooks/useApi';
import { LoadingState, ErrorState, EmptyState, SectionHeader, TrustBadge } from './ui/States';

export default function AuthorizationVisualizer() {
  const { data: agents, loading, error } = useAgents();
  const [selectedAgent, setSelectedAgent] = useState(null);

  useEffect(() => {
    if (agents && agents.length > 0 && !selectedAgent) {
      setSelectedAgent(agents[agents.length - 1]);
    }
  }, [agents, selectedAgent]);

  const handleSelect = (e) => {
    const a = agents.find((ag) => ag.agent_did === e.target.value);
    setSelectedAgent(a);
  };

  if (loading) return <LoadingState message="INITIALIZING POLICY ENGINE..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={Lock}
        title="Adaptive Authorization"
        subtitle="DYNAMIC POLICY ENFORCEMENT & GATEWAY INTERCEPTION"
      />

      {agents && agents.length === 0 ? (
        <EmptyState message="NO AGENTS DETECTED IN SYSTEM" />
      ) : (
        <>
          <div className="flex items-center gap-4 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-xl shadow-sm">
            <label className="text-xs font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest whitespace-nowrap">
              Evaluate Subject DID:
            </label>
            <select
              className="bg-slate-50 dark:bg-[#030712] border border-slate-300 dark:border-slate-700 rounded-lg p-2.5 text-cyan-700 dark:text-cyan-400 font-mono text-xs focus:outline-none focus:border-cyan-500 flex-1 max-w-xl shadow-inner"
              value={selectedAgent?.agent_did || ''}
              onChange={handleSelect}
            >
              <option value="" disabled>
                Select an Agent DID...
              </option>
              {agents.map((a) => (
                <option key={a.agent_did} value={a.agent_did}>
                  {a.agent_did} ({a.trust_state} - {a.trust_score.toFixed(4)})
                </option>
              ))}
            </select>
          </div>

          {!selectedAgent ? (
            <EmptyState message="SELECT AN AGENT TO VIEW POLICY EVALUATION" />
          ) : (
            <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-8 max-w-5xl mx-auto flex flex-col items-center shadow-sm relative overflow-hidden">
              <div
                className="absolute inset-0 opacity-5 pointer-events-none"
                style={{
                  backgroundImage:
                    'linear-gradient(#00f0ff 1px, transparent 1px), linear-gradient(90deg, #00f0ff 1px, transparent 1px)',
                  backgroundSize: '32px 32px',
                }}
              ></div>

              <div className="w-full flex items-center justify-between border-b border-slate-200 dark:border-slate-800/80 pb-4 mb-8 relative z-10">
                <span className="text-xs font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest">
                  Zero-Trust Dynamic Enforcement Pipeline
                </span>
                <span className="text-[11px] font-mono text-cyan-700 dark:text-cyan-400 truncate max-w-md font-semibold">
                  {selectedAgent.agent_did}
                </span>
              </div>

              <div className="flex flex-col md:flex-row items-center justify-between w-full relative z-10 gap-8 md:gap-4 py-4">
                {/* Step 1: Credential */}
                <div className="flex flex-col items-center flex-1 w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center shadow-xs">
                  <div className="w-16 h-16 rounded-full bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-300 dark:border-emerald-500/40 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.15)] mb-3">
                    <FileJson size={28} />
                  </div>
                  <div className="text-xs font-bold text-slate-900 dark:text-slate-200 uppercase tracking-wider mb-1">
                    1. Identity Credential
                  </div>
                  <div className="text-[10px] font-mono font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2.5 py-1 rounded border border-emerald-300 dark:border-emerald-800">
                    Ed25519 VERIFIED
                  </div>
                </div>

                <ArrowRight className="text-slate-400 dark:text-slate-600 flex-shrink-0 hidden md:block" size={24} />

                {/* Step 2: Trust Engine */}
                <div className="flex flex-col items-center flex-1 w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center shadow-xs">
                  <div
                    className={`w-16 h-16 rounded-full border flex items-center justify-center mb-3 transition-all duration-500 ${
                      selectedAgent.trust_state === 'TRUSTED'
                        ? 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-500/40 text-emerald-600 dark:text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.15)]'
                        : selectedAgent.trust_state === 'SUSPICIOUS'
                        ? 'bg-amber-50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-500/40 text-amber-600 dark:text-amber-400 shadow-[0_0_15px_rgba(245,158,11,0.15)]'
                        : 'bg-rose-50 dark:bg-rose-950/30 border-rose-300 dark:border-rose-500/40 text-rose-600 dark:text-rose-400 shadow-[0_0_15px_rgba(244,63,94,0.15)]'
                    }`}
                  >
                    <ShieldAlert size={28} />
                  </div>
                  <div className="text-xs font-bold text-slate-900 dark:text-slate-200 uppercase tracking-wider mb-1">
                    2. Behavioral Trust
                  </div>
                  <div className="flex flex-col items-center gap-1 mt-0.5">
                    <span className="text-xs font-mono font-bold text-slate-900 dark:text-slate-100">
                      T(t) = {selectedAgent.trust_score.toFixed(4)}
                    </span>
                    <TrustBadge state={selectedAgent.trust_state} />
                  </div>
                </div>

                <ArrowRight className="text-slate-400 dark:text-slate-600 flex-shrink-0 hidden md:block" size={24} />

                {/* Step 3: Gateway Policy */}
                <div className="flex flex-col items-center flex-1 w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center shadow-xs">
                  <div
                    className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-3 transition-all duration-500 ${
                      selectedAgent.trust_state === 'QUARANTINED' ||
                      selectedAgent.trust_state === 'REVOKED'
                        ? 'bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-500/50 text-rose-600 dark:text-rose-400 shadow-[0_0_20px_rgba(244,63,94,0.3)]'
                        : selectedAgent.trust_state === 'SUSPICIOUS'
                        ? 'bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-500/50 text-amber-600 dark:text-amber-400 shadow-[0_0_20px_rgba(245,158,11,0.2)]'
                        : 'bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-500/50 text-emerald-600 dark:text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.2)]'
                    }`}
                  >
                    {selectedAgent.trust_state === 'QUARANTINED' ||
                    selectedAgent.trust_state === 'REVOKED' ? (
                      <Ban size={32} className="animate-pulse" />
                    ) : selectedAgent.trust_state === 'SUSPICIOUS' ? (
                      <ShieldAlert size={32} />
                    ) : (
                      <CheckCircle2 size={32} />
                    )}
                  </div>
                  <div className="text-xs font-bold text-slate-900 dark:text-slate-200 uppercase tracking-wider mb-1">
                    3. Gateway Authorization
                  </div>
                  <div
                    className={`text-[11px] font-mono px-3 py-1 rounded font-bold ${
                      selectedAgent.trust_state === 'QUARANTINED' ||
                      selectedAgent.trust_state === 'REVOKED'
                        ? 'text-rose-700 bg-rose-50 border border-rose-300 dark:text-rose-400 dark:bg-rose-950/60 dark:border-rose-800'
                        : selectedAgent.trust_state === 'SUSPICIOUS'
                        ? 'text-amber-700 bg-amber-50 border border-amber-300 dark:text-amber-400 dark:bg-amber-950/60 dark:border-amber-800'
                        : 'text-emerald-700 bg-emerald-50 border border-emerald-300 dark:text-emerald-400 dark:bg-emerald-950/60 dark:border-emerald-800'
                    }`}
                  >
                    {selectedAgent.trust_state === 'QUARANTINED' ||
                    selectedAgent.trust_state === 'REVOKED'
                      ? 'HTTP 403 FORBIDDEN'
                      : selectedAgent.trust_state === 'SUSPICIOUS'
                      ? 'RESTRICTED / MONITORED'
                      : 'HTTP 200 ALLOWED'}
                  </div>
                  <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 mt-2">
                    {selectedAgent.trust_state === 'QUARANTINED' ||
                    selectedAgent.trust_state === 'REVOKED'
                      ? 'All protected operations blocked'
                      : selectedAgent.trust_state === 'SUSPICIOUS'
                      ? 'Privileged ops denied (HTTP 403), standard tasks audited'
                      : 'Full privileges granted for standard & orchestration'}
                  </div>
                </div>
              </div>

              <div className="mt-8 bg-slate-50 dark:bg-[#04060b] border border-slate-200 dark:border-slate-800 p-5 rounded-lg w-full text-center relative z-10 shadow-xs">
                <h4 className="text-tc-cyan font-mono text-[11px] tracking-widest uppercase mb-2 font-bold">
                  Adaptive Policy Enforcement Rationale
                </h4>
                <p className="text-slate-600 dark:text-slate-400 text-xs leading-relaxed max-w-3xl mx-auto">
                  A cryptographically valid credential alone does <strong className="text-slate-900 dark:text-slate-200">NOT</strong> guarantee resource access. The Adaptive Authorization interceptor continuously queries temporal trust score <code className="text-tc-cyan font-bold">T(t)</code>. If behavioral telemetry degrades to <strong className="text-amber-600 dark:text-amber-400">SUSPICIOUS</strong> (0.50 &le; T &lt; 0.80), privileged operations (workflows, orchestration, delegation) are intercepted with HTTP 403 while standard operations remain permitted under heightened monitoring. If trust drops below quarantine threshold (&lt;0.50) or is administratively REVOKED, all protected gateway operations are immediately denied.
                </p>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
