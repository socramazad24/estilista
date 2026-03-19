import axios, { type AxiosInstance, type AxiosError } from 'axios';
import type { 
  User, UserActivity, ApiResponse, LoginCredentials, AuthResponse,
  ServiceCategory, Service, Client, Sale, ProductCategory, Product,
  InventoryMovement, Provider, Employee, EmployeeLoan, AuditLog,
  DashboardStats, SalesReport
} from '@/types';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // ← AGREGAR ESTO para CORS con credenciales
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // ← Verificar formato Bearer
    }
    return config;
  },
  (error) => Promise.reject(error)
);


// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && originalRequest) {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, logout user
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: (credentials: LoginCredentials) => 
    axios.post<AuthResponse>(`${API_BASE_URL}/token/`, credentials),
  
  refresh: (refresh: string) => 
    axios.post<{ access: string }>(`${API_BASE_URL}/token/refresh/`, { refresh }),
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  getCurrentUser: () => api.get<User>('/users/me/'),
};

// Users API
export const usersApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<User>>('/users/', { params }),
  
  getById: (id: number) => api.get<User>(`/users/${id}/`),
  
  create: (data: Partial<User>) => api.post<User>('/users/', data),
  
  update: (id: number, data: Partial<User>) => api.patch<User>(`/users/${id}/`, data),
  
  delete: (id: number) => api.delete(`/users/${id}/`),
  
  changePassword: (data: { old_password: string; new_password: string; new_password_confirm: string }) => 
    api.post('/users/change_password/', data),
  
  getStylists: () => api.get<User[]>('/users/stylists/'),
  
  getActivities: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<UserActivity>>('/users/activities/', { params }),
};

// Services API
export const servicesApi = {
  getCategories: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<ServiceCategory>>('/services/categories/', { params }),
  
  createCategory: (data: Partial<ServiceCategory>) => 
    api.post<ServiceCategory>('/services/categories/', data),
  
  updateCategory: (id: number, data: Partial<ServiceCategory>) => 
    api.patch<ServiceCategory>(`/services/categories/${id}/`, data),
  
  deleteCategory: (id: number) => api.delete(`/services/categories/${id}/`),
  
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Service>>('/services/', { params }),
  
  getActive: () => api.get<Service[]>('/services/active/'),
  
  getByCategory: () => api.get<Array<{ category: ServiceCategory; services: Service[] }>>('/services/by_category/'),
  
  getTopServices: () => api.get<Service[]>('/services/top_services/'),
  
  getById: (id: number) => api.get<Service>(`/services/${id}/`),
  
  create: (data: Partial<Service>) => api.post<Service>('/services/', data),
  
  update: (id: number, data: Partial<Service>) => api.patch<Service>(`/services/${id}/`, data),
  
  delete: (id: number) => api.delete(`/services/${id}/`),
};

// Clients API
export const clientsApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Client>>('/sales/clients/', { params }),
  
  getFrequent: () => api.get<Client[]>('/sales/clients/frequent/'),
  
  getById: (id: number) => api.get<Client>(`/sales/clients/${id}/`),
  
  create: (data: Partial<Client>) => api.post<Client>('/sales/clients/', data),
  
  update: (id: number, data: Partial<Client>) => api.patch<Client>(`/sales/clients/${id}/`, data),
  
  delete: (id: number) => api.delete(`/sales/clients/${id}/`),
};

// Sales API
export const salesApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Sale>>('/sales/', { params }),
  
  getToday: () => api.get<{ sales: Sale[]; total_amount: number; count: number }>('/sales/today/'),
  
  getById: (id: number) => api.get<Sale>(`/sales/${id}/`),
  
  create: (data: Record<string, unknown>) => api.post<Sale>('/sales/', data),
  
  update: (id: number, data: Partial<Sale>) => api.patch<Sale>(`/sales/${id}/`, data),
  
  delete: (id: number) => api.delete(`/sales/${id}/`),
  
  getReport: (period: 'day' | 'week' | 'month' | 'year') => 
    api.get<SalesReport>(`/sales/report/?period=${period}`),
  
  getDashboardStats: () => api.get<DashboardStats>('/sales/dashboard_stats/'),
};

