import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi, setAuthToken } from '../api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCurrentUser = async () => {
    try {
      const userData = await authApi.getMe();
      setUser(userData);
      setError(null);
    } catch (err) {
      setUser(null);
      setAuthToken(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('tc_access_token');
    if (token) {
      setAuthToken(token);
      fetchCurrentUser();
    } else {
      setLoading(false);
    }

    const handleGlobalLogout = () => {
      setUser(null);
      setError(null);
    };

    window.addEventListener('tc_auth_logout', handleGlobalLogout);
    return () => window.removeEventListener('tc_auth_logout', handleGlobalLogout);
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    try {
      const data = await authApi.login(username, password);
      setAuthToken(data.access_token);
      setUser(data.user);
      setLoading(false);
      return data;
    } catch (err) {
      setLoading(false);
      const msg = err.response?.data?.detail || 'Authentication failed. Please check credentials.';
      setError(msg);
      throw new Error(msg);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authApi.logout();
    } catch (err) {
      // Ignore logout errors
    } finally {
      setAuthToken(null);
      setUser(null);
      setError(null);
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    refreshUser: fetchCurrentUser,
    isAdmin: user?.role?.toUpperCase() === 'ADMIN',
    isOperator: ['ADMIN', 'OPERATOR'].includes(user?.role?.toUpperCase()),
    isViewer: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
