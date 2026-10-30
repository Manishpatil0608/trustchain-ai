import React, { useState, useEffect } from 'react';
import { Users, UserPlus, ShieldAlert, Key, Lock, CheckCircle2, XCircle, RefreshCw, AlertCircle, Search, ShieldCheck, UserCheck } from 'lucide-react';
import { authApi } from '../api';
import { useAuth } from '../context/AuthContext';

export default function UserManagement() {
  const { user: currentUser, isAdmin } = useAuth();
  const [activeTab, setActiveTab] = useState('users'); // 'users' | 'create' | 'audit'
  
  // Users state
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [userSearch, setUserSearch] = useState('');
  
  // Create user form state
  const [newUsername, setNewUsername] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newRole, setNewRole] = useState('OPERATOR');
  const [creatingUser, setCreatingUser] = useState(false);
  const [createSuccess, setCreateSuccess] = useState('');
  const [createError, setCreateError] = useState('');

  // Audit logs state
  const [auditLogs, setAuditLogs] = useState([]);
  const [loadingAudit, setLoadingAudit] = useState(false);

  // Global error/status message
  const [actionMessage, setActionMessage] = useState({ type: '', text: '' });

  const fetchUsers = async () => {
    setLoadingUsers(true);
    try {
      const data = await authApi.getUsers();
      setUsers(data);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to load user registry.' });
    } finally {
      setLoadingUsers(false);
    }
  };

  const fetchAuditLogs = async () => {
    setLoadingAudit(true);
    try {
      const data = await authApi.getSecurityAuditLogs(100);
      setAuditLogs(data);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to load security audit trail.' });
    } finally {
      setLoadingAudit(false);
    }
  };

  useEffect(() => {
    if (isAdmin) {
      if (activeTab === 'users') fetchUsers();
      if (activeTab === 'audit') fetchAuditLogs();
    }
  }, [activeTab, isAdmin]);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setCreatingUser(true);
    setCreateSuccess('');
    setCreateError('');

    try {
      const newUser = await authApi.createUser({
        username: newUsername,
        email: newEmail || null,
        password: newPassword,
        role: newRole,
      });
      setCreateSuccess(`User '${newUser.username}' successfully created with role '${newUser.role}'.`);
      setNewUsername('');
      setNewEmail('');
      setNewPassword('');
      setNewRole('OPERATOR');
      fetchUsers();
    } catch (err) {
      setCreateError(err.response?.data?.detail || 'Failed to create user account.');
    } finally {
      setCreatingUser(false);
    }
  };

  const handleToggleStatus = async (userToToggle) => {
    try {
      const updated = await authApi.updateUserStatus(userToToggle.id, {
        is_active: !userToToggle.is_active,
        role: userToToggle.role,
      });
      setActionMessage({
        type: 'success',
        text: `User '${updated.username}' account status changed to ${updated.is_active ? 'ACTIVE' : 'DISABLED'}.`,
      });
      fetchUsers();
    } catch (err) {
      setActionMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to update user status.' });
    }
  };

  const handleRevokeSessions = async (userId, username) => {
    try {
      await authApi.revokeUserSessions(userId);
      setActionMessage({
        type: 'success',
        text: `All active refresh sessions for user '${username}' have been revoked.`,
      });
    } catch (err) {
      setActionMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to revoke sessions.' });
    }
  };

  const getRoleBadge = (role) => {
    switch (role?.toUpperCase()) {
      case 'ADMIN':
        return 'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/50 dark:text-purple-300 dark:border-purple-800/50';
      case 'OPERATOR':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200 dark:bg-tc-cyan/10 dark:text-tc-cyan dark:border-tc-cyan/40 dark:shadow-[0_0_8px_rgba(0,240,255,0.15)]';
      case 'VIEWER':
      default:
        return 'bg-[#EAF3FF] text-[#1D4ED8] border-[#BFDBFE] dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    }
  };

  if (!isAdmin) {
    return (
      <div className="p-8 text-center bg-white dark:bg-[#090d16] border border-red-200 dark:border-red-900/40 rounded-xl shadow-sm">
        <ShieldAlert size={48} className="mx-auto text-red-500 mb-4" />
        <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider">Access Denied</h2>
        <p className="text-slate-600 dark:text-slate-400 text-xs mt-2 font-mono">
          Platform User Management requires administrative privileges (ADMIN role).
        </p>
      </div>
    );
  }

  const filteredUsers = users.filter(
    (u) =>
      u.username.toLowerCase().includes(userSearch.toLowerCase()) ||
      (u.email && u.email.toLowerCase().includes(userSearch.toLowerCase())) ||
      u.role.toLowerCase().includes(userSearch.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-[#1a2333]">
        <div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="text-tc-cyan" size={28} />
            <h1 className="text-2xl font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">
              Platform User Management & Audit
            </h1>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 font-mono mt-1">
            RBAC Access Control, User Directory, and Platform Security Audit Log
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 bg-slate-100 dark:bg-[#080b12] p-1 border border-slate-200 dark:border-[#1a2333] rounded-lg">
          <button
            onClick={() => setActiveTab('users')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === 'users'
                ? 'bg-white dark:bg-[#121929] text-tc-cyan border border-slate-300 dark:border-tc-cyan/40 shadow-xs dark:shadow-[0_0_10px_rgba(0,240,255,0.2)] font-semibold'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Users size={14} />
            <span>User Directory ({users.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('create')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === 'create'
                ? 'bg-white dark:bg-[#121929] text-tc-cyan border border-slate-300 dark:border-tc-cyan/40 shadow-xs dark:shadow-[0_0_10px_rgba(0,240,255,0.2)] font-semibold'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <UserPlus size={14} />
            <span>Create User</span>
          </button>
          <button
            onClick={() => setActiveTab('audit')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === 'audit'
                ? 'bg-white dark:bg-[#121929] text-tc-cyan border border-slate-300 dark:border-tc-cyan/40 shadow-xs dark:shadow-[0_0_10px_rgba(0,240,255,0.2)] font-semibold'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <ShieldAlert size={14} />
            <span>Audit Trail</span>
          </button>
        </div>
      </div>

      {/* Global Status Message */}
      {actionMessage.text && (
        <div
          className={`p-3.5 rounded-lg flex items-center justify-between border text-xs font-mono ${
            actionMessage.type === 'error'
              ? 'bg-red-50 dark:bg-red-950/40 border-red-200 dark:border-red-500/50 text-red-800 dark:text-red-300'
              : 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-500/50 text-emerald-800 dark:text-emerald-300'
          }`}
        >
          <div className="flex items-center gap-2">
            {actionMessage.type === 'error' ? <AlertCircle size={16} /> : <CheckCircle2 size={16} />}
            <span>{actionMessage.text}</span>
          </div>
          <button
            onClick={() => setActionMessage({ type: '', text: '' })}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
          >
            ×
          </button>
        </div>
      )}

      {/* TAB 1: USER DIRECTORY */}
      {activeTab === 'users' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white dark:bg-[#090d16] p-4 rounded-xl border border-slate-200 dark:border-[#1e293b] shadow-sm">
            <div className="relative w-full sm:w-80">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
              <input
                type="text"
                value={userSearch}
                onChange={(e) => setUserSearch(e.target.value)}
                placeholder="Search username, email, role..."
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2 pl-9 pr-4 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan"
              />
            </div>
            <button
              onClick={fetchUsers}
              disabled={loadingUsers}
              className="flex items-center gap-2 px-3 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-[#121929] dark:hover:bg-[#1a2333] border border-slate-200 dark:border-tc-border text-slate-700 dark:text-slate-300 rounded-lg text-xs font-mono transition-colors"
            >
              <RefreshCw size={14} className={loadingUsers ? 'animate-spin' : ''} />
              <span>Refresh</span>
            </button>
          </div>

          <div className="bg-white dark:bg-[#090d16] border border-slate-200 dark:border-[#1e293b] rounded-xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans">
                <thead className="bg-slate-50 dark:bg-[#05070a] border-b border-slate-200 dark:border-[#1e293b] text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 tracking-wider">
                  <tr>
                    <th className="p-4">User</th>
                    <th className="p-4">Role</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Created</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-[#1e293b]/60">
                  {filteredUsers.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="p-8 text-center text-slate-500 font-mono">
                        {loadingUsers ? 'Loading platform user registry...' : 'No users found.'}
                      </td>
                    </tr>
                  ) : (
                    filteredUsers.map((u) => (
                      <tr key={u.id} className="hover:bg-slate-50 dark:hover:bg-[#0d1322] transition-colors">
                        <td className="p-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-[#121929] border border-tc-cyan/30 flex items-center justify-center font-mono font-bold text-tc-cyan text-xs">
                              {u.username.charAt(0).toUpperCase()}
                            </div>
                            <div>
                              <div className="font-semibold text-slate-900 dark:text-slate-200 flex items-center gap-2">
                                <span>{u.username}</span>
                                {u.id === currentUser?.id && (
                                  <span className="text-[9px] font-mono uppercase bg-tc-cyan/20 text-tc-cyan px-1.5 py-0.5 rounded border border-tc-cyan/40">
                                    YOU
                                  </span>
                                )}
                              </div>
                              <div className="text-[11px] text-slate-500 font-mono">
                                {u.email || 'No email associated'}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="p-4 align-middle">
                          <span className={`inline-flex items-center justify-center px-[10px] py-[5px] rounded-[6px] text-[11px] font-semibold uppercase tracking-wider border leading-none ${getRoleBadge(u.role)}`}>
                            {u.role}
                          </span>
                        </td>
                        <td className="p-4">
                          {u.is_active ? (
                            <span className="inline-flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-mono text-[11px] font-semibold">
                              <CheckCircle2 size={13} />
                              <span>Active</span>
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 text-red-600 dark:text-red-400 font-mono text-[11px] font-semibold">
                              <XCircle size={13} />
                              <span>Disabled</span>
                            </span>
                          )}
                        </td>
                        <td className="p-4 font-mono text-[11px] text-slate-500 dark:text-slate-400">
                          {new Date(u.created_at).toLocaleDateString()}
                        </td>
                        <td className="p-4 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => handleToggleStatus(u)}
                              disabled={u.id === currentUser?.id}
                              className={`px-3 py-1.5 rounded text-[10px] font-mono uppercase transition-colors border ${
                                u.is_active
                                  ? 'bg-red-50 hover:bg-red-100 border-red-200 text-red-700 dark:bg-red-950/40 dark:hover:bg-red-900/60 dark:border-red-500/40 dark:text-red-300'
                                  : 'bg-emerald-50 hover:bg-emerald-100 border-emerald-200 text-emerald-700 dark:bg-emerald-950/40 dark:hover:bg-emerald-900/60 dark:border-emerald-500/40 dark:text-emerald-300'
                              } disabled:opacity-30 disabled:cursor-not-allowed`}
                            >
                              {u.is_active ? 'Disable' : 'Enable'}
                            </button>
                            <button
                              onClick={() => handleRevokeSessions(u.id, u.username)}
                              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border-slate-300 text-slate-700 dark:bg-[#121929] dark:hover:bg-[#1e293b] border dark:border-slate-700 dark:text-slate-300 rounded text-[10px] font-mono uppercase transition-colors"
                              title="Revoke all active sessions"
                            >
                              Revoke Sessions
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: CREATE USER */}
      {activeTab === 'create' && (
        <div className="max-w-xl mx-auto bg-white dark:bg-[#090d16] border border-slate-200 dark:border-[#1e293b] rounded-xl p-6 shadow-sm space-y-6">
          <div>
            <h2 className="text-lg font-bold tracking-wider text-slate-900 dark:text-slate-100 uppercase">Create New Platform User</h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 font-mono mt-1">Assign RBAC roles (ADMIN, OPERATOR, VIEWER) for human platform users.</p>
          </div>

          {createSuccess && (
            <div className="p-3.5 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-500/50 rounded-lg text-emerald-800 dark:text-emerald-300 text-xs font-mono flex items-center gap-2">
              <CheckCircle2 size={16} />
              <span>{createSuccess}</span>
            </div>
          )}

          {createError && (
            <div className="p-3.5 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-500/50 rounded-lg text-red-800 dark:text-red-300 text-xs font-mono flex items-center gap-2">
              <AlertCircle size={16} />
              <span>{createError}</span>
            </div>
          )}

          <form onSubmit={handleCreateUser} className="space-y-4">
            <div>
              <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-1.5">
                Username
              </label>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="e.g. operator_alex"
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 px-3.5 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan"
                required
              />
            </div>

            <div>
              <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-1.5">
                Email Address (Optional)
              </label>
              <input
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                placeholder="e.g. alex@trustchain.local"
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 px-3.5 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan"
              />
            </div>

            <div>
              <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-1.5">
                Password (Min 8 Characters)
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 px-3.5 text-xs text-slate-900 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-tc-cyan"
                required
                minLength={8}
              />
            </div>

            <div>
              <label className="block text-[10px] font-mono text-slate-600 dark:text-slate-400 uppercase tracking-widest mb-1.5">
                Platform Role
              </label>
              <select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#030508] border border-slate-300 dark:border-[#1e293b] rounded-lg py-2.5 px-3.5 text-xs text-slate-900 dark:text-slate-200 focus:outline-none focus:border-tc-cyan font-mono"
              >
                <option value="VIEWER">VIEWER - Read-only dashboard access</option>
                <option value="OPERATOR">OPERATOR - Execute agent workflows & trigger evaluations</option>
                <option value="ADMIN">ADMIN - Full administrative access & governance controls</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={creatingUser}
              className="w-full bg-tc-cyan text-white dark:text-black font-semibold font-mono text-xs uppercase tracking-widest py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all shadow-[0_0_15px_rgba(0,240,255,0.15)] hover:bg-cyan-600 dark:hover:bg-cyan-300 disabled:opacity-50 mt-4"
            >
              {creatingUser ? (
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full border-2 border-white dark:border-black border-t-transparent animate-spin"></div>
                  Creating User...
                </span>
              ) : (
                <>
                  <UserPlus size={16} />
                  <span>Create User Account</span>
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {/* TAB 3: AUDIT TRAIL */}
      {activeTab === 'audit' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between bg-white dark:bg-[#090d16] p-4 rounded-xl border border-slate-200 dark:border-[#1e293b] shadow-sm">
            <h2 className="text-sm font-mono uppercase text-slate-800 dark:text-slate-300 tracking-wider">
              Security Audit Event Log (Last {auditLogs.length} Events)
            </h2>
            <button
              onClick={fetchAuditLogs}
              disabled={loadingAudit}
              className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-[#121929] dark:hover:bg-[#1a2333] border border-slate-200 dark:border-tc-border text-slate-700 dark:text-slate-300 rounded-lg text-xs font-mono transition-colors"
            >
              <RefreshCw size={14} className={loadingAudit ? 'animate-spin' : ''} />
              <span>Refresh Logs</span>
            </button>
          </div>

          <div className="bg-white dark:bg-[#090d16] border border-slate-200 dark:border-[#1e293b] rounded-xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans">
                <thead className="bg-slate-50 dark:bg-[#05070a] border-b border-slate-200 dark:border-[#1e293b] text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 tracking-wider">
                  <tr>
                    <th className="p-4">Timestamp</th>
                    <th className="p-4">Event Type</th>
                    <th className="p-4">User</th>
                    <th className="p-4">Client IP</th>
                    <th className="p-4">Result</th>
                    <th className="p-4">Details</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-[#1e293b]/60 font-mono text-[11px]">
                  {auditLogs.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="p-8 text-center text-slate-500">
                        {loadingAudit ? 'Loading security audit logs...' : 'No audit events logged.'}
                      </td>
                    </tr>
                  ) : (
                    auditLogs.map((log) => (
                      <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-[#0d1322] transition-colors">
                        <td className="p-4 text-slate-500 dark:text-slate-400">
                          {new Date(log.timestamp).toLocaleString()}
                        </td>
                        <td className="p-4 text-tc-cyan font-bold">
                          {log.event_type}
                        </td>
                        <td className="p-4 text-slate-900 dark:text-slate-200 font-semibold">
                          {log.username || 'N/A'}
                        </td>
                        <td className="p-4 text-slate-500 dark:text-slate-400">
                          {log.client_ip || '127.0.0.1'}
                        </td>
                        <td className="p-4">
                          {log.status === 'SUCCESS' ? (
                            <span className="text-emerald-600 dark:text-emerald-400 font-bold">SUCCESS</span>
                          ) : (
                            <span className="text-red-600 dark:text-red-400 font-bold">FAILURE</span>
                          )}
                        </td>
                        <td className="p-4 text-slate-600 dark:text-slate-400 max-w-xs truncate" title={log.details}>
                          {log.details || '-'}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