// Products API
export const productsApi = {
  getCategories: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<ProductCategory>>('/inventory/categories/', { params }),
  
  createCategory: (data: Partial<ProductCategory>) => 
    api.post<ProductCategory>('/inventory/categories/', data),
  
  updateCategory: (id: number, data: Partial<ProductCategory>) => 
    api.patch<ProductCategory>(`/inventory/categories/${id}/`, data),
  
  deleteCategory: (id: number) => api.delete(`/inventory/categories/${id}/`),
  
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Product>>('/inventory/products/', { params }),
  
  getActive: () => api.get<Product[]>('/inventory/products/active/'),
  
  getLowStock: () => api.get<Product[]>('/inventory/products/low_stock/'),
  
  getById: (id: number) => api.get<Product>(`/inventory/products/${id}/`),
  
  create: (data: Partial<Product>) => api.post<Product>('/inventory/products/', data),
  
  update: (id: number, data: Partial<Product>) => api.patch<Product>(`/inventory/products/${id}/`, data),
  
  delete: (id: number) => api.delete(`/inventory/products/${id}/`),
};

// Inventory Movements API
export const movementsApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<InventoryMovement>>('/inventory/movements/', { params }),
  
  getRecent: () => api.get<InventoryMovement[]>('/inventory/movements/recent/'),
  
  getByProduct: (productId: number) => 
    api.get<InventoryMovement[]>(`/inventory/movements/by_product/?product_id=${productId}`),
  
  create: (data: Partial<InventoryMovement>) => 
    api.post<InventoryMovement>('/inventory/movements/', data),
};

// Providers API
export const providersApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Provider>>('/providers/', { params }),
  
  getActive: () => api.get<Provider[]>('/providers/active/'),
  
  getById: (id: number) => api.get<Provider>(`/providers/${id}/`),
  
  create: (data: Partial<Provider>) => api.post<Provider>('/providers/', data),
  
  update: (id: number, data: Partial<Provider>) => api.patch<Provider>(`/providers/${id}/`, data),
  
  delete: (id: number) => api.delete(`/providers/${id}/`),
};

// Employees API
export const employeesApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<Employee>>('/employees/', { params }),
  
  getActive: () => api.get<Employee[]>('/employees/active/'),
  
  getById: (id: number) => api.get<Employee>(`/employees/${id}/`),
  
  create: (data: Partial<Employee>) => api.post<Employee>('/employees/', data),
  
  update: (id: number, data: Partial<Employee>) => api.patch<Employee>(`/employees/${id}/`, data),
  
  delete: (id: number) => api.delete(`/employees/${id}/`),
  
  getLoans: (employeeId: number) => api.get<EmployeeLoan[]>(`/employees/${employeeId}/loans/`),
};

// Loans API
export const loansApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<EmployeeLoan>>('/employees/loans/', { params }),
  
  getActive: () => api.get<EmployeeLoan[]>('/employees/loans/active/'),
  
  getSummary: () => api.get<{ total_active_loans: number; total_remaining_amount: number }>('/employees/loans/summary/'),
  
  create: (data: Partial<EmployeeLoan>) => api.post<EmployeeLoan>('/employees/loans/', data),
  
  approve: (id: number) => api.post<EmployeeLoan>(`/employees/loans/${id}/approve/`, {}),
  
  registerPayment: (id: number, paymentId: number) => 
    api.post<EmployeeLoan>(`/employees/loans/${id}/register_payment/`, { payment_id: paymentId }),
};

// Audit Logs API
export const auditApi = {
  getAll: (params?: Record<string, unknown>) => 
    api.get<ApiResponse<AuditLog>>('/audits/logs/', { params }),
  
  getRecent: () => api.get<AuditLog[]>('/audits/logs/recent/'),
  
  getSummary: (days?: number) => 
    api.get(`/audits/logs/summary/?days=${days || 7}`),
  
  getDashboard: () => api.get('/audits/logs/dashboard/'),
};

export default api;
