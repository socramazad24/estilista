import { useEffect } from 'react';
import { useSales } from '@/hooks/useSales';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import {
  DollarSign,
  ShoppingCart,
  TrendingUp,
  Calendar,
  Scissors,
  Users,
  Package,
  ArrowRight,
} from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const { stats, todaySales, fetchStats, fetchTodaySales, isLoading } = useSales();

  useEffect(() => {
    fetchStats();
    fetchTodaySales();
  }, [fetchStats, fetchTodaySales]);

  const StatCard = ({ 
    title, 
    value, 
    subtitle, 
    icon: Icon, 
    trend,
    color = 'blue',
    isLoading 
  }: { 
    title: string; 
    value: string | number; 
    subtitle?: string;
    icon: React.ElementType; 
    trend?: string;
    color?: 'blue' | 'green' | 'purple' | 'orange';
    isLoading?: boolean;
  }) => {
    const colorClasses = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-emerald-50 text-emerald-600',
      purple: 'bg-purple-50 text-purple-600',
      orange: 'bg-orange-50 text-orange-600',
    };

    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <p className="text-sm font-medium text-slate-500">{title}</p>
              {isLoading ? (
                <Skeleton className="h-8 w-32" />
              ) : (
                <h3 className="text-2xl font-bold">{value}</h3>
              )}
              {subtitle && !isLoading && (
                <p className="text-sm text-slate-500">{subtitle}</p>
              )}
              {trend && !isLoading && (
                <div className="flex items-center gap-1 text-sm text-emerald-600">
                  <TrendingUp className="w-4 h-4" />
                  <span>{trend}</span>
                </div>
              )}
            </div>
            <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
              <Icon className="w-6 h-6" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-500">Resumen de la actividad del salón</p>
        </div>
        <div className="flex gap-2">
          <Button asChild variant="outline">
            <Link to="/ventas/nueva">
              <ShoppingCart className="w-4 h-4 mr-2" />
              Nueva Venta
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Ventas Hoy"
          value={formatCurrency(todaySales?.total_amount || 0)}
          subtitle={`${todaySales?.count || 0} transacciones`}
          icon={DollarSign}
          color="green"
          isLoading={isLoading}
        />
        <StatCard
          title="Ventas Semana"
          value={formatCurrency(stats?.week.total || 0)}
          icon={Calendar}
          color="blue"
          isLoading={isLoading}
        />
        <StatCard
          title="Ventas Mes"
          value={formatCurrency(stats?.month.total || 0)}
          icon={TrendingUp}
          color="purple"
          isLoading={isLoading}
        />
        <StatCard
          title="Servicios Hoy"
          value={todaySales?.count || 0}
          subtitle="servicios realizados"
          icon={Scissors}
          color="orange"
          isLoading={isLoading}
        />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Services */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Servicios Más Cotizados</CardTitle>
            <CardDescription>Top servicios del mes</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map(i => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : stats?.top_services && stats.top_services.length > 0 ? (
              <div className="space-y-4">
                {stats.top_services.map((service, index) => (
                  <div key={index} className="flex items-center gap-4">
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-sm font-medium text-blue-600">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium">{service.name}</span>
                        <Badge variant="secondary">{service.count} ventas</Badge>
                      </div>
                      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-blue-500 rounded-full transition-all"
                          style={{
                            width: `${(service.count / (stats.top_services[0]?.count || 1)) * 100}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500">
                <Scissors className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>No hay datos de servicios disponibles</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Accesos Rápidos</CardTitle>
            <CardDescription>Acciones frecuentes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Button asChild variant="outline" className="w-full justify-between">
                <Link to="/ventas/nueva">
                  <span className="flex items-center gap-2">
                    <ShoppingCart className="w-4 h-4" />
                    Nueva Venta
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full justify-between">
                <Link to="/clientes/nuevo">
                  <span className="flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    Nuevo Cliente
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full justify-between">
                <Link to="/inventario/movimiento">
                  <span className="flex items-center gap-2">
                    <Package className="w-4 h-4" />
                    Movimiento Inventario
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" className="w-full justify-between">
                <Link to="/ventas">
                  <span className="flex items-center gap-2">
                    <DollarSign className="w-4 h-4" />
                    Ver Ventas
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Sales */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Ventas Recientes</CardTitle>
            <CardDescription>Últimas transacciones del día</CardDescription>
          </div>
          <Button asChild variant="outline" size="sm">
            <Link to="/ventas">Ver todas</Link>
          </Button>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <Skeleton key={i} className="h-14 w-full" />
              ))}
            </div>
          ) : todaySales?.sales && todaySales.sales.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-slate-500">Factura</th>
                    <th className="text-left py-3 px-4 font-medium text-slate-500">Cliente</th>
                    <th className="text-left py-3 px-4 font-medium text-slate-500">Servicios</th>
                    <th className="text-right py-3 px-4 font-medium text-slate-500">Total</th>
                    <th className="text-center py-3 px-4 font-medium text-slate-500">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {todaySales.sales.slice(0, 5).map((sale) => (
                    <tr key={sale.id} className="border-b hover:bg-slate-50">
                      <td className="py-3 px-4 font-medium">{sale.invoice_number}</td>
                      <td className="py-3 px-4">{sale.client_name}</td>
                      <td className="py-3 px-4">{sale.items?.length || 0} servicios</td>
                      <td className="py-3 px-4 text-right font-medium">
                        {formatCurrency(sale.total)}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant={sale.status === 'completed' ? 'default' : 'secondary'}>
                          {sale.status_display}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500">
              <ShoppingCart className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No hay ventas hoy</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
