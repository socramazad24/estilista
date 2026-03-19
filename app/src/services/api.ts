import axios, { type AxiosInstance } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const buildCrudApi = (base: string) => ({
  getAll: (params?: Record<string, unknown>) => api.get(base, { params }),
  getOne: (id: number | string) => api.get(`${base}${id}/`),
  create: (data: unknown) => api.post(base, data),
  update: (id: number | string, data: unknown) => api.put(`${base}${id}/`, data),
  partialUpdate: (id: number | string, data: unknown) => api.patch(`${base}${id}/`, data),
  remove: (id: number | string) => api.delete(`${base}${id}/`),
});

export const authApi = {
  login: (data: { username: string; password: string }) => api.post('/token/', data),
  refresh: (refresh: string) => api.post('/token/refresh/', { refresh }),
  getCurrentUser: () => api.get('/users/me/'),
  changePassword: (data: { old_password: string; new_password: string }) =>
    api.post('/users/change_password/', data),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

export const usersApi = {
  ...buildCrudApi('/users/'),
  getStylists: () => api.get('/users/', { params: { role: 'stylist' } }),
};

export const salesApi = {
  ...buildCrudApi('/sales/'),
  getToday: () => api.get('/sales/today/'),
  getReport: (period: 'day' | 'week' | 'month' | 'year') =>
    api.get('/sales/report/', { params: { period } }),
  getDashboardStats: () => api.get('/sales/dashboard_stats/'),
};

export const clientsApi = {
  ...buildCrudApi('/sales/clients/'),
  getFrequent: () => api.get('/sales/clients/frequent/'),
};

export const servicesApi = {
  ...buildCrudApi('/services/'),
  getCategories: () => api.get('/services/categories/'),
  getByCategory: () => api.get('/services/by_category/'),
  getActive: () => api.get('/services/active/'),
  getPackages: () => api.get('/services/packages/'),
};

export const inventoryApi = {
  products: buildCrudApi('/inventory/products/'),
  categories: buildCrudApi('/inventory/categories/'),
  movements: {
    ...buildCrudApi('/inventory/movements/'),
    recent: () => api.get('/inventory/movements/recent/'),
    byProduct: (productId: number | string) =>
      api.get('/inventory/movements/by_product/', { params: { productid: productId } }),
  },
  counts: {
    ...buildCrudApi('/inventory/counts/'),
    start: (id: number | string) => api.post(`/inventory/counts/${id}/start/`),
    complete: (id: number | string, data: unknown) => api.post(`/inventory/counts/${id}/complete/`, data),
  },
  lowStock: () => api.get('/inventory/products/low_stock/'),
  activeProducts: () => api.get('/inventory/products/active/'),
};

export const providersApi = {
  providers: {
    ...buildCrudApi('/providers/'),
    active: () => api.get('/providers/active/'),
  },
  contacts: buildCrudApi('/providers/contacts/'),
  purchaseOrders: {
    ...buildCrudApi('/providers/purchase-orders/'),
    send: (id: number | string) => api.post(`/providers/purchase-orders/${id}/send/`),
    receive: (id: number | string) => api.post(`/providers/purchase-orders/${id}/receive/`),
  },
};

export const employeesApi = {
  employees: buildCrudApi('/employees/'),
  loans: {
    ...buildCrudApi('/employees/loans/'),
    registerPayment: (id: number | string, data: unknown) =>
      api.post(`/employees/loans/${id}/register_payment/`, data),
  },
};

export const auditsApi = {
  logs: {
    getAll: (params?: Record<string, unknown>) => api.get('/audits/logs/', { params }),
    summary: () => api.get('/audits/logs/summary/'),
  },
};

export default api;
