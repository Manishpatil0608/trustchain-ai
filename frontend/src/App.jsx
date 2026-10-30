import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  Shield, Activity, Users, PlayCircle, Server, Lock, Database, GitMerge, FileKey2, 
  Layers, GitBranch, UserCheck, LogOut, Search, Sliders, CheckCircle2, Sun, Moon 
} from 'lucide-react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import TopBar from './components/TopBar';
import LoginPage from './components/LoginPage';
import UserManagement from './components/UserManagement';
import DashboardHome from './components/DashboardHome';
import AgentExplorer from './components/AgentExplorer';
import AgentDetails from './components/AgentDetails';
import DiscoveryCenter from './components/DiscoveryCenter';
import MatchingCenter from './components/MatchingCenter';
import TrustAnalytics from './components/TrustAnalytics';
import TelemetryCenter from './components/TelemetryCenter';
import IdentityCredentials from './components/IdentityCredentials';
import AuthorizationVisualizer from './components/AuthorizationVisualizer';
import AuditTrail from './components/AuditTrail';
import StateTransitionMap from './components/StateTransitionMap';
import SystemHealth from './components/SystemHealth';
import CollaborationCenter from './components/CollaborationCenter';
import WorkflowCenter from './components/WorkflowCenter';
import DemoVisualizer from './components/DemoVisualizer';

