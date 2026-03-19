import { useEffect, useState } from 'react';
import { auditsApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { formatDateTime } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Shield } from 'lucide-react';

export default function AuditsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    Promise.all([
      auditsApi.logs.getAll(),
      auditsApi.logs.summary(),
    ]).then(([logsRes, summaryRes]) => {
      setLogs(getResults<any>(logsRes.data));
      setSummary(summaryRes.data);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Auditorías</h1>
        <p className="text-slate-500">Seguimiento de acciones del sistema.</p>
      </div>

      {summary && (
        <div className="grid md:grid-cols-3 gap-4">
          {Object.entries(summary).slice(0, 3).map(([key, value]) => (
            <Card key={key}>
              <CardContent className="p-5">
                <p className="text-sm text-slate-500">{key}</p>
                <p className="text-2xl font-bold">{String(value)}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Registros</CardTitle>
          <CardDescription>Últimas acciones capturadas</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {logs.map((log) => (
            <div key={log.id} className="rounded-lg border p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="font-medium">{log.action || log.description || 'Evento'}</p>
                  <p className="text-sm text-slate-500">{log.user_name || log.user || 'Sistema'}</p>
                </div>
                <p className="text-sm text-slate-500">{log.created_at ? formatDateTime(log.created_at) : '—'}</p>
              </div>
            </div>
          ))}
          {logs.length === 0 && (
            <div className="text-center py-10 text-slate-500">
              <Shield className="w-10 h-10 mx-auto mb-2 opacity-50" />
              No hay auditorías
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

