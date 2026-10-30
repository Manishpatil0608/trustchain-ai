import React from 'react';
import { GitMerge, ShieldAlert, Ban, CheckCircle2, ShieldOff } from 'lucide-react';
import { SectionHeader } from './ui/States';

export default function StateTransitionMap() {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <SectionHeader
        icon={GitMerge}
        title="State Transition Map"
        subtitle="TRUST ENGINE FINITE STATE AUTOMATA & THRESHOLDS"
      />

      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center min-h-[580px] relative overflow-hidden shadow-sm transition-colors">
        {/* Background Grid */}
        <div
          className="absolute inset-0 opacity-5 pointer-events-none"
          style={{
            backgroundImage:
              'linear-gradient(#00f0ff 1px, transparent 1px), linear-gradient(90deg, #00f0ff 1px, transparent 1px)',
            backgroundSize: '32px 32px',
          }}
        ></div>

        <div className="relative z-10 w-full max-w-3xl">
          {/* Top Row: Trusted */}
          <div className="flex justify-center mb-16">
            <div className="bg-emerald-50 border-2 border-emerald-400 dark:bg-emerald-950/30 dark:border-emerald-500/50 p-6 rounded-2xl w-72 text-center shadow-xs dark:shadow-[0_0_25px_rgba(16,185,129,0.15)]">
              <CheckCircle2 size={32} className="mx-auto text-emerald-600 dark:text-emerald-400 mb-2" />
              <h3 className="font-bold text-emerald-700 dark:text-emerald-400 text-lg tracking-widest mb-1">TRUSTED</h3>
              <p className="text-xs font-mono text-emerald-800 dark:text-emerald-300 font-semibold">T(t) ≥ 0.80</p>
              <div className="mt-2 text-[10px] font-mono text-slate-600 dark:text-slate-400">Full Autonomy & Peer Delegation</div>
            </div>
          </div>

          {/* Middle Row: Suspicious */}
          <div className="flex justify-center mb-16 relative">
            {/* Degradation Arrow Down */}
            <div className="absolute -top-16 left-1/2 transform -translate-x-[50px] flex flex-col items-center">
              <div className="text-[10px] text-amber-600 dark:text-amber-400 font-mono absolute -left-28 top-5 font-semibold">
                Degradation &lt; 0.80
              </div>
              <div className="h-14 w-px bg-amber-500/60 relative">
                <div className="absolute bottom-0 -left-1 w-2 h-2 border-r border-b border-amber-400 transform rotate-45"></div>
              </div>
            </div>
            {/* Recovery Arrow Up */}
            <div className="absolute -top-16 left-1/2 transform translate-x-[50px] flex flex-col items-center">
              <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono absolute -right-28 top-5 font-semibold">
                Recovery ≥ 0.80
              </div>
              <div className="h-14 w-px bg-emerald-500/60 relative">
                <div className="absolute top-0 -left-1 w-2 h-2 border-l border-t border-emerald-400 transform rotate-45"></div>
              </div>
            </div>

            <div className="bg-amber-50 border-2 border-amber-400 dark:bg-amber-950/30 dark:border-amber-500/50 p-6 rounded-2xl w-72 text-center shadow-xs dark:shadow-[0_0_25px_rgba(245,158,11,0.15)]">
              <ShieldAlert size={32} className="mx-auto text-amber-600 dark:text-amber-400 mb-2" />
              <h3 className="font-bold text-amber-700 dark:text-amber-400 text-lg tracking-widest mb-1">SUSPICIOUS</h3>
              <p className="text-xs font-mono text-amber-800 dark:text-amber-300 font-semibold">0.50 ≤ T(t) &lt; 0.80</p>
              <div className="mt-2 text-[10px] font-mono text-slate-600 dark:text-slate-400">Restricted Rate Limits & Auditing</div>
            </div>
          </div>

          {/* Bottom Row: Quarantined */}
          <div className="flex justify-center relative">
            {/* Degradation Arrow Down */}
            <div className="absolute -top-16 left-1/2 transform -translate-x-[50px] flex flex-col items-center">
              <div className="text-[10px] text-rose-600 dark:text-rose-400 font-mono absolute -left-28 top-5 font-semibold">
                Breach &lt; 0.50
              </div>
              <div className="h-14 w-px bg-rose-500/60 relative">
                <div className="absolute bottom-0 -left-1 w-2 h-2 border-r border-b border-rose-400 transform rotate-45"></div>
              </div>
            </div>
            {/* Recovery Arrow Up */}
            <div className="absolute -top-16 left-1/2 transform translate-x-[50px] flex flex-col items-center">
              <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono absolute -right-28 top-5 font-semibold">
                Gradual Recov.
              </div>
              <div className="h-14 w-px bg-emerald-500/60 relative">
                <div className="absolute top-0 -left-1 w-2 h-2 border-l border-t border-emerald-400 transform rotate-45"></div>
              </div>
            </div>

            <div className="bg-rose-50 border-2 border-rose-400 dark:bg-rose-950/30 dark:border-rose-500/50 p-6 rounded-2xl w-72 text-center shadow-xs dark:shadow-[0_0_25px_rgba(244,63,94,0.15)]">
              <Ban size={32} className="mx-auto text-rose-600 dark:text-rose-400 mb-2" />
              <h3 className="font-bold text-rose-700 dark:text-rose-400 text-lg tracking-widest mb-1">QUARANTINED</h3>
              <p className="text-xs font-mono text-rose-800 dark:text-rose-300 font-semibold">T(t) &lt; 0.50</p>
              <div className="mt-2 text-[10px] font-mono text-slate-600 dark:text-slate-400">Zero Execution / Gateway Intercepted</div>
            </div>
          </div>

          {/* Revoked State */}
          <div className="absolute right-0 top-1/2 transform -translate-y-1/2 hidden lg:block">
            <div className="flex items-center gap-3">
              <div className="w-12 h-px bg-slate-300 dark:bg-slate-700 border-t border-dashed"></div>
              <div className="bg-slate-100 border-2 border-slate-300 dark:bg-slate-900/80 dark:border-slate-700 p-4 rounded-xl w-44 text-center opacity-90 shadow-xs">
                <ShieldOff size={24} className="mx-auto text-slate-400 dark:text-slate-500 mb-1" />
                <h3 className="font-bold text-slate-700 dark:text-slate-300 text-xs tracking-widest mb-1">REVOKED</h3>
                <p className="text-[10px] font-mono text-slate-500">Cryptographic Revocation</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}