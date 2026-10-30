import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Users, Play, CheckCircle2, AlertTriangle, ShieldAlert, Plus, 
  Search, RefreshCw, Send, Star, Layers, Activity, Lock, Cpu
} from 'lucide-react';

const API_BASE = 'http://localhost:8050/api/v1';

export default function CollaborationCenter() {
  const [agents, setAgents] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // Form states
  const [showAddAgent, setShowAddAgent] = useState(false);
  const [newAgent, setNewAgent] = useState({
    agent_name: '',
    agent_type: 'research',
    model_name: 'gpt-4o',
    model_provider: 'OpenAI',
    endpoint: '',
    description: '',
    capabilities: 'research,analysis'
  });

  const [reqForm, setReqForm] = useState({
    requester_did: '',
    target_did: '',
    task_description: 'Analyze security vectors in autonomous session delegation',
    required_capability: 'analysis'
  });

  const [selectedSessionId, setSelectedSessionId] = useState(null);
  const [sessionDetails, setSessionDetails] = useState(null);
  const [stepInput, setStepInput] = useState('');
  const [rating, setRating] = useState(5);
  const [ratingFeedback, setRatingFeedback] = useState('');
  const [statusMessage, setStatusMessage] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [agRes, sessRes, stRes] = await Promise.all([
        axios.get(`${API_BASE}/registry/agents`),
        axios.get(`${API_BASE}/collaboration/sessions`),
        axios.get(`${API_BASE}/registry/stats`)
      ]);
      setAgents(agRes.data);
      setSessions(sessRes.data);
      setStats(stRes.data);

      if (agRes.data.length > 0 && !reqForm.requester_did) {
        setReqForm(prev => ({ ...prev, requester_did: agRes.data[0].did }));
      }
    } catch (err) {
      console.error('Failed to load collaboration data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleRegisterAgent = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_BASE}/registry/agents`, newAgent);
      setStatusMessage({ type: 'success', text: `Agent '${res.data.agent_name}' registered successfully with DID: ${res.data.did}` });
      setShowAddAgent(false);
      setNewAgent({
        agent_name: '',
        agent_type: 'research',
        model_name: 'gpt-4o',
        model_provider: 'OpenAI',
        endpoint: '',
        description: '',
        capabilities: 'research,analysis'
      });
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to register agent' });
    }
  };

  const handleCreateCollaboration = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        requester_did: reqForm.requester_did,
        target_did: reqForm.target_did || null,
        task_description: reqForm.task_description,
        required_capability: reqForm.required_capability
      };
      const res = await axios.post(`${API_BASE}/collaboration/request`, payload);
      setStatusMessage({ type: 'success', text: `Collaboration Session Created! ID: ${res.data.session_id}` });
      setSelectedSessionId(res.data.session_id);
      fetchSessionDetails(res.data.session_id);
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Collaboration Request Denied' });
    }
  };

  const fetchSessionDetails = async (sessionId) => {
    try {
      const res = await axios.get(`${API_BASE}/collaboration/sessions/${sessionId}`);
      setSessionDetails(res.data);
      setSelectedSessionId(sessionId);
    } catch (err) {
      console.error('Error fetching session details', err);
    }
  };

  const handleExecuteStep = async () => {
    if (!selectedSessionId || !sessionDetails) return;
    try {
      const res = await axios.post(`${API_BASE}/collaboration/sessions/${selectedSessionId}/step`, {
        sender_did: sessionDetails.session.requester_did,
        content: stepInput || sessionDetails.session.task_description
      });
      setStatusMessage({ type: 'success', text: `Step Executed! Telemetry ingested. New Trust: ${res.data.telemetry.trust_score}` });
      setStepInput('');
      fetchSessionDetails(selectedSessionId);
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Execution Failed' });
    }
  };

  const handleTerminateSession = async () => {
    if (!selectedSessionId) return;
    try {
      const res = await axios.post(`${API_BASE}/collaboration/sessions/${selectedSessionId}/terminate`);
      setStatusMessage({ type: 'success', text: `Session ${selectedSessionId} terminated. Agents reset to AVAILABLE.` });
      fetchSessionDetails(selectedSessionId);
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Termination Failed' });
    }
  };

  const handleRateAgent = async () => {
    if (!sessionDetails) return;
    try {
      const res = await axios.post(`${API_BASE}/collaboration/rate`, {
        rater_did: sessionDetails.session.requester_did,
        target_did: sessionDetails.session.target_did,
        rating: parseFloat(rating),
        feedback: ratingFeedback
      });
      setStatusMessage({ type: 'success', text: `Rating submitted! New Reputation: ${res.data.new_reputation_score}/5.0` });
      setRatingFeedback('');
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Rating Failed' });
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-tc-border/50 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-tc-cyan uppercase tracking-widest mb-1">
            <Layers size={14} /> Multi-Agent Ecosystem & Trust Governance
          </div>
          <h1 className="text-2xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">Agent Collaboration Hub</h1>
          <p className="text-slate-600 dark:text-slate-400 text-sm mt-1">
            Registry, capability discovery, real-time collaboration sessions, telemetry & adaptive governance.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setShowAddAgent(true)}
            className="flex items-center gap-2 bg-tc-cyan text-white dark:text-black px-4 py-2.5 rounded font-semibold text-xs uppercase tracking-wider hover:bg-cyan-600 dark:hover:bg-cyan-300 transition-all duration-300 shadow-[0_0_15px_rgba(0,240,255,0.2)]">
            <Plus size={16} /> Register AI Agent
          </button>
          <button 
            onClick={fetchData}
            className="p-2.5 bg-slate-100 dark:bg-[#121929] border border-slate-200 dark:border-tc-border text-slate-700 dark:text-slate-300 rounded hover:border-tc-cyan transition-colors">
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* Status Alert Banner */}
      {statusMessage && (
        <div className={`p-4 rounded border flex items-center justify-between ${statusMessage.type === 'error' ? 'bg-red-50 dark:bg-red-950/40 border-red-200 dark:border-red-800/80 text-red-800 dark:text-red-300' : 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800/80 text-emerald-800 dark:text-emerald-300'}`}>
          <div className="flex items-center gap-3">
            {statusMessage.type === 'error' ? <ShieldAlert size={20} /> : <CheckCircle2 size={20} />}
            <span className="text-xs font-mono">{statusMessage.text}</span>
          </div>
          <button onClick={() => setStatusMessage(null)} className="text-xs opacity-70 hover:opacity-100">✕</button>
        </div>
      )}

      {/* Overview Metrics Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-tc-border/60 p-5 rounded-lg shadow-sm">
            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">Registered Agents</div>
            <div className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-100">{stats.agents.total}</div>
            <div className="flex items-center gap-2 mt-2 text-[10px] font-mono text-slate-500 dark:text-slate-400">
              <span className="text-tc-success font-semibold">{stats.agents.available} Available</span> • <span>{stats.agents.busy} Busy</span>
            </div>
          </div>
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-tc-border/60 p-5 rounded-lg shadow-sm">
            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">Security Status</div>
            <div className="text-2xl font-bold font-mono text-tc-success">{stats.trust_states.trusted} TRUSTED</div>
            <div className="flex items-center gap-2 mt-2 text-[10px] font-mono">
              <span className="text-amber-600 dark:text-amber-400 font-semibold">{stats.trust_states.suspicious} Suspicious</span> • 
              <span className="text-rose-600 dark:text-rose-500 font-bold">{stats.trust_states.quarantined} Quarantined</span>
            </div>
          </div>
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-tc-border/60 p-5 rounded-lg shadow-sm">
            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">Active Collaborations</div>
            <div className="text-2xl font-bold font-mono text-tc-cyan">{stats.collaborations.active}</div>
            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 mt-2">{stats.collaborations.completed} Completed Sessions</div>
          </div>
          <div className="bg-white dark:bg-[#0b101d] border border-slate-200 dark:border-tc-border/60 p-5 rounded-lg shadow-sm">
            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">Telemetry Events</div>
            <div className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-100">{stats.total_telemetry_events}</div>
            <div className="text-[10px] font-mono text-tc-cyan mt-2 font-semibold">Real-time Trust Engine Feeding</div>
          </div>
        </div>
      )}

      {/* Main Grid: Request Wizard + Agent Registry */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Request Collaboration Wizard (Left Column) */}
        <div className="bg-white dark:bg-[#080b12] border border-slate-200 dark:border-tc-border/60 rounded-xl p-6 space-y-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-tc-border/40 pb-4">
            <div className="flex items-center gap-2 text-sm font-bold uppercase text-slate-900 dark:text-slate-100">
              <Play size={16} className="text-tc-cyan" /> Request Collaboration
            </div>
            <span className="text-[10px] font-mono bg-tc-cyan/10 text-tc-cyan px-2 py-0.5 rounded border border-tc-cyan/30 font-semibold">
              POLICY CHECKED
            </span>
          </div>

          <form onSubmit={handleCreateCollaboration} className="space-y-4">
            <div>
              <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Requester Agent</label>
              <select 
                value={reqForm.requester_did}
                onChange={(e) => setReqForm(prev => ({ ...prev, requester_did: e.target.value }))}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2.5 text-xs text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none font-mono">
                {agents.map(a => (
                  <option key={a.did} value={a.did}>
                    {a.agent_name} ({a.operational_status}) - Trust: {a.trust_score?.toFixed(3)} [{a.trust_state}]
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Required Capability</label>
              <select 
                value={reqForm.required_capability}
                onChange={(e) => setReqForm(prev => ({ ...prev, required_capability: e.target.value }))}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2.5 text-xs text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none font-mono">
                <option value="analysis">Analysis & Reasoning</option>
                <option value="research">Research & Information Retrieval</option>
                <option value="coding">Coding & Implementation</option>
                <option value="planning">Execution Planning</option>
                <option value="verification">Verification & Security</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Target Agent (Optional / Discovery)</label>
              <select 
                value={reqForm.target_did}
                onChange={(e) => setReqForm(prev => ({ ...prev, target_did: e.target.value }))}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2.5 text-xs text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none font-mono">
                <option value="">-- Auto-Discover Available Candidate --</option>
                {agents.map(a => (
                  <option key={a.did} value={a.did}>
                    {a.agent_name} [{a.capabilities}] - {a.operational_status} ({a.trust_state})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Task Description</label>
              <textarea 
                value={reqForm.task_description}
                onChange={(e) => setReqForm(prev => ({ ...prev, task_description: e.target.value }))}
                rows={3}
                className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2.5 text-xs text-slate-900 dark:text-slate-200 focus:border-tc-cyan outline-none font-sans"
              />
            </div>

            <button 
              type="submit"
              className="w-full bg-tc-cyan text-white dark:text-black py-3 rounded font-bold text-xs uppercase tracking-wider hover:bg-cyan-600 dark:hover:bg-cyan-300 transition-all shadow-[0_0_15px_rgba(0,240,255,0.2)]">
              Initiate Collaboration Request
            </button>
          </form>
        </div>

        {/* Registered Agents List (Right 2 Columns) */}
        <div className="lg:col-span-2 bg-white dark:bg-[#080b12] border border-slate-200 dark:border-tc-border/60 rounded-xl p-6 space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-tc-border/40 pb-4">
            <div className="flex items-center gap-2 text-sm font-bold uppercase text-slate-900 dark:text-slate-100">
              <Users size={16} className="text-tc-cyan" /> Registered AI Agents & Operational Status
            </div>
            <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Total: {agents.length}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[460px] overflow-y-auto custom-scrollbar pr-1">
            {agents.map(agent => (
              <div 
                key={agent.did}
                className={`p-4 rounded-lg border transition-all ${
                  agent.trust_state === 'QUARANTINED' || agent.trust_state === 'REVOKED' 
                    ? 'bg-rose-50 border-rose-200 text-rose-800 dark:bg-red-950/20 dark:border-red-900/60 dark:text-rose-300' 
                    : 'bg-slate-50 dark:bg-[#0f1623] border-slate-200 dark:border-tc-border/60 hover:border-tc-cyan/40 dark:hover:border-tc-cyan/40'
                }`}>
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">{agent.agent_name}</h3>
                    <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 mt-0.5">{agent.model_provider} • {agent.model_name}</div>
                  </div>
                  <span className={`text-[9px] font-mono px-2 py-0.5 rounded uppercase font-bold tracking-wider ${
                    agent.operational_status === 'AVAILABLE' 
                      ? 'bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-400 dark:border-emerald-800' 
                      : agent.operational_status === 'BUSY' 
                        ? 'bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950 dark:text-amber-400 dark:border-amber-800' 
                        : 'bg-slate-100 text-slate-700 border border-slate-200 dark:bg-slate-800 dark:text-slate-400'
                  }`}>
                    {agent.operational_status}
                  </span>
                </div>

                <div className="mt-3 text-[10px] font-mono text-slate-500 dark:text-slate-400 truncate">
                  <span className="text-slate-400 dark:text-slate-500">DID:</span> {agent.did}
                </div>

                <div className="mt-3 flex items-center justify-between text-[11px] font-mono border-t border-slate-200 dark:border-tc-border/40 pt-3">
                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-500 dark:text-slate-400">Trust:</span>
                    <span className={`font-bold ${agent.trust_state === 'TRUSTED' ? 'text-tc-success' : agent.trust_state === 'SUSPICIOUS' ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-500'}`}>
                      {agent.trust_score?.toFixed(3)} [{agent.trust_state}]
                    </span>
                  </div>
                  <div className="flex items-center gap-1 text-amber-500 dark:text-amber-400 font-bold">
                    <Star size={12} fill="currentColor" />
                    <span>{agent.reputation_score}/5.0</span>
                  </div>
                </div>

                <div className="mt-2 text-[9px] font-mono text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-[#080b12] p-1.5 rounded truncate border border-slate-200/50 dark:border-transparent">
                  Capabilities: {agent.capabilities}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Active & Completed Collaboration Sessions */}
      <div className="bg-white dark:bg-[#080b12] border border-slate-200 dark:border-tc-border/60 rounded-xl p-6 space-y-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-200 dark:border-tc-border/40 pb-4">
          <div className="flex items-center gap-2 text-sm font-bold uppercase text-slate-900 dark:text-slate-100">
            <Activity size={16} className="text-tc-cyan" /> Collaboration Sessions & Interactive Work Execution
          </div>
          <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Active & Completed Sessions</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sessions List */}
          <div className="space-y-3">
            <div className="text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-wider">Select Session</div>
            {sessions.length === 0 ? (
              <div className="text-xs font-mono text-slate-500 p-4 border border-dashed border-slate-200 dark:border-tc-border/40 rounded text-center">
                No active or historical collaboration sessions found. Initiate a request above.
              </div>
            ) : (
              sessions.map(s => (
                <div 
                  key={s.session_id}
                  onClick={() => fetchSessionDetails(s.session_id)}
                  className={`p-3.5 rounded border cursor-pointer transition-all ${
                    selectedSessionId === s.session_id 
                      ? 'bg-sky-50 dark:bg-[#121929] border-sky-500 dark:border-tc-cyan text-slate-900 dark:text-slate-100 shadow-sm' 
                      : 'bg-slate-50 dark:bg-[#0b101d] border-slate-200 dark:border-tc-border/50 text-slate-600 dark:text-slate-400 hover:border-slate-400 dark:hover:border-slate-500'
                  }`}>
                  <div className="flex items-center justify-between text-xs font-mono font-bold">
                    <span className="text-tc-cyan">{s.session_id}</span>
                    <span className={`text-[9px] px-2 py-0.5 rounded uppercase font-semibold ${
                      s.status === 'COMPLETED' 
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-300 dark:bg-emerald-950 dark:text-emerald-400 dark:border-transparent' 
                        : s.status === 'ACTIVE' 
                          ? 'bg-cyan-50 text-cyan-700 border border-cyan-300 dark:bg-cyan-950 dark:text-cyan-400 dark:border-transparent animate-pulse' 
                          : 'bg-amber-50 text-amber-700 border border-amber-300 dark:bg-amber-950 dark:text-amber-400 dark:border-transparent'
                    }`}>
                      {s.status}
                    </span>
                  </div>
                  <div className="text-[11px] font-sans mt-2 line-clamp-1 text-slate-800 dark:text-slate-200">{s.task_description}</div>
                  <div className="text-[9px] font-mono text-slate-500 dark:text-slate-400 mt-2 flex justify-between">
                    <span>Cap: {s.required_capability}</span>
                    <span>Prod: {s.productivity_score}</span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Session Interactive Timeline & Details */}
          <div className="lg:col-span-2 bg-slate-50 dark:bg-[#0b101d] border border-slate-200 dark:border-tc-border/60 rounded-lg p-5 space-y-5">
            {sessionDetails ? (
              <>
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 border-b border-slate-200 dark:border-tc-border/40 pb-4">
                  <div>
                    <h3 className="text-sm font-bold font-mono text-tc-cyan">{sessionDetails.session.session_id}</h3>
                    <div className="text-[11px] text-slate-700 dark:text-slate-300 font-sans mt-1">{sessionDetails.session.task_description}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    {sessionDetails.session.status !== 'COMPLETED' && sessionDetails.session.status !== 'TERMINATED' && (
                      <button 
                        onClick={handleTerminateSession}
                        className="bg-rose-100 hover:bg-rose-200 text-rose-800 border border-rose-300 dark:bg-red-950/80 dark:text-red-300 dark:border-red-800 px-3 py-1.5 rounded text-[10px] font-mono uppercase font-bold dark:hover:bg-red-900 transition-colors">
                        Complete & Terminate
                      </button>
                    )}
                  </div>
                </div>

                {/* Event Logs Timeline */}
                <div className="space-y-3 max-h-60 overflow-y-auto custom-scrollbar pr-2">
                  <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest">Session Message History</div>
                  {sessionDetails.events.map((evt, idx) => (
                    <div key={idx} className="p-3 bg-white dark:bg-[#080b12] border border-slate-200 dark:border-tc-border/40 rounded space-y-1 shadow-xs">
                      <div className="flex justify-between items-center text-[10px] font-mono">
                        <span className="text-tc-cyan font-bold">{evt.sender_did === sessionDetails.session.requester_did ? 'REQUESTER' : evt.sender_did === 'SYSTEM' ? 'SYSTEM' : 'TARGET AGENT'}</span>
                        <span className="text-slate-500 dark:text-slate-400">{new Date(evt.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <div className="text-xs font-mono text-slate-800 dark:text-slate-200 whitespace-pre-wrap">{evt.content}</div>
                    </div>
                  ))}
                </div>

                {/* Step Execution & Rating Control */}
                {sessionDetails.session.status !== 'COMPLETED' && sessionDetails.session.status !== 'TERMINATED' ? (
                  <div className="border-t border-slate-200 dark:border-tc-border/40 pt-4 space-y-3">
                    <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase">Execute Session Step</div>
                    <div className="flex gap-2">
                      <input 
                        type="text"
                        value={stepInput}
                        onChange={(e) => setStepInput(e.target.value)}
                        placeholder="Enter step task instructions..."
                        className="flex-1 bg-white dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2.5 text-xs text-slate-900 dark:text-slate-200 outline-none focus:border-tc-cyan font-mono"
                      />
                      <button 
                        onClick={handleExecuteStep}
                        className="bg-tc-cyan text-white dark:text-black px-4 py-2 rounded text-xs font-bold uppercase tracking-wider hover:bg-cyan-600 dark:hover:bg-cyan-300 flex items-center gap-2 transition-colors">
                        <Send size={14} /> Execute
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="border-t border-slate-200 dark:border-tc-border/40 pt-4 space-y-3">
                    <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase">Submit Agent Rating</div>
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-1">
                        <span className="text-xs font-mono text-slate-700 dark:text-slate-300 mr-2">Rating:</span>
                        {[1, 2, 3, 4, 5].map(val => (
                          <Star 
                            key={val}
                            size={18}
                            onClick={() => setRating(val)}
                            className={`cursor-pointer ${val <= rating ? 'text-amber-500 fill-amber-500' : 'text-slate-300 dark:text-slate-600'}`}
                          />
                        ))}
                      </div>
                      <input 
                        type="text"
                        value={ratingFeedback}
                        onChange={(e) => setRatingFeedback(e.target.value)}
                        placeholder="Feedback notes..."
                        className="flex-1 bg-white dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none"
                      />
                      <button 
                        onClick={handleRateAgent}
                        className="bg-amber-500 text-white dark:text-black px-3 py-2 rounded text-xs font-bold uppercase hover:bg-amber-600 dark:hover:bg-amber-400 transition-colors">
                        Submit Rating
                      </button>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-16 text-slate-500 dark:text-slate-400 text-xs font-mono">
                Select a session on the left to view interactive messages, execute work steps, or submit ratings.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Add Agent Modal */}
      {showAddAgent && (
        <div className="fixed inset-0 z-50 bg-black/60 dark:bg-black/80 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#080b12] border border-slate-200 dark:border-tc-border rounded-xl max-w-lg w-full p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-tc-border/40 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 uppercase">Register New AI Agent</h3>
              <button onClick={() => setShowAddAgent(false)} className="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200">✕</button>
            </div>

            <form onSubmit={handleRegisterAgent} className="space-y-4">
              <div>
                <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Agent Name</label>
                <input 
                  type="text" required
                  value={newAgent.agent_name}
                  onChange={(e) => setNewAgent(prev => ({ ...prev, agent_name: e.target.value }))}
                  placeholder="e.g. Security Audit Agent"
                  className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Agent Type</label>
                  <select 
                    value={newAgent.agent_type}
                    onChange={(e) => setNewAgent(prev => ({ ...prev, agent_type: e.target.value }))}
                    className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none">
                    <option value="research">Research</option>
                    <option value="analysis">Analysis</option>
                    <option value="coding">Coding</option>
                    <option value="planning">Planning</option>
                    <option value="execution">Execution</option>
                    <option value="verification">Verification</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Model Provider</label>
                  <select 
                    value={newAgent.model_provider}
                    onChange={(e) => setNewAgent(prev => ({ ...prev, model_provider: e.target.value }))}
                    className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none">
                    <option value="OpenAI">OpenAI</option>
                    <option value="Anthropic">Anthropic</option>
                    <option value="Ollama">Ollama</option>
                    <option value="Local">Local Engine</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Capabilities (Comma-separated)</label>
                <input 
                  type="text" required
                  value={newAgent.capabilities}
                  onChange={(e) => setNewAgent(prev => ({ ...prev, capabilities: e.target.value }))}
                  placeholder="e.g. research,analysis,coding"
                  className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Endpoint (Optional)</label>
                <input 
                  type="text"
                  value={newAgent.endpoint}
                  onChange={(e) => setNewAgent(prev => ({ ...prev, endpoint: e.target.value }))}
                  placeholder="e.g. http://localhost:8050/api/v1/agent/task"
                  className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-tc-border rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none font-mono"
                />
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <button 
                  type="button" 
                  onClick={() => setShowAddAgent(false)}
                  className="px-4 py-2 border border-slate-300 dark:border-tc-border text-slate-600 dark:text-slate-400 rounded text-xs hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="px-4 py-2 bg-tc-cyan text-white dark:text-black font-bold rounded text-xs uppercase hover:bg-cyan-600 dark:hover:bg-cyan-300 transition-colors">
                  Generate DID & Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