function Sidebar() {
  const location = useLocation();
  const { user, logout, isAdmin } = useAuth();
  const { toggleTheme, isDark } = useTheme();
  
  const navGroups = [
    {
      label: 'OVERVIEW',
      items: [
        { path: '/', icon: <Shield size={15} />, label: 'Dashboard' }
      ]
    },
    {
      label: 'AGENTS',
      items: [
        { path: '/agents', icon: <Users size={15} />, label: 'Agent Explorer' },
        { path: '/discovery', icon: <Search size={15} />, label: 'Discovery' },
        { path: '/matching', icon: <Sliders size={15} />, label: 'Matching' }
      ]
    },
    {
      label: 'TRUST INTELLIGENCE',
      items: [
        { path: '/analytics', icon: <Activity size={15} />, label: 'Trust Analytics' },
        { path: '/telemetry', icon: <Database size={15} />, label: 'Telemetry' },
        { path: '/transitions', icon: <GitMerge size={15} />, label: 'State Transitions' },
        { path: '/authorization', icon: <Lock size={15} />, label: 'Authorization' }
      ]
    },
    {
      label: 'COLLABORATION',
      items: [
        { path: '/collaboration', icon: <Layers size={15} />, label: 'Collaboration' },
        { path: '/workflows', icon: <GitBranch size={15} />, label: 'Workflows' }
      ]
    },
    {
      label: 'IDENTITY',
      items: [
        { path: '/identity', icon: <FileKey2 size={15} />, label: 'DIDs & Credentials' }
      ]
    },
    {
      label: 'SECURITY',
      items: [
        { path: '/audit', icon: <GitMerge size={15} />, label: 'Audit Trail' },
        { path: '/health', icon: <Server size={15} />, label: 'System Health' }
      ]
    },
    {
      label: 'ADMINISTRATION',
      items: [
        ...(isAdmin ? [{ path: '/admin/users', icon: <UserCheck size={15} />, label: 'User Management' }] : [])
      ]
    },
    {
      label: 'DEMONSTRATION',
      items: [
        { path: '/demo', icon: <PlayCircle size={15} />, label: 'Live Demo' }
      ]
    }
  ].filter(group => group.items.length > 0);

  return (
    <div className="w-64 bg-white dark:bg-[#080b13] border-r border-slate-200 dark:border-slate-800 min-h-screen flex flex-col relative z-20 font-sans shadow-sm dark:shadow-2xl transition-colors">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-200 dark:border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-tc-cyan/10 border border-tc-cyan/30 rounded-lg">
            <Shield className="text-tc-cyan" size={22} />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-widest text-slate-900 dark:text-slate-100 uppercase font-mono">TRUSTCHAIN-AI</h1>
            <p className="text-[9px] text-slate-500 dark:text-slate-400 font-mono tracking-tighter uppercase font-medium">Security Operations Center</p>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-5 overflow-y-auto custom-scrollbar px-3 py-4">
        {navGroups.map((group, idx) => (
          <div key={idx}>
            <div className="text-[9px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1.5 px-3 font-semibold">
              {group.label}
            </div>
            <div className="space-y-0.5">
              {group.items.map(item => {
                const isActive = location.pathname === item.path || (item.path === '/agents' && location.pathname.startsWith('/agents/'));
                return (
                  <Link 
                    key={item.path} 
                    to={item.path} 
                    className={`flex items-center gap-3 px-3 py-2 rounded-md font-mono text-xs transition-all ${
                      isActive 
                        ? 'bg-sky-50 dark:bg-[#121929] border border-sky-200 dark:border-slate-800 text-cyan-700 dark:text-tc-cyan font-bold shadow-[inset_3px_0_0_#0284c7] dark:shadow-[inset_3px_0_0_#00f0ff]' 
                        : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#121929]/60 border border-transparent'
                    }`}>
                    {React.cloneElement(item.icon, { className: isActive ? 'text-cyan-700 dark:text-tc-cyan' : 'text-slate-400 dark:text-slate-500' })}
                    <span className="tracking-wide">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Bottom Sidebar Status & User Section */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#050811] space-y-3 font-mono text-[10px]">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 dark:bg-emerald-400 animate-pulse"></span>
            <span>● Backend Connected</span>
          </div>
          <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 dark:bg-emerald-400"></span>
            <span>● Database Connected</span>
          </div>
        </div>

        {user && (
          <div className="pt-2 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between gap-2">
            <div className="truncate">
              <div className="text-xs font-bold text-slate-900 dark:text-slate-200 truncate">{user.username}</div>
              <div className="text-[9px] text-tc-cyan uppercase font-bold">{user.role}</div>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={toggleTheme}
                title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                className="p-1.5 text-slate-500 hover:text-amber-500 hover:bg-slate-200/60 dark:text-slate-400 dark:hover:text-amber-400 dark:hover:bg-slate-800/60 rounded border border-transparent transition-all cursor-pointer"
              >
                {isDark ? <Sun size={14} className="text-amber-400" /> : <Moon size={14} className="text-cyan-600" />}
              </button>
              <button
                onClick={logout}
                title="Logout Session"
                className="p-1.5 text-slate-500 hover:text-rose-600 hover:bg-rose-100/60 dark:text-slate-400 dark:hover:text-rose-400 dark:hover:bg-rose-950/40 rounded border border-transparent hover:border-rose-300 dark:hover:border-rose-800/40 transition-all cursor-pointer"
              >
                <LogOut size={14} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function MainLayout() {
  const { user, loading } = useAuth();
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      window.location.reload();
    }, 400);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-[#050811] flex items-center justify-center font-mono text-tc-cyan text-xs">
        <div className="flex items-center gap-3">
          <div className="w-4 h-4 rounded-full border-2 border-tc-cyan border-t-transparent animate-spin"></div>
          <span>Authenticating SOC Operations Portal...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-[#050811] text-slate-900 dark:text-slate-200 font-sans selection:bg-tc-cyan selection:text-black transition-colors">
      <Sidebar />
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <TopBar onRefresh={handleRefresh} isRefreshing={isRefreshing} />
        <main className="flex-1 overflow-auto relative z-10 p-6 md:p-8 custom-scrollbar">
          <Routes>
            <Route path="/" element={<DashboardHome />} />
            <Route path="/agents" element={<AgentExplorer />} />
            <Route path="/agents/:did" element={<AgentDetails />} />
            <Route path="/discovery" element={<DiscoveryCenter />} />
            <Route path="/matching" element={<MatchingCenter />} />
            <Route path="/analytics" element={<TrustAnalytics />} />
            <Route path="/telemetry" element={<TelemetryCenter />} />
            <Route path="/transitions" element={<StateTransitionMap />} />
            <Route path="/authorization" element={<AuthorizationVisualizer />} />
            <Route path="/collaboration" element={<CollaborationCenter />} />
            <Route path="/workflows" element={<WorkflowCenter />} />
            <Route path="/identity" element={<IdentityCredentials />} />
            <Route path="/audit" element={<AuditTrail />} />
            <Route path="/health" element={<SystemHealth />} />
            <Route path="/admin/users" element={<UserManagement />} />
            <Route path="/demo" element={<DemoVisualizer />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <MainLayout />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}
