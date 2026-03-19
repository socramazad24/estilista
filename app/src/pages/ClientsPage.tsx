import { useEffect, useState } from 'react';
import { clientsApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Search, Plus, UserCircle2 } from 'lucide-react';
import { toast } from 'sonner';

const emptyForm = {
  first_name: '',
  last_name: '',
  phone: '',
  email: '',
  address: '',
  notes: '',
};

export default function ClientsPage() {
  const [items, setItems] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<any>(emptyForm);

  const load = async () => {
    const res = await clientsApi.getAll(search ? { search } : undefined);
    setItems(getResults<any>(res.data));
  };

  useEffect(() => { load(); }, []);
  useEffect(() => {
    const t = setTimeout(load, 350);
    return () => clearTimeout(t);
  }, [search]);

  const save = async () => {
    try {
      await clientsApi.create(form);
      toast.success('Cliente creado');
      setOpen(false);
      setForm(emptyForm);
      load();
    } catch {
      toast.error('No se pudo crear el cliente');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Clientes</h1>
          <p className="text-slate-500">Consulta y registro de clientes.</p>
        </div>
        <Button onClick={() => setOpen(true)} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />Nuevo cliente
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Base de clientes</CardTitle>
          <CardDescription>Búsqueda por nombre, teléfono o email</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input className="pl-10" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Buscar cliente..." />
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {items.map((item) => (
              <Card key={item.id}>
                <CardContent className="p-5 space-y-2">
                  <h3 className="font-semibold">{item.full_name || `${item.first_name} ${item.last_name}`}</h3>
                  <p className="text-sm text-slate-500">{item.phone || 'Sin teléfono'}</p>
                  <p className="text-sm text-slate-500">{item.email || 'Sin email'}</p>
                  <p className="text-sm text-slate-500">{item.address || 'Sin dirección'}</p>
                </CardContent>
              </Card>
            ))}
            {items.length === 0 && (
              <div className="col-span-full text-center py-10 text-slate-500">
                <UserCircle2 className="w-10 h-10 mx-auto mb-2 opacity-50" />
                No hay clientes
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader><DialogTitle>Nuevo cliente</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2"><Label>Nombres</Label><Input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} /></div>
              <div className="space-y-2"><Label>Apellidos</Label><Input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} /></div>
            </div>
            <div className="space-y-2"><Label>Teléfono</Label><Input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} /></div>
            <div className="space-y-2"><Label>Email</Label><Input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
            <div className="space-y-2"><Label>Dirección</Label><Input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} /></div>
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
