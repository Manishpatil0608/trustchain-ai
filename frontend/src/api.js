import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8050/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Access token state helper
let accessToken = localStorage.getItem('tc_access_token') || null;

export const setAuthToken = (token) => {
  accessToken = token;
  if (token) {
    localStorage.setItem('tc_access_token', token);
  } else {
    localStorage.removeItem('tc_access_token');
  }
};

// Request interceptor to attach Bearer token
apiClient.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh / logout
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/auth/login')) {
      originalRequest._retry = true;
      try {
        const refreshRes = await axios.post(`${API_BASE}/auth/refresh`, {}, { withCredentials: true });
        if (refreshRes.data && refreshRes.data.access_token) {
          setAuthToken(refreshRes.data.access_token);
          originalRequest.headers['Authorization'] = `Bearer ${refreshRes.data.access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshErr) {
        setAuthToken(null);
        window.dispatchEvent(new Event('tc_auth_logout'));
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (username, password) => apiClient.post('/auth/login', { username, password }).then((r) => r.data),
  refresh: () => apiClient.post('/auth/refresh', {}).then((r) => r.data),
  logout: () => apiClient.post('/auth/logout', {}).then((r) => r.data),
  getMe: () => apiClient.get('/auth/me').then((r) => r.data),
  changePassword: (current_password, new_password) => apiClient.post('/auth/change-password', { current_password, new_password }).then((r) => r.data),
  getUsers: () => apiClient.get('/auth/users').then((r) => r.data),
  createUser: (userData) => apiClient.post('/auth/users', userData).then((r) => r.data),
  updateUserStatus: (userId, statusData) => apiClient.patch(`/auth/users/${userId}/status`, statusData).then((r) => r.data),
  revokeUserSessions: (userId) => apiClient.post(`/auth/users/${userId}/revoke-sessions`).then((r) => r.data),
  getSecurityAuditLogs: (limit = 50) => apiClient.get(`/auth/audit?limit=${limit}`).then((r) => r.data),
};

export const trustApi = {
  getAgents: () => apiClient.get('/trust/agents').then((r) => r.data),
  getAgentState: (did) => apiClient.get(`/trust/state/${encodeURIComponent(did)}`).then((r) => r.data),
  getAgentAudit: (did) => apiClient.get(`/trust/audit/${encodeURIComponent(did)}`).then((r) => r.data),
  getAllAudit: () => apiClient.get('/trust/audit').then((r) => r.data),
  getAllTelemetry: () => apiClient.get('/trust/telemetry').then((r) => r.data),
  getAgentTelemetry: (did) => apiClient.get(`/trust/telemetry/${encodeURIComponent(did)}`).then((r) => r.data),
  getAgentCredentials: (did) => apiClient.get(`/vdr/credentials/subject/${encodeURIComponent(did)}`).then((r) => r.data),
  getAgentProfile: (didOrId) => apiClient.get(`/registry/agents/${encodeURIComponent(didOrId)}`).then((r) => r.data),
  getHealth: () => axios.get('http://localhost:8050/health').then((r) => r.data),
};

export const registryApi = {
  getAgents: (params) => apiClient.get('/registry/agents', { params }).then((r) => r.data),
  getAgentProfile: (didOrId) => apiClient.get(`/registry/agents/${encodeURIComponent(didOrId)}`).then((r) => r.data),
  checkAgentHealth: (didOrId) => apiClient.post(`/registry/agents/${encodeURIComponent(didOrId)}/health`).then((r) => r.data),
  discoverAgents: (params) => apiClient.get('/registry/discover', { params }).then((r) => r.data),
  matchAgents: (payload) => apiClient.post('/registry/matching', payload).then((r) => r.data),
  updateAgentStatus: (did, status) => apiClient.post(`/registry/agents/${encodeURIComponent(did)}/status`, { status }).then((r) => r.data),
  registerAgent: (agentData) => apiClient.post('/registry/agents', agentData).then((r) => r.data),
  getStats: () => apiClient.get('/registry/stats').then((r) => r.data),
};

export default apiClient;
