// User types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  phone?: string;
  role: 'admin' | 'stylist' | 'cashier' | 'assistant';
  is_active: boolean;
  date_joined: string;
  last_login?: string;
}

export interface UserActivity {
  id: number;
  user: number;
  user_name?: string;
  action: string;
  description: string;
  ip_address?: string;
  created_at: string;
}

// Service types
export interface ServiceCategory {
  id: number;
  name: string;
  description: string;
  color: string;
  is_active: boolean;
  service_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Service {
  id: number;
  category: number;
  category_name?: string;
  category_color?: string;
  name: string;
  description: string;
  price: number;
  duration_minutes: number;
  duration_display?: string;
  duration_short?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Client types
export interface Client {
  id: number;
  first_name: string;
  last_name: string;
  full_name?: string;
  phone: string;
  email?: string;
  address?: string;
  notes?: string;
  sales_count?: number;
  total_spent?: number;
  created_at: string;
  updated_at: string;
}

// Sale types
export interface SaleItem {
  id: number;

  // 🔥 OPCIONALES (clave)
  service?: number;

  service_name?: string;

  quantity: number;
  unit_price: number;

  // 🔥 OPCIONAL
  discount?: number;

  total: number;

  // opcional si lo usas en otros lados
  service_detail?: any;
}

export interface Sale {
  id: number;

  invoice_number?: string;

  client?: number;
  client_name?: string;

  stylist?: number;
  stylist_name?: string;

  cashier?: number;
  cashier_name?: string;

  date?: string;

  items: SaleItem[];

  subtotal: number;
  discount?: number;
  tax?: number;
  total: number;

  payment_method?: string;
  payment_method_display?: string;

  status?: string;

  notes?: string;

  created_at?: string;
}

// Inventory types
export interface ProductCategory {
  id: number;
  name: string;
  description: string;
  is_active: boolean;
  product_count?: number;
  created_at: string;
}

export interface Product {
  id: number;
  category: number;
  category_name?: string;
  provider?: number;
  provider_name?: string;
  name: string;
  description: string;
  sku: string;
  barcode?: string;
  unit: string;
  unit_display?: string;
  stock: number;
  min_stock: number;
  max_stock?: number;
  purchase_price: number;
  sale_price: number;
  location?: string;
  is_low_stock?: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface InventoryMovement {
  id: number;
  product: number;
  product_name?: string;
  product_sku?: string;
  movement_type: 'entry' | 'exit' | 'adjustment' | 'return';
  movement_type_display?: string;
  quantity: number;
  previous_stock: number;
  new_stock: number;
  unit_price: number;
  total_price: number;
  reference?: string;
  notes?: string;
  created_by?: number;
  created_by_name?: string;
  created_at: string;
}

// Provider types
export interface Provider {
  id: number;
  name: string;
  contact_name?: string;
  phone?: string;
  email?: string;
  address?: string;
  city?: string;
  nit?: string;
  website?: string;
  notes?: string;
  status: 'active' | 'inactive';
  status_display?: string;
  created_at: string;
  updated_at: string;
}

// Employee types
export interface Employee {
  id: number;
  user?: number;
  user_name?: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  document_type: string;
  document_number: string;
  phone?: string;
  email?: string;
  address?: string;
  birth_date?: string;
  hire_date: string;
  termination_date?: string;
  contract_type: 'full_time' | 'part_time' | 'freelance';
  contract_type_display?: string;
  base_salary: number;
  commission_rate: number;
  status: 'active' | 'inactive' | 'on_leave';
  status_display?: string;
  active_loans_total?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface EmployeeLoan {
  id: number;
  employee: number;
  employee_name?: string;
  amount: number;
  interest_rate: number;
  total_amount: number;
  remaining_amount: number;
  installment_amount: number;
  number_of_installments: number;
  paid_installments: number;
  request_date: string;
  approval_date?: string;
  first_payment_date?: string;
  status: 'active' | 'paid' | 'cancelled';
  status_display?: string;
  reason?: string;
  approved_by?: number;
  approved_by_name?: string;
  progress_percentage?: number;
  notes?: string;
  created_at: string;
}

// Audit types
export interface AuditLog {
  id: number;
  user?: number;
  user_name?: string;
  action: 'CREATE' | 'UPDATE' | 'DELETE' | 'LOGIN' | 'LOGOUT' | 'VIEW' | 'EXPORT' | 'PRINT' | 'OTHER';
  action_display?: string;
  model_name: string;
  object_id?: string;
  object_repr?: string;
  previous_data?: Record<string, unknown>;
  new_data?: Record<string, unknown>;
  ip_address?: string;
  user_agent?: string;
  description?: string;
  created_at: string;
}

// Dashboard types
export interface DashboardStats {
  today: {
    total: number;
    count: number;
  };
  week: {
    total: number;
  };
  month: {
    total: number;
  };
  top_services: Array<{
    name: string;
    count: number;
  }>;
}

export interface SalesReport {
  period: string;
  start_date: string;
  end_date: string;
  total_sales: number;
  total_amount: number;
  average_sale: number;
  by_payment_method: Record<string, { count: number; amount: number }>;
  by_service: Array<{
    name: string;
    count: number;
    total: number;
  }>;
}

// Auth types
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

// API Response types
export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  [key: string]: string | string[] | undefined;
}
