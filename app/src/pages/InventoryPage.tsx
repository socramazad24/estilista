import { useEffect, useState } from 'react';
import { inventoryApi, providersApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { formatCurrency } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Package, Plus, ArrowUpDown, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';

const emptyProduct = {
  category: '',
  provider: '',
  name: '',
  description: '',
  unit: 'unit',
  stock: '0',
  minstock: '5',
  purchaseprice: '0',
  saleprice: '0',
  location: '',
  isactive: true,
};

export default function InventoryPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [providers, setProviders] = useState<any[]>([]);
  const [lowStock, setLowStock] = useState<any[]>([]);
  const [openProduct, setOpenProduct] = useState(false);
  const [openMovement, setOpenMovement] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [productForm, setProductForm] = useState<any>(emptyProduct);
  const [movementForm, setMovementForm] = useState({
    product: '',
    movementtype: 'entry',
    quantity: '1',
    unitprice: '0',
    reference: '',
    notes: '',
  });

  const load = async () => {
    const [productsRes, categoriesRes, providersRes, lowStockRes] = await Promise.all([
      inventoryApi.products.getAll(),
      inventoryApi.categories.getAll(),
      providersApi.providers.getAll(),
      inventoryApi.lowStock(),
    ]);
    setProducts(getResults<any>(productsRes.data));
    setCategories(getResults<any>(categoriesRes.data));
    setProviders(getResults<any>(providersRes.data));
    setLowStock(getResults<any>(lowStockRes.data));
  };

  useEffect(() => { load(); }, []);

  const saveProduct = async () => {
    try {
      await inventoryApi.products.create({
        ...productForm,
        category: Number(productForm.category),
        provider: productForm.provider ? Number(productForm.provider) : null,
        stock: Number(productForm.stock),
        minstock: Number(productForm.minstock),
        purchaseprice: Number(productForm.purchaseprice),
        saleprice: Number(productForm.saleprice),
      });
      toast.success('Producto creado');
      setOpenProduct(false);
      setProductForm(emptyProduct);
      load();
    } catch {
      toast.error('No se pudo crear el producto');
    }
  };

  const saveMovement = async () => {
    try {
      await inventoryApi.movements.create({
        ...movementForm,
        product: Number(movementForm.product),
        quantity: Number(movementForm.quantity),
        unitprice: Number(movementForm.unitprice),
      });
      toast.success('Movimiento registrado');
      setOpenMovement(false);
      setMovementForm({
        product: '',
        movementtype: 'entry',
        quantity: '1',
        unitprice: '0',
        reference: '',
        notes: '',
      });
      load();
    } catch {
      toast.error('No se pudo registrar el movimiento');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col lg:flex-row gap-4 lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-bold">Inventario</h1>
          <p className="text-slate-500">Control de productos y movimientos.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setOpenMovement(true)}>
            <ArrowUpDown className="w-4 h-4 mr-2" />Movimiento
          </Button>
          <Button onClick={() => setOpenProduct(true)} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />Producto
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <Card><CardContent className="p-5"><p className="text-sm text-slate-500">Productos</p><p className="text-2xl font-bold">{products.length}</p></CardContent></Card>
        <Card><CardContent className="p-5"><p className="text-sm text-slate-500">Stock bajo</p><p className="text-2xl font-bold text-orange-600">{lowStock.length}</p></CardContent></Card>
        <Card><CardContent className="p-5"><p className="text-sm text-slate-500">Activos</p><p className="text-2xl font-bold">{products.filter(p => p.isactive).length}</p></CardContent></Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Productos</CardTitle>
          <CardDescription>Vista rápida del inventario</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {products.map((p) => (
            <Card key={p.id}>
              <CardContent className="p-5 space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold">{p.name}</h3>
                    <p className="text-sm text-slate-500">{p.sku || 'Sin SKU'}</p>
                  </div>
                  {p.islowstock ? (
                    <Badge variant="destructive">Stock bajo</Badge>
                  ) : (
                    <Badge variant="secondary">Normal</Badge>
                  )}
                </div>
                <div className="text-sm text-slate-600">{p.categoryname || 'Sin categoría'}</div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>Stock: <span className="font-medium">{p.stock}</span></div>
                  <div>Mínimo: <span className="font-medium">{p.minstock}</span></div>
                  <div>Compra: <span className="font-medium">{formatCurrency(Number(p.purchaseprice || 0))}</span></div>
                  <div>Venta: <span className="font-medium">{formatCurrency(Number(p.saleprice || 0))}</span></div>
                </div>
                <Button variant="outline" className="w-full" onClick={() => {
                  setSelectedProduct(p);
                  setMovementForm({ ...movementForm, product: String(p.id), unitprice: String(p.purchaseprice || 0) });
                  setOpenMovement(true);
                }}>
                  Registrar movimiento
                </Button>
              </CardContent>
            </Card>
          ))}
          {products.length === 0 && (
            <div className="col-span-full text-center py-10 text-slate-500">
              <Package className="w-10 h-10 mx-auto mb-2 opacity-50" />
              No hay productos
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Alertas</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          {lowStock.length === 0 ? (
            <p className="text-slate-500">No hay productos con stock bajo.</p>
          ) : lowStock.map((p) => (
            <div key={p.id} className="flex items-center justify-between rounded-lg border p-3">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-4 h-4 text-orange-500" />
                <div>
                  <p className="font-medium">{p.name}</p>
                  <p className="text-sm text-slate-500">Stock actual: {p.stock} / mínimo: {p.minstock}</p>
                </div>
              </div>
              <Badge variant="destructive">Reabastecer</Badge>
            </div>
          ))}
        </CardContent>
      </Card>

      <Dialog open={openProduct} onOpenChange={setOpenProduct}>
        <DialogContent className="max-w-2xl">
          <DialogHeader><DialogTitle>Nuevo producto</DialogTitle></DialogHeader>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Categoría</Label>
              <Select value={productForm.category} onValueChange={(v) => setProductForm({ ...productForm, category: v })}>
                <SelectTrigger><SelectValue placeholder="Selecciona categoría" /></SelectTrigger>
                <SelectContent>{categories.map((c) => <SelectItem key={c.id} value={String(c.id)}>{c.name}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Proveedor</Label>
              <Select value={productForm.provider} onValueChange={(v) => setProductForm({ ...productForm, provider: v })}>
                <SelectTrigger><SelectValue placeholder="Opcional" /></SelectTrigger>
                <SelectContent>{providers.map((p) => <SelectItem key={p.id} value={String(p.id)}>{p.name}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2"><Label>Nombre</Label><Input value={productForm.name} onChange={(e) => setProductForm({ ...productForm, name: e.target.value })} /></div>
            <div className="space-y-2"><Label>Unidad</Label><Input value={productForm.unit} onChange={(e) => setProductForm({ ...productForm, unit: e.target.value })} /></div>
            <div className="space-y-2"><Label>Stock inicial</Label><Input type="number" value={productForm.stock} onChange={(e) => setProductForm({ ...productForm, stock: e.target.value })} /></div>
            <div className="space-y-2"><Label>Stock mínimo</Label><Input type="number" value={productForm.minstock} onChange={(e) => setProductForm({ ...productForm, minstock: e.target.value })} /></div>
            <div className="space-y-2"><Label>Precio compra</Label><Input type="number" value={productForm.purchaseprice} onChange={(e) => setProductForm({ ...productForm, purchaseprice: e.target.value })} /></div>
            <div className="space-y-2"><Label>Precio venta</Label><Input type="number" value={productForm.saleprice} onChange={(e) => setProductForm({ ...productForm, saleprice: e.target.value })} /></div>
            <div className="space-y-2 md:col-span-2"><Label>Ubicación</Label><Input value={productForm.location} onChange={(e) => setProductForm({ ...productForm, location: e.target.value })} /></div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpenProduct(false)}>Cancelar</Button>
            <Button onClick={saveProduct}>Guardar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={openMovement} onOpenChange={setOpenMovement}>
        <DialogContent>
          <DialogHeader><DialogTitle>Movimiento de inventario</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Producto</Label>
              <Select value={movementForm.product} onValueChange={(v) => setMovementForm({ ...movementForm, product: v })}>
                <SelectTrigger><SelectValue placeholder="Selecciona producto" /></SelectTrigger>
                <SelectContent>{products.map((p) => <SelectItem key={p.id} value={String(p.id)}>{p.name}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Tipo</Label>
              <Select value={movementForm.movementtype} onValueChange={(v) => setMovementForm({ ...movementForm, movementtype: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="entry">Entrada</SelectItem>
                  <SelectItem value="exit">Salida</SelectItem>
                  <SelectItem value="adjustment">Ajuste</SelectItem>
                  <SelectItem value="return">Devolución</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2"><Label>Cantidad</Label><Input type="number" value={movementForm.quantity} onChange={(e) => setMovementForm({ ...movementForm, quantity: e.target.value })} /></div>
              <div className="space-y-2"><Label>Precio unitario</Label><Input type="number" value={movementForm.unitprice} onChange={(e) => setMovementForm({ ...movementForm, unitprice: e.target.value })} /></div>
            </div>
            <div className="space-y-2"><Label>Referencia</Label><Input value={movementForm.reference} onChange={(e) => setMovementForm({ ...movementForm, reference: e.target.value })} /></div>
            <div className="space-y-2"><Label>Notas</Label><Input value={movementForm.notes} onChange={(e) => setMovementForm({ ...movementForm, notes: e.target.value })} /></div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpenMovement(false)}>Cancelar</Button>
            <Button onClick={saveMovement}>Registrar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
