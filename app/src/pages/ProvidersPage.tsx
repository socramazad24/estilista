import { useEffect, useState } from 'react';
import { providersApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Plus, Truck } from 'lucide-react';
import { toast } from 'sonner';

const emptyForm = {
  name: '',
  contactname: '',
  phone: '',
  email: '',
  city: '',
  nit: '',
  address: '',
  website: '',
  notes: '',
  status: 'active',
};

export default function ProvidersPage() {
  const [items, setItems] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<any>(emptyForm);

  const load = async () => {
    const res = await providersApi.providers.getAll();
    setItems(getResults<any>(res.data));
  };

  useEffect(() => { load(); }, []);

  const save = async () => {
    try {
      await providersApi.providers.create(form);
      toast.success('Proveedor creado');
      setOpen(false);
      setForm(emptyForm);
      load();
    } catch {
      toast.error('No se pudo crear el proveedor');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Proveedores</h1>
          <p className="text-slate-500">Gestión de proveedores y datos de contacto.</p>
        </div>
        <Button onClick={() => setOpen(true)} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />Nuevo proveedor
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
          <CardDescription>{items.length} proveedores</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <Card key={item.id}>
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold">{item.name}</h3>
                    <p className="text-sm text-slate-500">{item.city || 'Sin ciudad'}</p>
                  </div>
                  <Badge variant={item.status === 'active' ? 'default' : 'secondary'}>
                    {item.status === 'active' ? 'Activo' : 'Inactivo'}
                  </Badge>
                </div>
                <div className="text-sm text-slate-600 space-y-1">
                  <p>Contacto: {item.contactname || '—'}</p>
                  <p>Teléfono: {item.phone || '—'}</p>
                  <p>Email: {item.email || '—'}</p>
                  <p>NIT: {item.nit || '—'}</p>
                </div>
              </CardContent>
            </Card>
          ))}
          {items.length === 0 && (
            <div className="col-span-full text-center py-10 text-slate-500">
              <Truck className="w-10 h-10 mx-auto mb-2 opacity-50" />
              No hay proveedores
            </div>
          )}
        </CardContent>
      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader><DialogTitle>Nuevo proveedor</DialogTitle></DialogHeader>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              ['name', 'Nombre'],
              ['contactname', 'Contacto'],
              ['phone', 'Teléfono'],
              ['email', 'Email'],
              ['city', 'Ciudad'],
              ['nit', 'NIT'],
              ['address', 'Dirección'],
              ['website', 'Sitio web'],
            ].map(([key, label]) => (
              <div className="space-y-2" key={key}>
                <Label>{label}</Label>
                <Input value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />
              </div>
            ))}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)}>Cancelar</Button>
            <Button onClick={save}>Guardar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
