import { useEffect, useState } from 'react';
import { authApi } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const [passwords, setPasswords] = useState({
    old_password: '',
    new_password: '',
  });

  useEffect(() => {
    authApi.getCurrentUser().then((res) => setUser(res.data));
  }, []);

  const changePassword = async () => {
    try {
      await authApi.changePassword(passwords);
      toast.success('Contraseña actualizada');
      setPasswords({ old_password: '', new_password: '' });
    } catch {
      toast.error('No se pudo actualizar la contraseña');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Mi Perfil</h1>
        <p className="text-slate-500">Información del usuario y seguridad.</p>
      </div>

      <Card>
        <CardHeader><CardTitle>Datos personales</CardTitle></CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-4 text-sm">
          <div><span className="text-slate-500">Usuario:</span> {user?.username || '—'}</div>
          <div><span className="text-slate-500">Rol:</span> {user?.role || '—'}</div>
          <div><span className="text-slate-500">Nombre:</span> {user ? `${user.first_name} ${user.last_name}` : '—'}</div>
          <div><span className="text-slate-500">Email:</span> {user?.email || '—'}</div>
          <div><span className="text-slate-500">Teléfono:</span> {user?.phone || '—'}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Cambiar contraseña</CardTitle></CardHeader>
        <CardContent className="space-y-4 max-w-xl">
          <div className="space-y-2">
            <Label>Contraseña actual</Label>
            <Input type="password" value={passwords.old_password} onChange={(e) => setPasswords({ ...passwords, old_password: e.target.value })} />
          </div>
          <div className="space-y-2">
            <Label>Nueva contraseña</Label>
            <Input type="password" value={passwords.new_password} onChange={(e) => setPasswords({ ...passwords, new_password: e.target.value })} />
          </div>
          <Button onClick={changePassword}>Actualizar</Button>
        </CardContent>
      </Card>
    </div>
  );
}
