import React from 'react';
import { GitMerge, ArrowRight, ShieldAlert, Lock, Activity, Ban } from 'lucide-react';
import { useAllAudit } from '../hooks/useApi';
import { LoadingState, ErrorState, EmptyState, SectionHeader, TrustBadge } from './ui/States';

export default function AuditTrail() {
  const { data: audits, loading, error } = useAllAudit();

  if (loading) return <LoadingState message="RECONSTRUCTING AUDIT TIMELINE..." />;
  if (error) return <ErrorState error={error} retry={() => window.location.reload()} />;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={GitMerge}
        title="Security Events & Audit Trail"
        subtitle="TEMPORAL RECORD OF BEHAVIORAL STATE TRANSITIONS"
      />

      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
        {audits && audits.length === 0 ? (
          <EmptyState message="NO STATE TRANSITIONS RECORDED IN AUDIT LOG" />
        ) : (
          <div className="relative border-l-2 border-slate-200 dark:border-slate-800 ml-4 space-y-8 pb-4 before:absolute before:-left-[1px] before:top-0 before:h-full before:w-[2px] before:bg-gradient-to-b before:from-cyan-500 before:to-transparent">
            {audits.map((a, i) => (
              <div key={a.id || i} className="relative pl-8 group">
                {/* Timeline dot */}
                <div className="absolute -left-[11px] top-1.5 w-5 h-5 rounded-full bg-white dark:bg-[#030712] border-2 border-cyan-500 dark:border-cyan-400 flex items-center justify-center shadow-[0_0_10px_rgba(0,240,255,0.4)] group-hover:scale-110 transition-transform">
                  <div className="w-1.5 h-1.5 bg-cyan-500 dark:bg-cyan-400 rounded-full"></div>
                </div>

                <div className="text-[10px] text-slate-500 font-mono mb-2 tracking-widest">
                  {new Date(a.timestamp).toLocaleString()}
                </div>

                <div className="bg-slate-50 dark:bg-[#070b14] border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xs group-hover:border-slate-300 dark:group-hover:border-slate-700 transition-colors">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex-1">
                      <div className="text-[10px] text-cyan-700 dark:text-cyan-400 font-mono mb-1 uppercase tracking-widest font-semibold">
                        AGENT DID
                      </div>
                      <div className="text-xs font-mono text-slate-900 dark:text-slate-200 truncate max-w-md font-semibold" title={a.agent_did}>
                        {a.agent_did}
                      </div>
                    </div>
                    <div className="flex items-center justify-center gap-3 bg-white dark:bg-[#030712] px-4 py-2.5 rounded-lg border border-slate-200 dark:border-slate-800 flex-shrink-0 shadow-xs">
                      <TrustBadge state={a.previous_state} />
                      <ArrowRight size={14} className="text-tc-cyan" />
                      <TrustBadge state={a.new_state} />
                    </div>
                  </div>
                  <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800/80 text-xs font-mono text-slate-700 dark:text-slate-300 flex items-start gap-2">
                    <span className="text-slate-500 uppercase tracking-widest text-[10px] shrink-0 mt-0.5">
                      Trigger Reason:
                    </span>
                    <span className="text-slate-700 dark:text-slate-300 leading-relaxed">{a.reason}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
