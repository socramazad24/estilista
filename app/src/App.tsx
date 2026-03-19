import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import { Toaster } from '@/components/ui/sonner';
import MainLayout from '@/components/layout/MainLayout';
import Login from '@/pages/Login';
import Dashboard from '@/components/dashboard/Dashboard';
import NewSale from '@/components/sales/NewSale';

// Protected Route Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <MainLayout>{children}</MainLayout>;
}

// Placeholder components for other routes
function Ventas() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Historial de Ventas</h1>
      <p className="text-slate-500">Aquí se mostrará el historial completo de ventas.</p>
    </div>
  );
}

function Servicios() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Gestión de Servicios</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los servicios ofrecidos.</p>
    </div>
  );
}

function Inventario() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Gestión de Inventario</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los productos del inventario.</p>
    </div>
  );
}

function Proveedores() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Gestión de Proveedores</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los proveedores.</p>
    </div>
  );
}

function Clientes() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Gestión de Clientes</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los clientes.</p>
    </div>
  );
}

function Empleados() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Gestión de Empleados</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los empleados.</p>
    </div>
  );
}

function Prestamos() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Préstamos a Empleados</h1>
      <p className="text-slate-500">Aquí se podrán gestionar los préstamos a empleados.</p>
    </div>
  );
}

function Auditorias() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Auditorías</h1>
      <p className="text-slate-500">Aquí se mostrarán los registros de auditoría.</p>
    </div>
  );
}

function Historial() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Historial</h1>
      <p className="text-slate-500">Aquí se mostrará el historial de actividades.</p>
    </div>
  );
}

function Perfil() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Mi Perfil</h1>
      <p className="text-slate-500">Aquí se podrá gestionar el perfil del usuario.</p>
    </div>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route path="/" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      
      <Route path="/ventas" element={
        <ProtectedRoute>
          <Ventas />
        </ProtectedRoute>
      } />
      
      <Route path="/ventas/nueva" element={
        <ProtectedRoute>
          <NewSale />
        </ProtectedRoute>
      } />
      
      <Route path="/servicios" element={
        <ProtectedRoute>
          <Servicios />
        </ProtectedRoute>
      } />
      
      <Route path="/inventario" element={
        <ProtectedRoute>
          <Inventario />
        </ProtectedRoute>
      } />
      
      <Route path="/proveedores" element={
        <ProtectedRoute>
          <Proveedores />
        </ProtectedRoute>
      } />
      
      <Route path="/clientes" element={
        <ProtectedRoute>
          <Clientes />
        </ProtectedRoute>
      } />
      
      <Route path="/empleados" element={
        <ProtectedRoute>
          <Empleados />
        </ProtectedRoute>
      } />
      
      <Route path="/prestamos" element={
        <ProtectedRoute>
          <Prestamos />
        </ProtectedRoute>
      } />
      
      <Route path="/auditorias" element={
        <ProtectedRoute>
          <Auditorias />
        </ProtectedRoute>
      } />
      
      <Route path="/historial" element={
        <ProtectedRoute>
          <Historial />
        </ProtectedRoute>
      } />
      
      <Route path="/perfil" element={
        <ProtectedRoute>
          <Perfil />
        </ProtectedRoute>
      } />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
