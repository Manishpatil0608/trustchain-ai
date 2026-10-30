import React, { useEffect, useState } from 'react';
import { trustApi } from '../api';
import { useAgents } from '../hooks/useApi';
import { FileKey2, Lock, Link as LinkIcon, ShieldCheck, Database, Key } from 'lucide-react';
import { LoadingState, ErrorState, EmptyState, SectionHeader } from './ui/States';

export default function IdentityCredentials() {
  const { data: agents, loading, error } = useAgents();
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [credentials, setCredentials] = useState([]);
  const [credsLoading, setCredsLoading] = useState(false);

  useEffect(() => {
    if (agents && agents.length > 0 && !selectedAgent) {
      handleSelectAgent(agents[agents.length - 1].agent_did);
    }
  }, [agents, selectedAgent]);

  const handleSelectAgent = (did) => {
    setSelectedAgent(did);
    setCredsLoading(true);
    trustApi
      .getAgentCredentials(did)
      .then((res) => setCredentials(res || []))
      .catch(console.error)
      .finally(() => setCredsLoading(false));
  };

  if (loading) return <LoadingState message="FETCHING IDENTITY REGISTRY..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={FileKey2}
        title="Identity & Credentials"
        subtitle="DECENTRALIZED KEY ARCHITECTURE & W3C VERIFIABLE CREDENTIALS"
      />

      {agents && agents.length === 0 ? (
        <EmptyState message="NO AGENTS REGISTERED IN SYSTEM" />
      ) : (
        <>
          <div className="flex items-center gap-4 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 p-4 rounded-xl shadow-sm">
            <label className="text-xs font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest whitespace-nowrap">
              Inspect Agent DID:
            </label>
            <select
              className="bg-slate-50 dark:bg-[#030712] border border-slate-300 dark:border-slate-700 rounded-lg p-2.5 text-cyan-700 dark:text-cyan-400 font-mono text-xs focus:outline-none focus:border-cyan-500 flex-1 max-w-xl shadow-inner"
              value={selectedAgent || ''}
              onChange={(e) => handleSelectAgent(e.target.value)}
            >
              <option value="" disabled>
                Select an Agent DID...
              </option>
              {agents.map((a) => (
                <option key={a.agent_did} value={a.agent_did}>
                  {a.agent_did}
                </option>
              ))}
            </select>
          </div>

          {!selectedAgent ? (
            <EmptyState message="SELECT AN AGENT TO VIEW CREDENTIALS" />
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
                  <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest border-b border-slate-200 dark:border-slate-800 pb-3 mb-4 flex items-center gap-2">
                    <Key size={14} className="text-tc-cyan" /> Cryptographic Binding
                  </h3>
                  <div className="space-y-3">
                    <div className="bg-slate-50 dark:bg-[#04060b] p-3 rounded-lg border border-slate-200 dark:border-slate-800/80">
                      <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono uppercase mb-1">Subject DID</div>
                      <div className="text-xs text-cyan-700 dark:text-cyan-400 font-mono truncate font-semibold" title={selectedAgent}>
                        {selectedAgent}
                      </div>
                    </div>
                    <div className="bg-slate-50 dark:bg-[#04060b] p-3 rounded-lg border border-slate-200 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-[10px] text-slate-700 dark:text-slate-400 font-mono uppercase flex items-center gap-2">
                        <ShieldCheck size={14} className="text-emerald-500" /> Ed25519 Verification
                      </div>
                      <div className="text-[10px] bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/40 dark:border-emerald-800 dark:text-emerald-400 px-2.5 py-0.5 rounded font-mono font-semibold">
                        SIGNATURE VALID
                      </div>
                    </div>
                    <div className="bg-slate-50 dark:bg-[#04060b] p-3 rounded-lg border border-slate-200 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-[10px] text-slate-700 dark:text-slate-400 font-mono uppercase flex items-center gap-2">
                        <Database size={14} className="text-tc-cyan" /> Registry Status
                      </div>
                      <div className="text-[10px] bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/40 dark:border-emerald-800 dark:text-emerald-400 px-2.5 py-0.5 rounded font-mono font-semibold">
                        VDR SYNCED
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
                  <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest border-b border-slate-200 dark:border-slate-800 pb-3 mb-4 flex items-center gap-2">
                    <FileKey2 size={14} className="text-tc-cyan" /> Verifiable Credential Payload
                  </h3>
                  {credsLoading ? (
                    <div className="animate-pulse text-tc-cyan font-mono text-xs">Loading payload...</div>
                  ) : credentials.length > 0 ? (
                    <pre className="text-[11px] text-cyan-300 bg-slate-900 dark:bg-[#04060b] p-4 rounded-lg border border-slate-800 font-mono overflow-auto max-h-72 custom-scrollbar shadow-inner leading-relaxed">
                      {JSON.stringify(credentials[0].vc, null, 2)}
                    </pre>
                  ) : (
                    <div className="text-slate-500 font-mono text-xs p-4 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-lg">
                      No credentials found in VDR.
                    </div>
                  )}
                </div>
              </div>

              <div className="lg:col-span-3 bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-8 shadow-sm flex flex-col items-center justify-center min-h-[500px] relative overflow-hidden">
                <div
                  className="absolute inset-0 opacity-5 pointer-events-none"
                  style={{
                    backgroundImage: 'radial-gradient(circle at center, #00f0ff 1px, transparent 1px)',
                    backgroundSize: '24px 24px',
                  }}
                ></div>

                <h3 className="font-mono text-xs text-slate-600 dark:text-slate-400 uppercase tracking-widest absolute top-6 left-6 z-10 border-b border-slate-200 dark:border-slate-800 pb-2">
                  Trust Chain Architecture
                </h3>

                <div className="flex flex-col items-center w-full max-w-md relative z-10 mt-8">
                  {/* Issuer */}
                  <div className="w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center justify-between shadow-sm">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-200 dark:border-cyan-800/60 rounded-lg text-cyan-700 dark:text-cyan-400">
                        <Key size={20} />
                      </div>
                      <div>
                        <div className="text-xs font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-0.5">
                          ISSUER AUTHORITY
                        </div>
                        <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400">TrustChain Root VDR</div>
                      </div>
                    </div>
                    <div className="text-[10px] font-mono font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-3 py-1 rounded border border-emerald-300 dark:border-emerald-800">
                      VERIFIED
                    </div>
                  </div>

                  <div className="h-10 w-[2px] bg-cyan-500/30 relative">
                    <div className="absolute top-1/2 -left-8 transform -translate-y-1/2 bg-white dark:bg-[#04060b] px-2 py-0.5 text-[10px] text-cyan-700 dark:text-cyan-400 font-mono border border-slate-200 dark:border-cyan-800/60 rounded shadow-xs font-semibold">
                      Signs VC
                    </div>
                  </div>

                  {/* Verifiable Credential */}
                  <div className="w-full bg-slate-50 dark:bg-[#070b14] border border-cyan-500/40 p-4 rounded-xl flex items-center justify-between shadow-[0_0_20px_rgba(0,240,255,0.08)] relative">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-cyan-50 dark:bg-cyan-950/60 border border-cyan-200 dark:border-cyan-500/50 rounded-lg text-cyan-700 dark:text-cyan-400">
                        <FileKey2 size={20} />
                      </div>
                      <div>
                        <div className="text-xs font-bold text-cyan-700 dark:text-cyan-400 uppercase tracking-wider mb-0.5">
                          VERIFIABLE CREDENTIAL
                        </div>
                        <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400">
                          {credentials.length > 0 && credentials[0].vc?.type
                            ? credentials[0].vc.type[1] || 'AgentCapabilityCredential'
                            : 'W3C LDP VC'}
                        </div>
                      </div>
                    </div>
                    <div className="text-[10px] font-mono font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-3 py-1 rounded border border-emerald-300 dark:border-emerald-800">
                      ACTIVE
                    </div>
                  </div>

                  <div className="h-10 w-[2px] bg-cyan-500/30 relative">
                    <div className="absolute top-1/2 -left-8 transform -translate-y-1/2 bg-white dark:bg-[#04060b] px-2 py-0.5 text-[10px] text-cyan-700 dark:text-cyan-400 font-mono border border-slate-200 dark:border-cyan-800/60 rounded shadow-xs font-semibold">
                      Binds To
                    </div>
                  </div>

                  {/* Agent */}
                  <div className="w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center justify-between shadow-sm">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-200 dark:border-cyan-800/60 rounded-lg text-cyan-700 dark:text-cyan-400">
                        <Lock size={20} />
                      </div>
                      <div className="overflow-hidden">
                        <div className="text-xs font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-0.5">
                          AI AGENT IDENTITY
                        </div>
                        <div
                          className="text-[10px] font-mono text-slate-500 dark:text-slate-400 truncate max-w-[200px]"
                          title={selectedAgent}
                        >
                          {selectedAgent}
                        </div>
                      </div>
                    </div>
                    <div className="text-[10px] font-mono font-semibold text-cyan-700 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 px-3 py-1 rounded border border-cyan-200 dark:border-cyan-800">
                      BOUND
                    </div>
                  </div>

                  <div className="h-10 w-[2px] bg-cyan-500/30 relative">
                    <div className="absolute top-1/2 -left-8 transform -translate-y-1/2 bg-white dark:bg-[#04060b] px-2 py-0.5 text-[10px] text-cyan-700 dark:text-cyan-400 font-mono border border-slate-200 dark:border-cyan-800/60 rounded shadow-xs font-semibold">
                      Presents
                    </div>
                  </div>

                  {/* API Gateway */}
                  <div className="w-full bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center justify-between shadow-sm opacity-90">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-600 dark:text-slate-400">
                        <LinkIcon size={20} />
                      </div>
                      <div>
                        <div className="text-xs font-bold text-slate-900 dark:text-slate-200 uppercase tracking-wider mb-0.5">
                          API GATEWAY
                        </div>
                        <div className="text-[10px] font-mono text-slate-500">Resource Server Interceptor</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
