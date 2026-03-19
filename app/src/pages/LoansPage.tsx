import { useEffect, useState } from 'react';
import { employeesApi } from '@/services/api';
import { getResults } from '@/lib/page-utils';
import { formatCurrency, formatDate } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { HandCoins } from 'lucide-react';
import { toast } from 'sonner';

export default function LoansPage() {
  const [items, setItems] = useState<any[]>([]);
  const [selected, setSelected] = useState<any | null>(null);
  const [amount, setAmount] = useState('');

  const load = async () => {
    const res = await employeesApi.loans.getAll();
    setItems(getResults<any>(res.data));
  };

  useEffect(() => { load(); }, []);

  const registerPayment = async () => {
    if (!selected) return;
    try {
      await employeesApi.loans.registerPayment(selected.id, { amount: Number(amount) });
      toast.success('Pago registrado');
      setSelected(null);
      setAmount('');
      load();
    } catch {
      toast.error('No se pudo registrar el pago');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Préstamos</h1>
        <p className="text-slate-500">Seguimiento de préstamos y pagos.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((loan) => (
          <Card key={loan.id}>
            <CardHeader>
              <CardTitle className="text-base">{loan.employee_name || loan.employee || `Préstamo #${loan.id}`}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>Monto: <span className="font-semibold">{formatCurrency(Number(loan.amount || loan.total_amount || 0))}</span></p>
              <p>Saldo: <span className="font-semibold">{formatCurrency(Number(loan.balance || loan.pending_amount || 0))}</span></p>
              <p>Fecha: {loan.date ? formatDate(loan.date) : '—'}</p>
              <Button className="w-full" onClick={() => setSelected(loan)}>Registrar pago</Button>
            </CardContent>
          </Card>
        ))}
        {items.length === 0 && (
          <div className="col-span-full text-center py-10 text-slate-500">
            <HandCoins className="w-10 h-10 mx-auto mb-2 opacity-50" />
            No hay préstamos
          </div>
        )}
      </div>

      <Dialog open={!!selected} onOpenChange={(v) => !v && setSelected(null)}>
        <DialogContent>
          <DialogHeader><DialogTitle>Registrar pago</DialogTitle></DialogHeader>
          <div className="space-y-2">
            <Label>Monto pagado</Label>
            <Input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setSelected(null)}>Cancelar</Button>
            <Button onClick={registerPayment}>Guardar pago</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
