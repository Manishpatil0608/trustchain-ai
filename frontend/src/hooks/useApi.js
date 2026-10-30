import { useState, useEffect } from 'react';
import { trustApi, registryApi } from '../api';

export function useApi(apiFunc, deps = []) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;
        setLoading(true);
        apiFunc()
            .then(res => {
                if (isMounted) {
                    setData(res);
                    setError(null);
                }
            })
            .catch(err => {
                if (isMounted) setError(err.message || 'API Offline');
            })
            .finally(() => {
                if (isMounted) setLoading(false);
            });
        return () => { isMounted = false; };
    }, deps);

    return { data, loading, error };
}

export function useAgents() { return useApi(trustApi.getAgents); }
export function useRegistryAgents(params) { return useApi(() => registryApi.getAgents(params), [JSON.stringify(params)]); }
export function useAllTelemetry() { return useApi(trustApi.getAllTelemetry); }
export function useAllAudit() { return useApi(trustApi.getAllAudit); }
export function useHealth() { return useApi(trustApi.getHealth); }
