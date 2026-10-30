import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Shield, Copy, Check, Filter, ArrowUpDown, ExternalLink, RefreshCw, Cpu, Layers } from 'lucide-react';
import { registryApi, trustApi } from '../api';
import { LoadingState, ErrorState, EmptyState, TrustBadge, HealthBadge, StatusBadge } from './ui/States';
import AgentInvestigationDrawer from './AgentInvestigationDrawer';

export default function AgentExplorer() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [filterState, setFilterState] = useState('ALL');
  const [filterCapability, setFilterCapability] = useState('ALL');
  const [sortOrder, setSortOrder] = useState('desc'); // default highest trust first
  const [copied, setCopied] = useState(null);
  const [selectedAgentDid, setSelectedAgentDid] = useState(null);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      setError(null);
      // Attempt to load full agent registry records
      let data = [];
      try {
        const regRes = await registryApi.getAgents();
        if (Array.isArray(regRes) && regRes.length > 0) {
          data = regRes;
        }
      } catch (e) {
        console.warn('Registry agents fetch fallback to trust agents:', e);
      }

      // If registry returned empty or failed, fallback to trustApi.getAgents
      if (data.length === 0) {
        const trustRes = await trustApi.getAgents();
        data = (trustRes || []).map(t => ({
          agent_id: `agent_${t.agent_did?.slice(-8)}`,
          agent_name: `Agent ${t.agent_did?.slice(0, 16)}...`,
          did: t.agent_did,
          agent_did: t.agent_did,
          capabilities: 'general',
          trust_score: t.trust_score,
          trust_state: t.trust_state,
          health_status: 'HEALTHY',
          operational_status: 'AVAILABLE',
          reputation_score: 5.0,
        }));
      }

      setAgents(data);
    } catch (err) {
      setError(err.message || 'Failed to load agent roster.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleCopy = (did) => {
    if (!did) return;
    navigator.clipboard.writeText(did);
    setCopied(did);
    setTimeout(() => setCopied(null), 2000);
  };

  if (loading) return <LoadingState message="SCANNING IDENTITY REGISTRY & TRUST STATES..." />;
  if (error) return <ErrorState error={error} retry={fetchAgents} />;

  // Extract all distinct capabilities for filter dropdown
  const allCapabilities = Array.from(new Set(
    agents.flatMap(a => (a.capabilities || '').split(',').map(c => c.trim().toLowerCase())).filter(Boolean)
  ));

  let processed = [...agents];

  // Search by DID, name, or capabilities
  if (search.trim()) {
    const q = search.toLowerCase().trim();
    processed = processed.filter(a => 
      (a.did || a.agent_did || '').toLowerCase().includes(q) ||
      (a.agent_name || '').toLowerCase().includes(q) ||
      (a.capabilities || '').toLowerCase().includes(q) ||
      (a.model_name || '').toLowerCase().includes(q)
    );
  }

  // Filter by Trust State
  if (filterState !== 'ALL') {
    processed = processed.filter(a => a.trust_state === filterState);
  }

  // Filter by Capability
  if (filterCapability !== 'ALL') {
    processed = processed.filter(a => 
      (a.capabilities || '').toLowerCase().includes(filterCapability.toLowerCase())
    );
  }

  // Sort by Trust Score
  processed.sort((a, b) => {
    const scoreA = a.trust_score ?? 0;
    const scoreB = b.trust_score ?? 0;
    return sortOrder === 'asc' ? scoreA - scoreB : scoreB - scoreA;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-in fade-in duration-300">
      {/* Page Header */}
      <header className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-tc-cyan font-mono text-xs font-semibold uppercase tracking-widest mb-1">
            <Shield size={14} /> Decentralized Identity Registry
          </div>
          <h2 className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-100 uppercase tracking-wide flex items-center gap-3">
            Autonomous Agent Inventory
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-xs font-mono mt-1">
            W3C did:key identities, live behavioral trust postures, and verified capabilities.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-tc-cyan" size={13} />
            <input 
              type="text" 
              placeholder="Search Name, DID, Capability..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="bg-white dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded text-xs text-slate-900 dark:text-slate-200 focus:outline-none focus:border-tc-cyan w-64 py-2 pl-9 pr-3 font-mono transition-colors shadow-xs" 
            />
          </div>

          <select 
            value={filterState} 
            onChange={e => setFilterState(e.target.value)} 
            className="bg-white dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded text-xs text-slate-700 dark:text-slate-200 py-2 px-3 font-mono focus:border-tc-cyan outline-none cursor-pointer shadow-xs"
          >
            <option value="ALL">ALL TRUST STATES</option>
            <option value="TRUSTED">TRUSTED (T &ge; 0.8)</option>
            <option value="SUSPICIOUS">SUSPICIOUS (0.5 &le; T &lt; 0.8)</option>
            <option value="QUARANTINED">QUARANTINED (T &lt; 0.5)</option>
            <option value="REVOKED">REVOKED (ADMIN)</option>
          </select>

          {allCapabilities.length > 0 && (
            <select 
              value={filterCapability} 
              onChange={e => setFilterCapability(e.target.value)} 
              className="bg-white dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded text-xs text-slate-700 dark:text-slate-200 py-2 px-3 font-mono focus:border-tc-cyan outline-none cursor-pointer shadow-xs"
            >
              <option value="ALL">ALL CAPABILITIES</option>
              {allCapabilities.map(c => (
                <option key={c} value={c}>{c.toUpperCase()}</option>
              ))}
            </select>
          )}

          <button
            onClick={fetchAgents}
            className="p-2 bg-white dark:bg-[#121929] border border-slate-300 dark:border-slate-800 rounded text-slate-600 dark:text-slate-300 hover:text-tc-cyan dark:hover:text-tc-cyan transition-colors"
            title="Refresh Roster"
          >
            <RefreshCw size={13} />
          </button>
        </div>
      </header>

      {/* Roster Table Card */}
      <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
        {agents.length === 0 ? (
          <EmptyState message="No agents discovered in the registry." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-slate-50 dark:bg-[#080b13] text-slate-500 dark:text-slate-400 text-[10px] uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="p-3.5 font-bold">Agent Identity</th>
                  <th className="p-3.5 font-bold">Capabilities</th>
                  <th 
                    className="p-3.5 font-bold cursor-pointer hover:text-tc-cyan transition-colors flex items-center gap-1.5" 
                    onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                    title="Toggle Sort by Trust Score"
                  >
                    Trust Score T(t) <ArrowUpDown size={11}/>
                  </th>
                  <th className="p-3.5 font-bold">Risk Posture</th>
                  <th className="p-3.5 font-bold text-center">Trust State</th>
                  <th className="p-3.5 font-bold text-center">Health</th>
                  <th className="p-3.5 font-bold text-right">Investigation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/70">
                {processed.map(a => {
                  const did = a.did || a.agent_did;
                  const trustScore = a.trust_score ?? 1.0;
                  const trustState = a.trust_state || 'TRUSTED';
                  const caps = (a.capabilities || 'general').split(',').map(c => c.trim()).filter(Boolean);

                  return (
                    <tr 
                      key={did} 
                      className="hover:bg-slate-50/80 dark:hover:bg-[#121929]/70 transition-colors group"
                    >
                      {/* Identity Column */}
                      <td className="p-3.5">
                        <div className="flex flex-col gap-0.5">
                          <span className="font-bold text-slate-900 dark:text-slate-100 text-xs">
                            {a.agent_name || `Agent ${did.slice(0, 16)}...`}
                          </span>
                          <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 text-[10px]">
                            <span className="truncate max-w-[150px] md:max-w-[220px]" title={did}>
                              {did}
                            </span>
                            <button 
                              onClick={() => handleCopy(did)} 
                              className="text-slate-400 hover:text-tc-cyan transition-colors" 
                              title="Copy Full DID"
                            >
                              {copied === did ? <Check size={12} className="text-tc-success" /> : <Copy size={12} />}
                            </button>
                          </div>
                        </div>
                      </td>

                      {/* Capabilities Chips */}
                      <td className="p-3.5">
                        <div className="flex flex-wrap gap-1 max-w-[200px]">
                          {caps.slice(0, 3).map((cap, i) => (
                            <span 
                              key={i} 
                              className="px-1.5 py-0.5 rounded text-[9px] bg-slate-100 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 uppercase"
                            >
                              {cap}
                            </span>
                          ))}
                          {caps.length > 3 && (
                            <span className="text-[9px] text-slate-400 font-bold">+{caps.length - 3}</span>
                          )}
                        </div>
                      </td>

                      {/* Trust Score */}
                      <td className="p-3.5">
                        <div className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                          {trustScore.toFixed(4)}
                        </div>
                      </td>

                      {/* Risk Visualizer */}
                      <td className="p-3.5">
                        <div className="w-28 md:w-36 h-2 bg-slate-200 dark:bg-[#050811] border border-slate-300 dark:border-slate-700 rounded-full overflow-hidden">
                          <div 
                            className={`h-full transition-all duration-700 ${
                              trustScore >= 0.8 
                                ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]' 
                                : trustScore >= 0.5 
                                ? 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]' 
                                : 'bg-rose-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]'
                            }`} 
                            style={{ width: `${Math.max(6, Math.min(100, trustScore * 100))}%` }}
                          />
                        </div>
                      </td>

                      {/* Trust State Badge */}
                      <td className="p-3.5 text-center">
                        <TrustBadge state={trustState} />
                      </td>

                      {/* Health Status */}
                      <td className="p-3.5 text-center">
                        <HealthBadge status={a.health_status || 'HEALTHY'} />
                      </td>

                      {/* Actions Column: Primary INVESTIGATE Button */}
                      <td className="p-3.5 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            type="button"
                            onClick={() => setSelectedAgentDid(did)}
                            className="bg-sky-50 hover:bg-sky-100 text-cyan-700 border border-sky-300 dark:bg-cyan-950/40 dark:hover:bg-cyan-900/60 dark:text-tc-cyan dark:border-cyan-800/80 text-[11px] font-mono font-bold tracking-wider px-3 py-1.5 rounded transition-all uppercase shadow-xs cursor-pointer flex items-center gap-1.5"
                            title={`Investigate ${a.agent_name || did}`}
                          >
                            <Shield size={12} />
                            Investigate
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}

                {processed.length === 0 && search && (
                  <tr>
                    <td colSpan={7} className="p-10">
                      <EmptyState message={`No agents found matching search "${search}"`} />
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Slide-over Investigation Drawer */}
      {selectedAgentDid && (
        <AgentInvestigationDrawer
          did={selectedAgentDid}
          onClose={() => setSelectedAgentDid(null)}
          onRefreshList={fetchAgents}
        />
      )}
    </div>
  );
}
