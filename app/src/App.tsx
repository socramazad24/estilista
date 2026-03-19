import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import { Toaster } from '@/components/ui/sonner';
import MainLayout from '@/components/layout/MainLayout';
import Login from '@/pages/Login';
import Dashboard from '@/components/dashboard/Dashboard';
import NewSale from '@/components/sales/NewSale';

import SalesPage from '@/pages/SalesPage';
import ServicesPage from '@/pages/ServicesPage';
import InventoryPage from '@/pages/InventoryPage';
import ProvidersPage from '@/pages/ProvidersPage';
import ClientsPage from '@/pages/ClientsPage';
import EmployeesPage from '@/pages/EmployeesPage';
import LoansPage from '@/pages/LoansPage';
import AuditsPage from '@/pages/AuditsPage';
import ProfilePage from '@/pages/ProfilePage';
import HistoryPage from '@/pages/HistoryPage';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <MainLayout>{children}</MainLayout>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/ventas" element={<ProtectedRoute><SalesPage /></ProtectedRoute>} />
      <Route path="/ventas/nueva" element={<ProtectedRoute><NewSale /></ProtectedRoute>} />
      <Route path="/servicios" element={<ProtectedRoute><ServicesPage /></ProtectedRoute>} />
      <Route path="/inventario" element={<ProtectedRoute><InventoryPage /></ProtectedRoute>} />
      <Route path="/proveedores" element={<ProtectedRoute><ProvidersPage /></ProtectedRoute>} />
      <Route path="/clientes" element={<ProtectedRoute><ClientsPage /></ProtectedRoute>} />
      <Route path="/empleados" element={<ProtectedRoute><EmployeesPage /></ProtectedRoute>} />
      <Route path="/prestamos" element={<ProtectedRoute><LoansPage /></ProtectedRoute>} />
      <Route path="/auditorias" element={<ProtectedRoute><AuditsPage /></ProtectedRoute>} />
      <Route path="/historial" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
      <Route path="/perfil" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </AuthProvider>
  );
}
