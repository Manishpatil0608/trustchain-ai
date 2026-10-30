import React, { useState } from 'react';
import { Shield, Lock, User, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setErrorMessage('Please provide both username and password.');
      return;
    }

    setSubmitting(true);
    setErrorMessage('');

    try {
      await login(username, password);
    } catch (err) {
      setErrorMessage(err.message || 'Authentication failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#05070a] flex items-center justify-center p-4 relative overflow-hidden font-sans transition-colors">
      {/* Glow Backdrops */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-tc-cyan/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-10 right-10 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full max-w-md bg-white dark:bg-[#090d16] border border-slate-200 dark:border-[#1e293b] rounded-xl p-8 shadow-xl dark:shadow-2xl relative z-10 backdrop-blur-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 dark:bg-[#121929] border border-tc-cyan/30 mb-4 relative">
            <Shield className="text-tc-cyan relative z-10" size={32} />
            <div className="absolute inset-0 bg-tc-cyan blur-md opacity-20"></div>
          </div>
          <h1 className="text-2xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">TrustChain-AI</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-mono tracking-widest uppercase mt-1">Platform Authentication Gateway</p>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="mb-6 p-3.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-500/50 rounded-lg flex items-start gap-3 text-red-800 dark:text-red-300 text-xs">
            <AlertCircle size={16} className="text-red-500 shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-2 font-semibold">
              Username or Email
            </label>
            <div className="relative">
              <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 pl-10 pr-4 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan transition-colors"
                autoComplete="username"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-2 font-semibold">
              Password
            </label>
            <div className="relative">
              <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 pl-10 pr-4 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan transition-colors"
                autoComplete="current-password"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-tc-cyan hover:bg-cyan-600 dark:hover:bg-cyan-300 text-white dark:text-black font-semibold font-mono text-xs uppercase tracking-widest py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-[0_0_15px_rgba(0,240,255,0.2)] disabled:opacity-50 mt-4 cursor-pointer"
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full border-2 border-white dark:border-black border-t-transparent animate-spin"></div>
                Authenticating...
              </span>
            ) : (
              <>
                <span>Authenticate Platform Session</span>
                <ArrowRight size={14} />
              </>
            )}
          </button>
        </form>

        {/* Development Quick Helper Note */}
        <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800/80 text-center">
          <div className="flex items-center justify-center gap-2 text-[10px] font-mono text-slate-500 uppercase tracking-wider">
            <CheckCircle2 size={12} className="text-tc-cyan" />
            <span>Dev Admin: admin / Admin@TrustChain2026!</span>
          </div>
        </div>
      </div>
    </div>
  );
}
