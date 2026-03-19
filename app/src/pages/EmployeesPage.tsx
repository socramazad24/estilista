import { useEffect, useState } from 'react';
import { employeesApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users } from 'lucide-react';

export default function EmployeesPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    employeesApi.employees.getAll().then((res) => setItems(getResults<any>(res.data)));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Empleados</h1>
        <p className="text-slate-500">Vista operativa conectada al endpoint de empleados.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((item) => (
          <Card key={item.id}>
            <CardHeader><CardTitle className="text-base">{item.full_name || item.name || `${item.first_name || ''} ${item.last_name || ''}`.trim() || `Empleado #${item.id}`}</CardTitle></CardHeader>
            <CardContent className="space-y-2 text-sm">
              {Object.entries(item).slice(0, 6).map(([k, v]) => (
                <div key={k} className="flex justify-between gap-4">
                  <span className="text-slate-500">{k}</span>
                  <span className="text-right">{String(v ?? '—')}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
        {items.length === 0 && (
          <div className="col-span-full text-center py-10 text-slate-500">
            <Users className="w-10 h-10 mx-auto mb-2 opacity-50" />
            No hay empleados
          </div>
        )}
      </div>
    </div>
  );
}
