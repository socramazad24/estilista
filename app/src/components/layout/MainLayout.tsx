import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';
import { Badge } from '@/components/ui/badge';
import {
  Scissors,
  LayoutDashboard,
  ShoppingCart,
  Package,
  Users,
  UserCircle,
  Truck,
  History,
  Menu,
  LogOut,
  ChevronDown,
  DollarSign,
  Shield,
} from 'lucide-react';

interface NavItem {
  path: string;
  label: string;
  icon: React.ElementType;
  roles?: string[];
  badge?: number;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/ventas', label: 'Ventas', icon: ShoppingCart },
  { path: '/servicios', label: 'Servicios', icon: Scissors },
  { path: '/inventario', label: 'Inventario', icon: Package },
  { path: '/proveedores', label: 'Proveedores', icon: Truck },
  { path: '/clientes', label: 'Clientes', icon: UserCircle },
  { path: '/empleados', label: 'Empleados', icon: Users },
  { path: '/prestamos', label: 'Préstamos', icon: DollarSign },
  { path: '/auditorias', label: 'Auditorías', icon: Shield, roles: ['admin'] },
  { path: '/historial', label: 'Historial', icon: History },
];

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { user, logout, hasRole } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const getRoleDisplay = (role: string) => {
    const roles: Record<string, string> = {
      admin: 'Administrador',
      stylist: 'Estilista',
      cashier: 'Cajero',
      assistant: 'Asistente',
    };
    return roles[role] || role;
  };

  const filteredNavItems = navItems.filter(
    item => !item.roles || hasRole(item.roles)
  );

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-64 bg-slate-900 text-white fixed h-full">
        {/* Logo */}
        <div className="p-6 border-b border-slate-800">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
              <Scissors className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg leading-tight">Estilera</h1>
              <p className="text-xs text-slate-400">Sistema de Gestión</p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 px-3">
          <ul className="space-y-1">
            {filteredNavItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="flex-1">{item.label}</span>
                  {item.badge && (
                    <Badge variant="secondary" className="bg-slate-700 text-white">
                      {item.badge}
                    </Badge>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-slate-800">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-3 w-full p-2 rounded-lg hover:bg-slate-800 transition-colors">
                <Avatar className="w-9 h-9 bg-blue-600">
                  <AvatarFallback className="text-sm font-medium">
                    {user ? getInitials(user.first_name + ' ' + user.last_name) : 'U'}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 text-left">
                  <p className="text-sm font-medium truncate">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs text-slate-400">
                    {user ? getRoleDisplay(user.role) : ''}
                  </p>
                </div>
                <ChevronDown className="w-4 h-4 text-slate-400" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>Mi Cuenta</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigate('/perfil')}>
                <UserCircle className="mr-2 h-4 w-4" />
                Perfil
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                <LogOut className="mr-2 h-4 w-4" />
                Cerrar Sesión
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </aside>

      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 bg-slate-900 text-white z-50">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
              <Scissors className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold">Estilera</span>
          </div>

          <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="text-white">
                <Menu className="w-6 h-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-64 bg-slate-900 text-white p-0">
              <SheetHeader className="p-6 border-b border-slate-800">
                <SheetTitle className="text-white flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
                    <Scissors className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h1 className="font-bold text-lg">Estilera</h1>
                    <p className="text-xs text-slate-400">Sistema de Gestión</p>
                  </div>
                </SheetTitle>
              </SheetHeader>

              <nav className="py-4 px-3">
                <ul className="space-y-1">
                  {filteredNavItems.map((item) => (
                    <li key={item.path}>
                      <Link
                        to={item.path}
                        onClick={() => setIsMobileMenuOpen(false)}
                        className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                          isActive(item.path)
                            ? 'bg-blue-600 text-white'
                            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                        }`}
                      >
                        <item.icon className="w-5 h-5" />
                        <span className="flex-1">{item.label}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </nav>

              <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-800">
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-3 w-full p-2 text-red-400 hover:bg-slate-800 rounded-lg transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Cerrar Sesión</span>
                </button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 lg:ml-64 pt-16 lg:pt-0">
        <div className="p-4 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
