import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Shield, Server, Bell, RefreshCw, Lock, CheckCircle2, User, Sun, Moon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { trustApi } from '../api';

export default function TopBar({ onRefresh, isRefreshing }) {
    const location = useLocation();
    const { user } = useAuth();
    const { theme, toggleTheme, isDark } = useTheme();
    const [apiHealth, setApiHealth] = useState('ONLINE');

    useEffect(() => {
        let isMounted = true;
        trustApi.getHealth()
            .then((res) => {
                if (!isMounted) return;
                if (res?.status === 'ok') setApiHealth('ONLINE');
                else if (res?.status === 'degraded') setApiHealth('DEGRADED');
                else setApiHealth('DEGRADED');
            })
            .catch(() => {
                if (isMounted) setApiHealth('OFFLINE');
            });
        return () => { isMounted = false; };
    }, [isRefreshing]);

    const getBreadcrumb = (path) => {
        switch (path) {
            case '/': return { group: 'OVERVIEW', title: 'Dashboard Operations Center' };
            case '/agents': return { group: 'AGENTS', title: 'Agent Registry & Posture' };
            case '/discovery': return { group: 'AGENTS', title: 'Agent Discovery & Selection' };
            case '/matching': return { group: 'AGENTS', title: 'Trust-Aware Agent Matching' };
            case '/analytics': return { group: 'TRUST INTELLIGENCE', title: 'Trust Analytics & Engine Math' };
            case '/telemetry': return { group: 'TRUST INTELLIGENCE', title: 'Behavioral Telemetry Stream' };
            case '/transitions': return { group: 'TRUST INTELLIGENCE', title: 'State Transition Machine' };
            case '/authorization': return { group: 'TRUST INTELLIGENCE', title: 'Adaptive Authorization Policy' };
            case '/collaboration': return { group: 'COLLABORATION', title: 'Agent Collaboration Console' };
            case '/workflows': return { group: 'COLLABORATION', title: 'Multi-Agent Workflow Pipelines' };
            case '/identity': return { group: 'IDENTITY', title: 'DIDs & Verifiable Credentials' };
            case '/audit': return { group: 'SECURITY', title: 'Tamper-Evident Audit Trail' };
            case '/health': return { group: 'SECURITY', title: 'System Infrastructure Health' };
            case '/admin/users': return { group: 'ADMINISTRATION', title: 'User Access & RBAC' };
            case '/demo': return { group: 'DEMONSTRATION', title: 'Live End-to-End Runbook' };
            default:
                if (path.startswith('/agents/')) return { group: 'AGENTS', title: 'Agent Security Profile' };
                return { group: 'TRUSTCHAIN-AI', title: 'Security Operations Center' };
        }
    };

    const bc = getBreadcrumb(location.pathname);

    return (
        <header className="h-14 border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-[#080b13]/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs dark:shadow-md transition-colors">
            {/* Left Breadcrumb */}
            <div className="flex items-center gap-3">
                <span className="text-[10px] font-mono uppercase tracking-widest text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900/80 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-800 font-semibold">
                    {bc.group}
                </span>
                <span className="text-slate-400 dark:text-slate-600 font-mono text-xs">/</span>
                <h2 className="text-xs font-bold font-mono tracking-wider text-slate-900 dark:text-slate-100 uppercase">{bc.title}</h2>
            </div>

            {/* Right Security System Status & Controls */}
            <div className="flex items-center gap-4">
                {apiHealth === 'ONLINE' && (
                    <div className="flex items-center gap-2 px-2.5 py-1 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800/60 rounded text-[10px] font-mono text-emerald-700 dark:text-emerald-400 font-bold uppercase tracking-wider">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 dark:bg-emerald-400 animate-pulse shadow-[0_0_8px_#10b981]"></span>
                        API ONLINE (:8050)
                    </div>
                )}
                {apiHealth === 'DEGRADED' && (
                    <div className="flex items-center gap-2 px-2.5 py-1 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800/60 rounded text-[10px] font-mono text-amber-700 dark:text-amber-400 font-bold uppercase tracking-wider">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-500 dark:bg-amber-400 animate-pulse shadow-[0_0_8px_#f59e0b]"></span>
                        API DEGRADED (:8050)
                    </div>
                )}
                {apiHealth === 'OFFLINE' && (
                    <div className="flex items-center gap-2 px-2.5 py-1 bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-800/60 rounded text-[10px] font-mono text-rose-700 dark:text-rose-400 font-bold uppercase tracking-wider">
                        <span className="w-1.5 h-1.5 rounded-full bg-rose-500 dark:bg-rose-400 animate-pulse shadow-[0_0_8px_#ef4444]"></span>
                        API OFFLINE (:8050)
                    </div>
                )}

                {user && (
                    <div className="flex items-center gap-2 px-2.5 py-1 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded text-[10px] font-mono text-slate-800 dark:text-slate-300">
                        <User size={12} className="text-tc-cyan" />
                        <span className="font-bold">{user.username}</span>
                        <span className="text-slate-400 dark:text-slate-500">|</span>
                        <span className="text-tc-cyan uppercase font-bold">{user.role}</span>
                    </div>
                )}

                {/* Theme Toggle Button */}
                <button
                    onClick={toggleTheme}
                    title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                    aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                    className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-slate-700 dark:text-slate-300 rounded hover:border-tc-cyan transition-all text-[10px] font-mono shadow-xs cursor-pointer font-semibold"
                >
                    {isDark ? (
                        <>
                            <Sun size={12} className="text-amber-400" />
                            <span className="hidden sm:inline">LIGHT</span>
                        </>
                    ) : (
                        <>
                            <Moon size={12} className="text-cyan-600" />
                            <span className="hidden sm:inline">DARK</span>
                        </>
                    )}
                </button>

                {onRefresh && (
                    <button
                        onClick={onRefresh}
                        title="Refresh SOC Telemetry"
                        className="p-1.5 bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-slate-700 dark:text-slate-300 rounded hover:border-tc-cyan transition-colors"
                    >
                        <RefreshCw size={13} className={isRefreshing ? 'animate-spin text-tc-cyan' : ''} />
                    </button>
                )}
            </div>
        </header>
    );
}
