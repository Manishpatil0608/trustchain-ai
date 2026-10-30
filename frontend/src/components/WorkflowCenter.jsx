import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  GitBranch, Play, CheckCircle2, AlertTriangle, ShieldAlert, Plus, 
  RefreshCw, ArrowRight, Layers, Cpu, Clock, Check, XCircle, Lock
} from 'lucide-react';

const API_BASE = 'http://localhost:8050/api/v1';

export default function WorkflowCenter() {
  const [workflows, setWorkflows] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedWfId, setSelectedWfId] = useState(null);
  const [wfDetails, setWfDetails] = useState(null);
  const [statusMessage, setStatusMessage] = useState(null);

  // New Workflow Modal Form
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newWf, setNewWf] = useState({
    workflow_name: 'Cybersecurity Threat Analysis Pipeline',
    task_description: 'Analyze multi-agent delegation vulnerabilities and verify mitigation controls.',
    orchestrator_did: '',
    pattern: 'SEQUENTIAL',
    nodes: [
      { agent_did: '', required_capability: 'research', step_order: 1 },
      { agent_did: '', required_capability: 'analysis', step_order: 2 },
      { agent_did: '', required_capability: 'verification', step_order: 3 }
    ]
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [wfRes, agRes] = await Promise.all([
        axios.get(`${API_BASE}/workflows`),
        axios.get(`${API_BASE}/registry/agents`)
      ]);
      setWorkflows(wfRes.data);
      setAgents(agRes.data);

      if (agRes.data.length >= 3 && !newWf.orchestrator_did) {
        setNewWf(prev => ({
          ...prev,
          orchestrator_did: agRes.data[0].did,
          nodes: [
            { agent_did: agRes.data[0].did, required_capability: 'research', step_order: 1 },
            { agent_did: agRes.data[1]?.did || agRes.data[0].did, required_capability: 'analysis', step_order: 2 },
            { agent_did: agRes.data[2]?.did || agRes.data[0].did, required_capability: 'verification', step_order: 3 }
          ]
        }));
      }
    } catch (err) {
      console.error('Failed to fetch workflow data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleCreateWorkflow = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_BASE}/workflows`, newWf);
      setStatusMessage({ type: 'success', text: `Workflow Created! ID: ${res.data.workflow_id}` });
      setShowCreateModal(false);
      setSelectedWfId(res.data.workflow_id);
      fetchWfDetails(res.data.workflow_id);
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to create workflow' });
    }
  };

  const fetchWfDetails = async (wfId) => {
    try {
      const res = await axios.get(`${API_BASE}/workflows/${wfId}`);
      setWfDetails(res.data);
      setSelectedWfId(wfId);
    } catch (err) {
      console.error('Error fetching workflow details', err);
    }
  };

  const handleExecuteWorkflow = async (wfId) => {
    try {
      setStatusMessage({ type: 'info', text: 'Executing multi-agent workflow pipeline...' });
      const res = await axios.post(`${API_BASE}/workflows/${wfId}/execute`);
      setStatusMessage({ type: 'success', text: `Workflow executed successfully! Completed ${res.data.steps_executed} steps.` });
      fetchWfDetails(wfId);
      fetchData();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Workflow Execution Intercepted / Failed' });
      fetchWfDetails(wfId);
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-tc-cyan uppercase tracking-widest mb-1">
            <GitBranch size={14} /> Multi-Agent Workflow Orchestrator
          </div>
          <h1 className="text-2xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">
            Workflow Orchestration Center
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Sequential & Parallel multi-agent pipeline execution with per-DID attribution, telemetry & security checks.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            type="button"
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 bg-tc-cyan text-white dark:text-black px-4 py-2.5 rounded font-semibold text-xs uppercase tracking-wider hover:opacity-90 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500">
            <Plus size={16} /> Create Workflow
          </button>
          <button 
            type="button"
            onClick={fetchData}
            title="Refresh Workflows"
            className="p-2.5 bg-white dark:bg-[#121929] border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 rounded hover:border-tc-cyan transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500">
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* Alert Banner */}
      {statusMessage && (
        <div className={`p-4 rounded border flex items-center justify-between ${
          statusMessage.type === 'error' 
            ? 'bg-red-50 dark:bg-red-950/40 border-red-200 dark:border-red-800/80 text-red-700 dark:text-red-300' 
            : statusMessage.type === 'info' 
            ? 'bg-sky-50 dark:bg-cyan-950/40 border-sky-200 dark:border-cyan-800/80 text-sky-700 dark:text-cyan-300' 
            : 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800/80 text-emerald-700 dark:text-emerald-300'
        }`}>
          <div className="flex items-center gap-3">
            {statusMessage.type === 'error' ? <ShieldAlert size={20} /> : <CheckCircle2 size={20} />}
            <span className="text-xs font-mono font-medium">{statusMessage.text}</span>
          </div>
          <button onClick={() => setStatusMessage(null)} className="text-xs opacity-70 hover:opacity-100">✕</button>
        </div>
      )}

      {/* Workflow Layout: Left List + Right Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Workflows List */}
        <div className="bg-white dark:bg-[#080b12] border border-slate-200 dark:border-slate-800 rounded-xl p-6 space-y-4 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4">
            <div className="flex items-center gap-2 text-sm font-bold uppercase text-slate-900 dark:text-slate-100">
              <Layers size={16} className="text-tc-cyan" /> Registered Workflows
            </div>
            <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Total: {workflows.length}</span>
          </div>

          <div className="space-y-3 max-h-[500px] overflow-y-auto custom-scrollbar pr-1">
            {workflows.length === 0 ? (
              <div className="text-xs font-mono text-slate-500 p-6 border border-dashed border-slate-300 dark:border-slate-800 rounded text-center">
                No workflows created yet. Click "Create Workflow" above to define a multi-agent pipeline.
              </div>
            ) : (
              workflows.map(w => (
                <div 
                  key={w.workflow_id}
                  onClick={() => fetchWfDetails(w.workflow_id)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedWfId === w.workflow_id 
                      ? 'bg-sky-50 dark:bg-[#121929] border-sky-500 dark:border-tc-cyan text-slate-900 dark:text-slate-100 shadow-sm' 
                      : 'bg-white dark:bg-[#0b101d] border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-600'
                  }`}>
                  <div className="flex items-center justify-between text-xs font-mono font-bold">
                    <span className="text-tc-cyan">{w.workflow_id}</span>
                    <span className={`text-[9px] px-2 py-0.5 rounded uppercase font-bold ${
                      w.status === 'COMPLETED' 
                        ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-800' 
                        : w.status === 'RUNNING' 
                        ? 'bg-cyan-100 dark:bg-cyan-950 text-cyan-700 dark:text-cyan-400 border border-cyan-300 dark:border-cyan-800 animate-pulse' 
                        : w.status === 'TERMINATED' 
                        ? 'bg-red-100 dark:bg-red-950 text-red-700 dark:text-red-400 border border-red-300 dark:border-red-800' 
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                    }`}>
                      {w.status}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-slate-900 dark:text-slate-200 mt-2 font-sans">{w.workflow_name}</h4>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-1">{w.task_description}</p>
                  <div className="mt-3 text-[9px] font-mono text-slate-400 dark:text-slate-500 flex justify-between border-t border-slate-200 dark:border-slate-800 pt-2">
                    <span>Pattern: {w.pattern}</span>
                    <span>Created: {new Date(w.created_at).toLocaleTimeString()}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Workflow Visualizer & Pipeline Execution (Right 2 Columns) */}
        <div className="lg:col-span-2 bg-white dark:bg-[#080b12] border border-slate-200 dark:border-slate-800 rounded-xl p-6 space-y-6 shadow-sm">
          {wfDetails ? (
            <>
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2 text-xs font-mono text-tc-cyan font-bold">
                    {wfDetails.workflow.workflow_id} • {wfDetails.workflow.pattern} PIPELINE
                  </div>
                  <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 font-sans mt-0.5">{wfDetails.workflow.workflow_name}</h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{wfDetails.workflow.task_description}</p>
                </div>

                {wfDetails.workflow.status !== 'COMPLETED' && (
                  <button 
                    type="button"
                    onClick={() => handleExecuteWorkflow(wfDetails.workflow.workflow_id)}
                    className="flex items-center gap-2 bg-tc-cyan text-white dark:text-black px-5 py-2.5 rounded font-bold text-xs uppercase tracking-wider hover:opacity-90 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500">
                    <Play size={16} /> Execute Workflow
                  </button>
                )}
              </div>

              {/* Graphical Workflow Nodes Visualizer */}
              <div className="space-y-3">
                <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 uppercase tracking-widest">
                  Multi-Agent Execution Pipeline Flow
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {wfDetails.nodes.map((node) => {
                    const agentObj = agents.find(a => a.did === node.agent_did);
                    return (
                      <React.Fragment key={node.node_id}>
                        <div className={`p-4 rounded-xl border relative flex flex-col justify-between ${
                          node.status === 'COMPLETED' 
                            ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/80' 
                            : node.status === 'BLOCKED' 
                            ? 'bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800' 
                            : node.status === 'RUNNING' 
                            ? 'bg-sky-50 dark:bg-cyan-950/30 border-sky-400 dark:border-tc-cyan animate-pulse' 
                            : 'bg-slate-50 dark:bg-[#0f1623] border-slate-200 dark:border-slate-800'
                        }`}>
                          <div className="flex justify-between items-start">
                            <span className="text-[10px] font-mono font-bold text-tc-cyan bg-tc-cyan/10 px-2 py-0.5 rounded">
                              STEP {node.step_order}
                            </span>
                            <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded uppercase ${
                              node.status === 'COMPLETED' 
                                ? 'text-emerald-600 dark:text-emerald-400' 
                                : node.status === 'BLOCKED' 
                                ? 'text-red-600 dark:text-red-400' 
                                : 'text-slate-500 dark:text-slate-400'
                            }`}>
                              {node.status}
                            </span>
                          </div>

                          <div className="my-3">
                            <div className="font-bold text-xs text-slate-900 dark:text-slate-100">
                              {agentObj ? agentObj.agent_name : node.agent_did.slice(0, 16) + '...'}
                            </div>
                            <div className="text-[10px] font-mono text-slate-500 dark:text-slate-400 mt-0.5">
                              Capability: {node.required_capability}
                            </div>
                            {agentObj && (
                              <div className="text-[9px] font-mono text-slate-500 mt-1">
                                Trust: <span className={agentObj.trust_state === 'TRUSTED' ? 'text-emerald-600 dark:text-tc-success font-bold' : 'text-red-500 font-bold'}>
                                  {agentObj.trust_score?.toFixed(3)} [{agentObj.trust_state}]
                                </span>
                              </div>
                            )}
                          </div>

                          {node.output_data && (
                            <div className="mt-2 text-[9px] font-mono text-slate-700 dark:text-slate-300 bg-white dark:bg-[#080b12] border border-slate-200 dark:border-slate-800 p-2 rounded max-h-20 overflow-y-auto">
                              {node.output_data}
                            </div>
                          )}
                        </div>
                      </React.Fragment>
                    );
                  })}
                </div>
              </div>

              {/* Final Result Container */}
              {wfDetails.workflow.final_result && (
                <div className="border-t border-slate-200 dark:border-slate-800 pt-4 space-y-2">
                  <div className="text-[10px] font-mono text-tc-cyan uppercase tracking-widest flex items-center gap-2">
                    <CheckCircle2 size={14} /> Workflow Output Result
                  </div>
                  <div className="bg-slate-50 dark:bg-[#080b12] border border-slate-200 dark:border-slate-800 p-4 rounded text-xs font-mono text-slate-800 dark:text-slate-200 whitespace-pre-wrap">
                    {wfDetails.workflow.final_result}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-24 text-slate-400 dark:text-slate-500 text-xs font-mono">
              Select a workflow on the left to inspect multi-agent nodes, trigger step execution, or view attribution results.
            </div>
          )}
        </div>
      </div>

      {/* Create Workflow Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/50 dark:bg-black/80 flex items-center justify-center p-4 backdrop-blur-sm">
          <div className="bg-white dark:bg-[#080b12] border border-slate-200 dark:border-slate-800 rounded-xl max-w-xl w-full p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 uppercase">
                Define Multi-Agent Workflow
              </h3>
              <button onClick={() => setShowCreateModal(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">✕</button>
            </div>

            <form onSubmit={handleCreateWorkflow} className="space-y-4">
              <div>
                <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Workflow Name</label>
                <input 
                  type="text" required
                  value={newWf.workflow_name}
                  onChange={(e) => setNewWf(prev => ({ ...prev, workflow_name: e.target.value }))}
                  className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-700 rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none focus:border-tc-cyan"
                />
              </div>

              <div>
                <label className="block text-[11px] font-mono text-slate-600 dark:text-slate-400 uppercase mb-1">Task Description</label>
                <textarea 
                  rows={2} required
                  value={newWf.task_description}
                  onChange={(e) => setNewWf(prev => ({ ...prev, task_description: e.target.value }))}
                  className="w-full bg-slate-50 dark:bg-[#121929] border border-slate-300 dark:border-slate-700 rounded p-2 text-xs text-slate-900 dark:text-slate-200 outline-none focus:border-tc-cyan"
                />
              </div>

              <div className="space-y-3 border-t border-slate-200 dark:border-slate-800 pt-3">
                <div className="text-[10px] font-mono text-tc-cyan uppercase tracking-wider">Configure Pipeline Steps (Agents)</div>
                {newWf.nodes.map((node, idx) => (
                  <div key={idx} className="flex gap-2 items-center bg-slate-50 dark:bg-[#121929] p-2.5 rounded border border-slate-200 dark:border-slate-800">
                    <span className="text-[10px] font-mono font-bold text-slate-600 dark:text-slate-400 w-16">STEP {node.step_order}</span>
                    <select 
                      value={node.agent_did}
                      onChange={(e) => {
                        const val = e.target.value;
                        setNewWf(prev => {
                          const updated = [...prev.nodes];
                          updated[idx].agent_did = val;
                          return { ...prev, nodes: updated };
                        });
                      }}
                      className="flex-1 bg-white dark:bg-[#080b12] border border-slate-300 dark:border-slate-700 rounded p-1.5 text-xs text-slate-900 dark:text-slate-200 outline-none font-mono">
                      {agents.map(a => (
                        <option key={a.did} value={a.did}>{a.agent_name} ({a.capabilities})</option>
                      ))}
                    </select>
                    <input 
                      type="text"
                      value={node.required_capability}
                      onChange={(e) => {
                        const val = e.target.value;
                        setNewWf(prev => {
                          const updated = [...prev.nodes];
                          updated[idx].required_capability = val;
                          return { ...prev, nodes: updated };
                        });
                      }}
                      className="w-28 bg-white dark:bg-[#080b12] border border-slate-300 dark:border-slate-700 rounded p-1.5 text-xs text-slate-900 dark:text-slate-200 font-mono"
                    />
                  </div>
                ))}
              </div>

              <div className="pt-3 flex justify-end gap-3">
                <button 
                  type="button" 
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded text-xs transition-colors">
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="px-5 py-2 bg-tc-cyan text-white dark:text-black font-bold rounded text-xs uppercase hover:opacity-90 transition-all shadow-sm">
                  Initialize Pipeline
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
