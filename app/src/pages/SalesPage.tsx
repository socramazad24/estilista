import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { salesApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { formatCurrency, formatDateTime } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Plus, Receipt } from 'lucide-react';

export default function SalesPage() {
  const [sales, setSales] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await salesApi.getAll(search ? { search } : undefined);
      setSales(getResults<any>(res.data));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);
  useEffect(() => {
    const t = setTimeout(load, 350);
    return () => clearTimeout(t);
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold">Historial de Ventas</h1>
          <p className="text-slate-500">Consulta ventas, estados y totales.</p>
        </div>
        <Button asChild className="bg-blue-600 hover:bg-blue-700">
          <Link to="/ventas/nueva"><Plus className="w-4 h-4 mr-2" />Nueva venta</Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Ventas registradas</CardTitle>
          <CardDescription>Búsqueda por factura o cliente</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input value={search} onChange={(e) => setSearch(e.target.value)} className="pl-10" placeholder="Buscar..." />
          </div>

          <div className="rounded-lg border overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left p-3">Factura</th>
                  <th className="text-left p-3">Cliente</th>
                  <th className="text-left p-3">Estilista</th>
                  <th className="text-left p-3">Fecha</th>
                  <th className="text-right p-3">Total</th>
                  <th className="text-center p-3">Estado</th>
                </tr>
              </thead>
              <tbody>
                {sales.map((sale) => (
                  <tr key={sale.id} className="border-t">
                    <td className="p-3 font-medium">{sale.invoice_number}</td>
                    <td className="p-3">{sale.client_name || sale.client_firstname || '—'}</td>
                    <td className="p-3">{sale.stylist_name || sale.stylist || '—'}</td>
                    <td className="p-3">{sale.date ? formatDateTime(sale.date) : '—'}</td>
                    <td className="p-3 text-right font-semibold">{formatCurrency(Number(sale.total || sale.total_amount || 0))}</td>
                    <td className="p-3 text-center">
                      <Badge variant={sale.status === 'completed' ? 'default' : 'secondary'}>
                        {sale.status_display || sale.status}
                      </Badge>
                    </td>
                  </tr>
                ))}
                {!loading && sales.length === 0 && (
                  <tr>
                    <td colSpan={6} className="p-10 text-center text-slate-500">
                      <Receipt className="w-10 h-10 mx-auto mb-2 opacity-50" />
                      No hay ventas para mostrar
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
