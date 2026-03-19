import { useEffect, useState } from 'react';
import { servicesApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { formatCurrency } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Plus, Scissors, Pencil, Trash2 } from 'lucide-react';
import { toast } from 'sonner';

const emptyForm = {
  category: '',
  name: '',
  description: '',
  price: '',
  durationminutes: '60',
  isactive: true,
};

export default function ServicesPage() {
  const [items, setItems] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<any | null>(null);
  const [form, setForm] = useState<any>(emptyForm);

  const load = async () => {
    const [servicesRes, categoriesRes] = await Promise.all([
      servicesApi.getAll(),
      servicesApi.getCategories(),
    ]);
    setItems(getResults<any>(servicesRes.data));
    setCategories(getResults<any>(categoriesRes.data));
  };

  useEffect(() => { load(); }, []);

  const save = async () => {
    const payload = {
      ...form,
      category: Number(form.category),
      price: Number(form.price),
      durationminutes: Number(form.durationminutes),
      isactive: Boolean(form.isactive),
    };

    try {
      if (editing) await servicesApi.update(editing.id, payload);
      else await servicesApi.create(payload);
      toast.success(editing ? 'Servicio actualizado' : 'Servicio creado');
      setOpen(false);
      setEditing(null);
      setForm(emptyForm);
      load();
    } catch {
      toast.error('No se pudo guardar el servicio');
    }
  };

  const remove = async (id: number) => {
    try {
      await servicesApi.remove(id);
      toast.success('Servicio eliminado');
      load();
    } catch {
      toast.error('No se pudo eliminar');
    }
  };

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setOpen(true);
  };

  const openEdit = (item: any) => {
    setEditing(item);
    setForm({
      category: String(item.category ?? ''),
      name: item.name ?? '',
      description: item.description ?? '',
      price: String(item.price ?? ''),
      durationminutes: String(item.durationminutes ?? 60),
      isactive: Boolean(item.isactive),
    });
    setOpen(true);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Servicios</h1>
          <p className="text-slate-500">Administra servicios, precio y duración.</p>
        </div>
        <Button onClick={openCreate} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />Nuevo servicio
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
          <CardDescription>{items.length} servicios cargados</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <Card key={item.id} className="border">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold">{item.name}</h3>
                    <p className="text-sm text-slate-500">{item.category_name || item.categoryname || 'Sin categoría'}</p>
                  </div>
                  <Badge variant={item.isactive ? 'default' : 'secondary'}>
                    {item.isactive ? 'Activo' : 'Inactivo'}
                  </Badge>
                </div>
                <div className="text-sm text-slate-600 truncate">{item.description || 'Sin descripción'}</div>
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-blue-600">{formatCurrency(Number(item.price || 0))}</span>
                  <span className="text-sm text-slate-500">{item.durationdisplay || item.durationshort || `${item.durationminutes} min`}</span>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" className="flex-1" onClick={() => openEdit(item)}>
                    <Pencil className="w-4 h-4 mr-2" />Editar
                  </Button>
                  <Button variant="destructive" className="flex-1" onClick={() => remove(item.id)}>
                    <Trash2 className="w-4 h-4 mr-2" />Eliminar
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
          {items.length === 0 && (
            <div className="col-span-full text-center py-10 text-slate-500">
              <Scissors className="w-10 h-10 mx-auto mb-2 opacity-50" />
              No hay servicios
            </div>
          )}
        </CardContent>
      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editing ? 'Editar servicio' : 'Nuevo servicio'}</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Categoría</Label>
              <Select value={form.category} onValueChange={(v) => setForm({ ...form, category: v })}>
                <SelectTrigger><SelectValue placeholder="Selecciona categoría" /></SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat.id} value={String(cat.id)}>{cat.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Nombre</Label>
              <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>

            <div className="space-y-2">
              <Label>Descripción</Label>
              <Input value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Precio</Label>
                <Input type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>Duración</Label>
                <Select value={form.durationminutes} onValueChange={(v) => setForm({ ...form, durationminutes: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {['15','30','45','60','90','120','150','180'].map((m) => (
                      <SelectItem key={m} value={m}>{m} min</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
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
