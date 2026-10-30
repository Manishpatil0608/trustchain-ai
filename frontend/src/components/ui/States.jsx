import React from 'react';
import { ShieldAlert, ServerOff, Loader2, Database, Shield, CheckCircle2, AlertTriangle, Lock, XCircle } from 'lucide-react';

export function LoadingState({ message = "Loading Operations Center..." }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-[400px] text-tc-cyan animate-pulse font-mono">
            <Loader2 size={40} className="mb-4 animate-spin text-tc-cyan opacity-90" />
            <p className="tracking-widest uppercase text-xs">{message}</p>
        </div>
    );
}

export function ErrorState({ error, retry }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-[400px] text-rose-400 font-mono text-center">
            <ServerOff size={44} className="mb-4 text-rose-500 opacity-90" />
            <h3 className="text-base font-bold tracking-widest uppercase mb-2 text-slate-100">BACKEND API OFFLINE</h3>
            <p className="text-xs text-slate-400 max-w-md mb-6">{error || 'Unable to connect to TrustChain-AI backend.'}<br/>Target: http://localhost:8050/api/v1</p>
            {retry && (
                <button onClick={retry} className="px-5 py-2 border border-rose-500/40 bg-rose-950/30 rounded hover:bg-rose-900/40 text-rose-300 uppercase tracking-widest text-xs transition-colors shadow-[0_0_15px_rgba(239,68,68,0.2)]">
                    Retry Connection
                </button>
            )}
        </div>
    );
}

export function EmptyState({ message = "No data available in the current context." }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-[220px] text-slate-500 dark:text-slate-400 font-mono text-center border border-dashed border-slate-300 dark:border-slate-800 rounded-lg bg-slate-50 dark:bg-[#080b13]/60 p-6">
            <Database size={28} className="mb-3 text-slate-400 dark:text-slate-600" />
            <p className="text-xs uppercase tracking-widest">{message}</p>
        </div>
    );
}

export function TrustBadge({ state }) {
    const s = (state || 'UNKNOWN').toUpperCase();
    switch (s) {
        case 'TRUSTED':
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/80 dark:text-emerald-400 dark:border-emerald-800/80 shadow-xs dark:shadow-[0_0_10px_rgba(16,185,129,0.15)]">
                    <CheckCircle2 size={11} /> TRUSTED
                </span>
            );
        case 'SUSPICIOUS':
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950/80 dark:text-amber-400 dark:border-amber-800/80 shadow-xs dark:shadow-[0_0_10px_rgba(245,158,11,0.15)]">
                    <AlertTriangle size={11} /> SUSPICIOUS
                </span>
            );
        case 'QUARANTINED':
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-300 dark:bg-rose-950/80 dark:text-rose-400 dark:border-rose-800/80 shadow-xs dark:shadow-[0_0_10px_rgba(239,68,68,0.15)]">
                    <ShieldAlert size={11} /> QUARANTINED
                </span>
            );
        case 'REVOKED':
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-300 dark:bg-slate-900 dark:text-slate-400 dark:border-slate-700">
                    <XCircle size={11} /> REVOKED
                </span>
            );
        default:
            return (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-300 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700">
                    {s}
                </span>
            );
    }
}

export function StatusBadge({ status }) {
    const s = (status || 'UNKNOWN').toUpperCase();
    if (s === 'AVAILABLE') {
        return <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/60 dark:text-emerald-400 dark:border-emerald-800/60">AVAILABLE</span>;
    }
    if (s === 'BUSY') {
        return <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950/60 dark:text-amber-400 dark:border-amber-800/60">BUSY</span>;
    }
    return <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-300 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700">{s}</span>;
}

export function HealthBadge({ status }) {
    const raw = status || 'UNKNOWN';
    const s = raw.toUpperCase();

    // Healthy / Synced / Operational states
    if (['HEALTHY', 'ONLINE', 'SYNCED', 'OPERATIONAL', 'OK', 'AVAILABLE', 'CONNECTED'].includes(s)) {
        return (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950/60 dark:text-emerald-400 dark:border-emerald-800/60 shadow-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> {s}
            </span>
        );
    }

    // Degraded / Warning states
    if (['DEGRADED', 'UNHEALTHY', 'WARNING', 'SLOW'].includes(s)) {
        return (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950/60 dark:text-amber-400 dark:border-amber-800/60 shadow-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span> {s}
            </span>
        );
    }

    // Unknown / Initializing states
    if (['UNKNOWN', 'INITIALIZING', 'PENDING', 'CHECKING'].includes(s)) {
        return (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-300 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-400"></span> {s}
            </span>
        );
    }

    // Offline / Error / Unreachable states
    return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[9px] font-mono font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-300 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-800/60 shadow-xs">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span> {s}
        </span>
    );
}

export function TrustProgressBar({ score = 0, state = 'TRUSTED' }) {
    const numScore = typeof score === 'number' ? score : parseFloat(score) || 0;
    const clamped = Math.min(1.0, Math.max(0.0, numScore));
    const percentage = Math.round(clamped * 100);

    let barColor = 'bg-emerald-500 dark:bg-emerald-400';
    if (state === 'SUSPICIOUS' || (clamped >= 0.50 && clamped < 0.80)) barColor = 'bg-amber-500 dark:bg-amber-400';
    if (state === 'QUARANTINED' || clamped < 0.50) barColor = 'bg-rose-500';
    if (state === 'REVOKED') barColor = 'bg-slate-500';

    const blocksCount = 10;
    const filledBlocks = Math.round(clamped * blocksCount);
    const asciiBlocks = '█'.repeat(filledBlocks) + '░'.repeat(blocksCount - filledBlocks);

    return (
        <div className="space-y-1 font-mono">
            <div className="flex items-center justify-between text-[11px]">
                <span className="font-bold text-slate-900 dark:text-slate-200">{numScore.toFixed(4)}</span>
                <span className="text-[9px] text-slate-500 dark:text-slate-400 tracking-tighter">{asciiBlocks}</span>
            </div>
            <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-900 rounded-full overflow-hidden border border-slate-300 dark:border-slate-800">
                <div className={`h-full ${barColor} transition-all duration-500`} style={{ width: `${percentage}%` }}></div>
            </div>
        </div>
    );
}

export function SectionHeader({ icon: Icon, title, subtitle, badge }) {
    return (
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-5 mb-6">
            <div>
                <div className="flex items-center gap-2 text-[10px] font-mono text-tc-cyan uppercase tracking-widest mb-1 font-semibold">
                    {Icon && <Icon size={13} />} SOC MONITORING CONSOLE
                </div>
                <h1 className="text-xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">{title}</h1>
                {subtitle && <p className="text-slate-600 dark:text-slate-400 text-xs mt-0.5">{subtitle}</p>}
            </div>
            {badge && (
                <span className="text-[10px] font-mono bg-tc-cyan/10 text-tc-cyan px-2.5 py-1 rounded border border-tc-cyan/30 uppercase tracking-widest self-start md:self-center font-semibold">
                    {badge}
                </span>
            )}
        </div>
    );
}
