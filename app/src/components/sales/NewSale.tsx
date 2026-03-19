import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useServices, useClients } from '@/hooks/useSales';
import { usersApi, salesApi } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { 
  Plus, 
  Minus, 
  Trash2, 
  Search, 
  UserPlus, 
  ShoppingCart, 
  Check,
  Printer,
  X,
  Scissors,
  Clock,
} from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import type { Service, Client, Sale } from '@/types';

interface CartItem {
  id: number;
  service: number;
  service_detail: Service;
  quantity: number;
  unit_price: number;
  discount: number;
  total: number;
  notes?: string;
}

export default function NewSale() {
  const navigate = useNavigate();
  const { servicesByCategory, fetchServicesByCategory } = useServices();
  const { clients, searchClients, createClient } = useClients();
  
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [selectedStylist, setSelectedStylist] = useState<string>('');
  const [paymentMethod, setPaymentMethod] = useState<string>('cash');
  const [searchQuery, setSearchQuery] = useState('');
  const [clientSearchQuery, setClientSearchQuery] = useState('');
  const [showNewClientDialog, setShowNewClientDialog] = useState(false);
  const [showInvoiceDialog, setShowInvoiceDialog] = useState(false);
  const [completedSale, setCompletedSale] = useState<Sale | null>(null);
  const [stylists, setStylists] = useState<Array<{ id: number; first_name: string; last_name: string }>>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  // New client form
  const [newClient, setNewClient] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    email: '',
  });

  useEffect(() => {
    fetchServicesByCategory();
    fetchStylists();
  }, [fetchServicesByCategory]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (clientSearchQuery.length >= 2) {
        searchClients(clientSearchQuery);
      }
    }, 300);
    return () => clearTimeout(timeout);
  }, [clientSearchQuery, searchClients]);

  const fetchStylists = async () => {
    try {
      const response = await usersApi.getStylists();
      setStylists(response.data);
      if (response.data.length > 0) {
        setSelectedStylist(response.data[0].id.toString());
      }
    } catch (error) {
      console.error('Error fetching stylists:', error);
    }
  };

  const addToCart = (service: Service) => {
    const existingItem = cart.find(item => item.service === service.id);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.service === service.id 
          ? { ...item, quantity: item.quantity + 1, total: (item.quantity + 1) * item.unit_price }
          : item
      ));
    } else {
      const newItem: CartItem = {
        id: Date.now(),
        service: service.id,
        service_detail: service,
        quantity: 1,
        unit_price: Number(service.price) || 0,
        discount: 0,
        total: Number(service.price) || 0,
        notes: '',
      };
      setCart([...cart, newItem]);
    }
    toast.success(`${service.name} agregado al carrito`);
  };

  const removeFromCart = (serviceId: number) => {
    setCart(cart.filter(item => item.service !== serviceId));
  };

  const updateQuantity = (serviceId: number, delta: number) => {
    setCart(cart.map(item => {
      if (item.service === serviceId) {
        const newQuantity = Math.max(1, item.quantity + delta);
        return { ...item, quantity: newQuantity, total: newQuantity * (Number(item.unit_price) || 0) };
      }
      return item;
    }));
  };

  const handleCreateClient = async () => {
    try {
      const client = await createClient(newClient);
      setSelectedClient(client);
      setShowNewClientDialog(false);
      setNewClient({ first_name: '', last_name: '', phone: '', email: '' });
      toast.success('Cliente creado exitosamente');
    } catch (error) {
      toast.error('Error al crear el cliente');
    }
  };

  const handleCompleteSale = async () => {
    if (!selectedClient) {
      toast.error('Selecciona un cliente');
      return;
    }
    if (cart.length === 0) {
      toast.error('Agrega al menos un servicio');
      return;
    }
    if (!selectedStylist) {
      toast.error('Selecciona un estilista');
      return;
    }

    setIsProcessing(true);

    try {
      const saleData = {
        client: selectedClient.id,
        stylist: parseInt(selectedStylist),
        subtotal: cart.reduce((sum, item) => sum + (Number(item.total) || 0), 0),
        discount: 0,
        tax: 0,
        total: cart.reduce((sum, item) => sum + (Number(item.total) || 0), 0),
        payment_method: paymentMethod,
        notes: '',
        items: cart.map(item => ({
          service: item.service,
          quantity: item.quantity,
          unit_price: item.unit_price,
          discount: item.discount,
          notes: item.notes,
        })),
      };

      const response = await salesApi.create(saleData);

      console.log("SALE RESPONSE:", response.data);

      const saleResponse = response.data;

      // Buscar estilista
      const stylist = stylists.find(
        s => s.id === parseInt(selectedStylist)
      );

      // Construir venta completa para la factura
      const formattedSale = {
        ...saleResponse,

        // 🔥 Fecha segura
        date: saleResponse.date || new Date().toISOString(),

        // 🔥 Nombres seguros
        client_name: saleResponse.client_name || selectedClient?.full_name || "—",

        stylist_name: saleResponse.stylist_name || (
          stylist ? `${stylist.first_name} ${stylist.last_name}` : "—"
        ),

        cashier_name: saleResponse.cashier_name || "Admin",

        // 🔥 Items corregidos
        items: (saleResponse.items || cart).map((item: any, index: number) => ({
          id: item.id || index,

          service_name:
            item.service_name ||
            item.service_detail?.name ||
            cart[index]?.service_detail?.name ||
            "Servicio",

          quantity: Number(item.quantity) || 1,

          unit_price: Number(item.unit_price) || 0,

          total:
            Number(item.total) ||
            (Number(item.unit_price) || 0) * (Number(item.quantity) || 1),
        })),

        // 🔥 Totales seguros
        subtotal:
          Number(saleResponse.subtotal) ||
          cart.reduce((sum, item) => sum + item.total, 0),

        total:
          Number(saleResponse.total) ||
          cart.reduce((sum, item) => sum + item.total, 0),
      };

      setCompletedSale(formattedSale);
      setShowInvoiceDialog(true);
      toast.success('Venta completada exitosamente');
    } catch (error) {
      toast.error('Error al completar la venta');
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePrintInvoice = () => {
    window.print();
  };

  const handleCloseInvoice = () => {
    setShowInvoiceDialog(false);
    setCart([]);
    setSelectedClient(null);
    navigate('/ventas');
  };

const cartTotal = cart.reduce(
  (sum, item) => sum + (Number(item.total) || 0),
  0
);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Nueva Venta</h1>
          <p className="text-slate-500">Registra una nueva venta de servicios</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/ventas')}>
          <X className="w-4 h-4 mr-2" />
          Cancelar
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Services Selection */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Scissors className="w-5 h-5" />
                Seleccionar Servicios
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <Input
                  placeholder="Buscar servicios..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>

              <Tabs defaultValue={servicesByCategory[0]?.category.id.toString()}>
                <TabsList className="flex flex-wrap h-auto gap-1">
                  {servicesByCategory.map(category => (
                    <TabsTrigger 
                      key={category.category.id} 
                      value={category.category.id.toString()}
                      className="text-xs"
                    >
                      {category.category.name}
                    </TabsTrigger>
                  ))}
                </TabsList>

                {servicesByCategory.map(category => (
                  <TabsContent key={category.category.id} value={category.category.id.toString()}>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {category.services
                        .filter(service => 
                          service.name.toLowerCase().includes(searchQuery.toLowerCase())
                        )
                        .map(service => (
                        <button
                          key={service.id}
                          onClick={() => addToCart(service)}
                          className="flex items-center justify-between p-3 border rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors text-left"
                        >
                          <div>
                            <p className="font-medium">{service.name}</p>
                            <div className="flex items-center gap-2 text-sm text-slate-500">
                              <Clock className="w-3 h-3" />
                              {service.duration_short}
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="font-bold text-blue-600">{formatCurrency(service.price)}</p>
                            <Plus className="w-4 h-4 ml-auto text-blue-500" />
                          </div>
                        </button>
                      ))}
                    </div>
                  </TabsContent>
                ))}
              </Tabs>
            </CardContent>
          </Card>
        </div>

        {/* Cart and Checkout */}
        <div className="space-y-4">
          {/* Client Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UserPlus className="w-5 h-5" />
                Cliente
              </CardTitle>
            </CardHeader>
            <CardContent>
              {selectedClient ? (
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div>
                    <p className="font-medium">{selectedClient.full_name}</p>
                    <p className="text-sm text-slate-500">{selectedClient.phone}</p>
                  </div>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={() => setSelectedClient(null)}
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="Buscar cliente..."
                      value={clientSearchQuery}
                      onChange={(e) => setClientSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  
                  {clients.length > 0 && (
                    <ScrollArea className="h-32 border rounded-lg">
                      {clients.map(client => (
                        <button
                          key={client.id}
                          onClick={() => {
                            setSelectedClient(client);
                            setClientSearchQuery('');
                          }}
                          className="w-full px-3 py-2 text-left hover:bg-slate-50 border-b last:border-b-0"
                        >
                          <p className="font-medium">{client.full_name}</p>
                          <p className="text-sm text-slate-500">{client.phone}</p>
                        </button>
                      ))}
                    </ScrollArea>
                  )}
                  
                  <Button 
                    variant="outline" 
                    className="w-full"
                    onClick={() => setShowNewClientDialog(true)}
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Nuevo Cliente
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Stylist Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Scissors className="w-5 h-5" />
                Estilista
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={selectedStylist} onValueChange={setSelectedStylist}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccionar estilista" />
                </SelectTrigger>
                <SelectContent>
                  {stylists.map(stylist => (
                    <SelectItem key={stylist.id} value={stylist.id.toString()}>
                      {stylist.first_name} {stylist.last_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          {/* Cart */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="w-5 h-5" />
                Carrito
                <Badge variant="secondary" className="ml-auto">
                  {cart.length} items
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {cart.length === 0 ? (
                <div className="text-center py-6 text-slate-500">
                  <ShoppingCart className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>El carrito está vacío</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {cart.map(item => (
                    <div key={item.service} className="flex items-center gap-3 p-2 bg-slate-50 rounded-lg">
                      <div className="flex-1">
                        <p className="font-medium text-sm">{item.service_detail.name}</p>
                        <p className="text-sm text-slate-500">{formatCurrency(item.unit_price)}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-7 w-7"
                          onClick={() => updateQuantity(item.service, -1)}
                        >
                          <Minus className="w-3 h-3" />
                        </Button>
                        <span className="w-6 text-center">{item.quantity}</span>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-7 w-7"
                          onClick={() => updateQuantity(item.service, 1)}
                        >
                          <Plus className="w-3 h-3" />
                        </Button>
                      </div>
                      <div className="text-right min-w-[80px]">
                        <p className="font-medium">{formatCurrency(item.total)}</p>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-7 w-7 text-red-500"
                        onClick={() => removeFromCart(item.service)}
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
            <CardFooter className="flex-col gap-4">
              <Separator />
              <div className="flex items-center justify-between w-full">
                <span className="text-lg font-medium">Total</span>
                <span className="text-2xl font-bold text-blue-600">{formatCurrency(cartTotal)}</span>
              </div>
              
              <Select value={paymentMethod} onValueChange={setPaymentMethod}>
                <SelectTrigger>
                  <SelectValue placeholder="Método de pago" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cash">Efectivo</SelectItem>
                  <SelectItem value="card">Tarjeta</SelectItem>
                  <SelectItem value="transfer">Transferencia</SelectItem>
                  <SelectItem value="nequi">Nequi</SelectItem>
                  <SelectItem value="daviplata">Daviplata</SelectItem>
                </SelectContent>
              </Select>
              
              <Button 
                className="w-full bg-blue-600 hover:bg-blue-700"
                disabled={cart.length === 0 || !selectedClient || isProcessing}
                onClick={handleCompleteSale}
              >
                {isProcessing ? (
                  <>Procesando...</>
                ) : (
                  <>
                    <Check className="w-4 h-4 mr-2" />
                    Completar Venta
                  </>
                )}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>

      {/* New Client Dialog */}
      <Dialog open={showNewClientDialog} onOpenChange={setShowNewClientDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Nuevo Cliente</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Nombre</Label>
                <Input 
                  value={newClient.first_name}
                  onChange={(e) => setNewClient({...newClient, first_name: e.target.value})}
                />
              </div>
              <div className="space-y-2">
                <Label>Apellido</Label>
                <Input 
                  value={newClient.last_name}
                  onChange={(e) => setNewClient({...newClient, last_name: e.target.value})}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label>Teléfono</Label>
              <Input 
                value={newClient.phone}
                onChange={(e) => setNewClient({...newClient, phone: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <Label>Email (opcional)</Label>
              <Input 
                type="email"
                value={newClient.email}
                onChange={(e) => setNewClient({...newClient, email: e.target.value})}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowNewClientDialog(false)}>
              Cancelar
            </Button>
            <Button onClick={handleCreateClient} className="bg-blue-600 hover:bg-blue-700">
              Crear Cliente
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Invoice Dialog */}
      <Dialog open={showInvoiceDialog} onOpenChange={setShowInvoiceDialog}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-500" />
              Venta Completada
            </DialogTitle>
          </DialogHeader>
          
          {completedSale && (
            <div className="print-only">
              <div className="text-center mb-6">
                <h2 className="text-xl font-bold">ESTILERA</h2>
                <p className="text-slate-500">Factura de Venta</p>
                <p className="text-lg font-mono mt-2">{completedSale.invoice_number as string}</p>
              </div>
              
              <div className="space-y-2 text-sm mb-4">
                <div className="flex justify-between">
                  <span className="text-slate-500">Fecha:</span>
                  <span>
                    {completedSale.date
                      ? new Date(completedSale.date as string).toLocaleString()
                      : "—"}
                  </span>                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Cliente:</span>
                  <span>{completedSale.client_name as string}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Estilista:</span>
                  <span>{completedSale.stylist_name as string}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Cajero:</span>
                  <span>{completedSale.cashier_name as string}</span>
                </div>
              </div>
              
              <Separator className="my-4" />
              
              <table className="w-full text-sm mb-4">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2">Servicio</th>
                    <th className="text-center py-2">Cant</th>
                    <th className="text-right py-2">Precio</th>
                    <th className="text-right py-2">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {(completedSale.items as Array<{ id: number; service_name: string; quantity: number; unit_price: number; total: number }>).map((item) => (
                    <tr key={item.id}>
                      <td className="py-2">{item.service_name}</td>
                      <td className="text-center py-2">{item.quantity}</td>
                      <td className="text-right py-2">{formatCurrency(item.unit_price)}</td>
                      <td className="text-right py-2">
                        {formatCurrency(Number(item.total) || 0)}
                      </td>                    </tr>
                  ))}
                </tbody>
              </table>
              
              <Separator className="my-4" />
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subtotal:</span>
                  <span>{formatCurrency(completedSale.subtotal as number)}</span>
                </div>
                <div className="flex justify-between text-lg font-bold">
                  <span>TOTAL:</span>
                  <span className="text-blue-600">{formatCurrency(completedSale.total as number)}</span>
                </div>
                <div className="flex justify-between text-sm text-slate-500">
                  <span>Método de pago:</span>
                  <span>{completedSale.payment_method_display as string}</span>
                </div>
              </div>
              
              <div className="text-center mt-6 text-sm text-slate-500">
                <p>¡Gracias por su preferencia!</p>
              </div>
            </div>
          )}
          
          <DialogFooter className="no-print">
            <Button variant="outline" onClick={handleCloseInvoice}>
              Cerrar
            </Button>
            <Button onClick={handlePrintInvoice} className="bg-blue-600 hover:bg-blue-700">
              <Printer className="w-4 h-4 mr-2" />
              Imprimir Factura
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
