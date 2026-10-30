import React, { useState, useEffect } from 'react';
import { PlayCircle, ShieldAlert, FileKey2, Ban, Lock, Server, Activity, CheckCircle2 } from 'lucide-react';
import { trustApi } from '../api';
import { SectionHeader, TrustBadge } from './ui/States';

export default function DemoVisualizer() {
  const [agents, setAgents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const fetchAgents = () => {
      trustApi
        .getAgents()
        .then((a) => {
          if (isMounted) {
            setAgents(a);
            setError(null);
          }
        })
        .catch((err) => {
          if (isMounted) setError('Backend offline or unreachable');
        });
    };
    fetchAgents();
    const interval = setInterval(fetchAgents, 1500);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const demoAgent = agents.length > 0 ? agents[agents.length - 1] : null;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={PlayCircle}
        title="Research Hypothesis Live Demonstration"
        subtitle="DYNAMIC REPUTATION-BASED ACCESS CONTROL EXPERIMENT"
      />

      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center relative overflow-hidden shadow-sm">
        <div className="text-center mb-8 max-w-2xl">
          <p className="text-cyan-700 dark:text-cyan-400 font-mono text-sm leading-relaxed font-semibold">
            "A valid cryptographic credential can be blocked dynamically after behavioral trust falls below quarantine threshold."
          </p>
        </div>

        {error ? (
          <div className="text-rose-700 dark:text-rose-400 font-mono text-center border border-rose-200 dark:border-rose-800/80 bg-rose-50 dark:bg-rose-950/20 p-8 rounded-xl max-w-md">
            <Server size={40} className="mx-auto mb-3 opacity-80" />
            <h3 className="text-sm font-bold tracking-widest mb-1 uppercase">BACKEND CONNECTION LOST</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400">Ensure FastAPI backend is running on port 8050.</p>
          </div>
        ) : !demoAgent ? (
          <div className="text-cyan-700 dark:text-cyan-400 font-mono flex flex-col items-center border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#04060b] p-10 rounded-xl max-w-md text-center">
            <Server size={40} className="mb-3 opacity-50" />
            <p className="tracking-widest uppercase mb-2 text-xs font-semibold">Awaiting Agent Telemetry Stream...</p>
            <div className="text-[11px] text-slate-500 dark:text-slate-400">
              Trigger agent actions or workflow runs in the Operations Center to observe real-time dynamic enforcement.
            </div>
          </div>
        ) : (
          <div className="w-full max-w-5xl bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 rounded-xl p-8 relative overflow-hidden shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest">Target Agent:</span>
                <span className="text-xs font-mono text-cyan-700 dark:text-cyan-400 font-semibold truncate max-w-xs md:max-w-md">
                  {demoAgent.agent_did}
                </span>
              </div>
              <div className="flex items-center gap-2 px-2.5 py-1 bg-white dark:bg-[#030712] border border-slate-200 dark:border-slate-800 rounded-full shadow-xs">
                <div className="w-2 h-2 rounded-full bg-tc-cyan animate-pulse"></div>
                <span className="text-[10px] text-cyan-700 dark:text-cyan-400 font-mono tracking-widest uppercase font-semibold">LIVE SYNC (1.5s)</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
              {/* Identity Block */}
              <div className="text-center p-6 bg-white dark:bg-[#030712] border border-slate-200 dark:border-slate-800 rounded-xl shadow-xs">
                <FileKey2 size={28} className="mx-auto text-tc-cyan mb-3" />
                <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 mb-2 uppercase tracking-widest font-semibold">
                  1. Cryptographic Identity
                </h3>
                <div className="mt-4">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800 text-[10px] font-mono tracking-wider font-semibold">
                    <Lock size={12} /> Ed25519 VERIFIED
                  </span>
                </div>
              </div>

              {/* Trust Engine Block */}
              <div
                className={`text-center p-6 bg-white dark:bg-[#030712] border-2 rounded-xl shadow-xs transition-all duration-500 ${
                  demoAgent.trust_state === 'TRUSTED'
                    ? 'border-emerald-500/50'
                    : demoAgent.trust_state === 'SUSPICIOUS'
                    ? 'border-amber-500/50'
                    : 'border-rose-500/50'
                }`}
              >
                <Activity
                  size={28}
                  className={`mx-auto mb-3 ${
                    demoAgent.trust_state === 'TRUSTED'
                      ? 'text-emerald-500 dark:text-emerald-400'
                      : demoAgent.trust_state === 'SUSPICIOUS'
                      ? 'text-amber-500 dark:text-amber-400'
                      : 'text-rose-500 dark:text-rose-400'
                  }`}
                />
                <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 mb-2 uppercase tracking-widest font-semibold">
                  2. Behavioral Trust Score
                </h3>
                <div className="text-3xl font-mono font-bold text-slate-900 dark:text-slate-100 mb-2">
                  {demoAgent.trust_score.toFixed(4)}
                </div>
                <TrustBadge state={demoAgent.trust_state} />
              </div>

              {/* Policy Enforcement Block */}
              <div
                className={`text-center p-6 border-2 rounded-xl shadow-xs transition-all duration-500 ${
                  demoAgent.trust_state === 'QUARANTINED' || demoAgent.trust_state === 'REVOKED'
                    ? 'border-rose-300 dark:border-rose-500/70 bg-rose-50 dark:bg-rose-950/20'
                    : 'border-emerald-300 dark:border-emerald-500/50 bg-emerald-50 dark:bg-emerald-950/10'
                }`}
              >
                {demoAgent.trust_state === 'QUARANTINED' || demoAgent.trust_state === 'REVOKED' ? (
                  <>
                    <Ban size={28} className="mx-auto text-rose-500 dark:text-rose-400 mb-3 animate-pulse" />
                    <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 mb-2 uppercase tracking-widest font-semibold">
                      3. Gateway Policy Enforcement
                    </h3>
                    <div className="text-sm font-mono font-bold text-rose-700 dark:text-rose-400 tracking-wider mb-1">
                      HTTP 403 FORBIDDEN
                    </div>
                    <p className="text-[10px] font-mono text-rose-600 dark:text-rose-300">Access Intercepted & Quarantined</p>
                  </>
                ) : (
                  <>
                    <CheckCircle2 size={28} className="mx-auto text-emerald-500 dark:text-emerald-400 mb-3" />
                    <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 mb-2 uppercase tracking-widest font-semibold">
                      3. Gateway Policy Enforcement
                    </h3>
                    <div className="text-sm font-mono font-bold text-emerald-700 dark:text-emerald-400 tracking-wider mb-1">
                      HTTP 200 ALLOWED
                    </div>
                    <p className="text-[10px] font-mono text-emerald-600 dark:text-emerald-300">Request Permitted</p>
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
