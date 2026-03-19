import { useState, useCallback } from 'react';
import { salesApi, servicesApi, clientsApi } from '@/services/api';
import type { Sale, Service, Client, DashboardStats, SalesReport } from '@/types';

export function useSales() {
  const [sales, setSales] = useState<Sale[]>([]);
  const [todaySales, setTodaySales] = useState<{ sales: Sale[]; total_amount: number; count: number } | null>(null);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [report, setReport] = useState<SalesReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSales = useCallback(async (params?: Record<string, unknown>) => {
    setIsLoading(true);
    try {
      const response = await salesApi.getAll(params);
      setSales(response.data.results);
      setError(null);
    } catch (err) {
      setError('Error al cargar las ventas');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchTodaySales = useCallback(async () => {
    try {
      const response = await salesApi.getToday();
      setTodaySales(response.data);
    } catch (err) {
      console.error('Error fetching today sales:', err);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      const response = await salesApi.getDashboardStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  }, []);

  const fetchReport = useCallback(async (period: 'day' | 'week' | 'month' | 'year') => {
    try {
      const response = await salesApi.getReport(period);
      setReport(response.data);
    } catch (err) {
      console.error('Error fetching report:', err);
    }
  }, []);

  const createSale = async (saleData: Record<string, unknown>) => {
    try {
      const response = await salesApi.create(saleData);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  return {
    sales,
    todaySales,
    stats,
    report,
    isLoading,
    error,
    fetchSales,
    fetchTodaySales,
    fetchStats,
    fetchReport,
    createSale,
  };
}

export function useServices() {
  const [services, setServices] = useState<Service[]>([]);
  const [servicesByCategory, setServicesByCategory] = useState<Array<{ category: { id: number; name: string; color: string }; services: Service[] }>>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchServices = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await servicesApi.getActive();
      setServices(response.data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchServicesByCategory = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await servicesApi.getByCategory();
      setServicesByCategory(response.data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    services,
    servicesByCategory,
    isLoading,
    fetchServices,
    fetchServicesByCategory,
  };
}

export function useClients() {
  const [clients, setClients] = useState<Client[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchClients = useCallback(async (params?: Record<string, unknown>) => {
    setIsLoading(true);
    try {
      const response = await clientsApi.getAll(params);
      setClients(response.data.results);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const searchClients = useCallback(async (search: string) => {
    if (search.length < 2) return;
    setIsLoading(true);
    try {
      const response = await clientsApi.getAll({ search });
      setClients(response.data.results);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createClient = async (clientData: Partial<Client>) => {
    try {
      const response = await clientsApi.create(clientData);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  return {
    clients,
    isLoading,
    fetchClients,
    searchClients,
    createClient,
  };
}
