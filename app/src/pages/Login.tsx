import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { Scissors, Lock, User } from 'lucide-react';
import axios from 'axios';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setError('');
      setIsLoading(true);

      try {
        await login({ username, password });
        navigate('/');
      } catch (err: unknown) {
        console.error('Error completo:', err); // Para debugging
        
        if (axios.isAxiosError(err)) {
          if (!err.response) {
            // Error de red (CORS, servidor caído, etc.)
            setError('No se puede conectar al servidor. Verifica que el backend esté ejecutándose en http://localhost:8000');
          } else if (err.response.status === 401) {
            setError('Usuario o contraseña incorrectos');
          } else if (err.response.status === 0) {
            setError('Error de CORS. Verifica la configuración del backend');
          } else {
            setError(err.response.data?.detail || `Error ${err.response.status}: ${err.response.statusText}`);
          }
        } else {
          setError('Error desconocido al iniciar sesión');
        }
      } finally {
        setIsLoading(false);
      }
    };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 to-blue-50 p-4">
      <div className="w-full max-w-md">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-blue-600 to-blue-800 shadow-lg mb-4">
            <Scissors className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-slate-800">Estilera</h1>
          <p className="text-slate-500 mt-1">Sistema de Gestión para Estilistas</p>
        </div>

        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl font-bold text-center">Iniciar Sesión</CardTitle>
            <CardDescription className="text-center">
              Ingresa tus credenciales para acceder al sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            {error && (
              <Alert variant="destructive" className="mb-4">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Usuario</Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input
                    id="username"
                    type="text"
                    placeholder="Ingresa tu usuario"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Contraseña</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="Ingresa tu contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Spinner className="mr-2 h-4 w-4" />
                    Iniciando sesión...
                  </>
                ) : (
                  'Iniciar Sesión'
                )}
              </Button>
            </form>

            <div className="mt-6 p-4 bg-slate-50 rounded-lg text-sm text-slate-600">
              <p className="font-medium mb-2">Credenciales de prueba:</p>
              <div className="space-y-1">
                <p><span className="font-mono bg-slate-200 px-1 rounded">admin</span> / <span className="font-mono bg-slate-200 px-1 rounded">Admin123!</span></p>
                <p><span className="font-mono bg-slate-200 px-1 rounded">maria.gomez</span> / <span className="font-mono bg-slate-200 px-1 rounded">Estilista123!</span></p>
                <p><span className="font-mono bg-slate-200 px-1 rounded">cajero1</span> / <span className="font-mono bg-slate-200 px-1 rounded">Cajero123!</span></p>
              </div>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-sm text-slate-500 mt-6">
          © 2024 Estilera. Todos los derechos reservados.
        </p>
      </div>
    </div>
  );
}
