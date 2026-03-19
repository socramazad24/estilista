# Estilera - Sistema de Gestión para Salón de Belleza

Sistema completo de gestión para estilerías/salones de belleza con funcionalidades de ventas, inventario, empleados, préstamos y auditorías.

## Características

### Módulos Principales
- **Dashboard**: Visualización de ventas del día, semana y mes con gráficos y estadísticas
- **Gestión de Ventas**: Creación de ventas con múltiples servicios, facturación automática
- **Gestión de Servicios**: Categorías y servicios (cepillados, planchados, uñas, tintes, etc.)
- **Gestión de Inventario**: Productos, movimientos de inventario, alertas de stock bajo
- **Gestión de Proveedores**: Proveedores y órdenes de compra
- **Gestión de Empleados**: Empleados, asistencias, comisiones
- **Préstamos a Empleados**: Sistema de préstamos con cuotas y pagos
- **Auditorías**: Registro de todas las acciones realizadas en el sistema
- **Gestión de Usuarios**: Roles (admin, estilista, cajero, asistente)

### Características Técnicas
- **Backend**: Django + Django REST Framework
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Autenticación**: JWT (JSON Web Tokens)
- **Base de Datos**: SQLite (configurable a PostgreSQL)
- **Diseño**: Responsive con colores pastel negro y azul
- **Moneda**: Pesos Colombianos (COP)

## Instalación

### Requisitos
- Python 3.10+
- Node.js 18+
- npm o yarn

### 1. Clonar o descargar el proyecto

```bash
cd /mnt/okcomputer/output
```

### 2. Configurar el Backend

```bash
# Instalar dependencias de Python
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pillow python-dateutil django-filter

# Aplicar migraciones
cd backend
python manage.py migrate

# Cargar datos de prueba (opcional)
python seed_data.py
```

### 3. Configurar el Frontend

```bash
cd ../app
npm install
npm run build
```

## Ejecución

### Opción 1: Ejecutar Backend y Frontend por separado

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend (desarrollo):**
```bash
cd app
npm run dev
```

### Opción 2: Usar el script de inicio

```bash
python start_server.py
```

## Acceso

- **Frontend**: http://localhost:5173 (desarrollo) o http://localhost:8000 (producción)
- **API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

### Credenciales de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | Admin123! | Administrador |
| maria.gomez | Estilista123! | Estilista |
| ana.lopez | Estilista123! | Estilista |
| cajero1 | Cajero123! | Cajero |

## Estructura del Proyecto

```
/mnt/okcomputer/output/
├── backend/                    # Backend Django
│   ├── estilera/              # Configuración principal
│   ├── users/                 # Gestión de usuarios
│   ├── services/              # Gestión de servicios
│   ├── sales/                 # Gestión de ventas y clientes
│   ├── inventory/             # Gestión de inventario
│   ├── providers/             # Gestión de proveedores
│   ├── employees/             # Gestión de empleados y préstamos
│   ├── audits/                # Sistema de auditoría
│   ├── manage.py
│   └── seed_data.py           # Script de datos de prueba
│
├── app/                       # Frontend React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── contexts/          # Contextos (Auth)
│   │   ├── hooks/             # Hooks personalizados
│   │   ├── services/          # Servicios API
│   │   ├── types/             # Tipos TypeScript
│   │   └── pages/             # Páginas
│   └── dist/                  # Build de producción
│
└── README.md
```

## API Endpoints

### Autenticación
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token

### Usuarios
- `GET /api/users/` - Listar usuarios
- `GET /api/users/me/` - Usuario actual
- `POST /api/users/change_password/` - Cambiar contraseña

### Servicios
- `GET /api/services/` - Listar servicios
- `GET /api/services/categories/` - Categorías de servicios
- `GET /api/services/by_category/` - Servicios agrupados por categoría

### Ventas
- `GET /api/sales/` - Listar ventas
- `POST /api/sales/` - Crear venta
- `GET /api/sales/today/` - Ventas de hoy
- `GET /api/sales/report/?period=day|week|month` - Reporte de ventas
- `GET /api/sales/dashboard_stats/` - Estadísticas para dashboard

### Clientes
- `GET /api/sales/clients/` - Listar clientes
- `POST /api/sales/clients/` - Crear cliente

### Inventario
- `GET /api/inventory/products/` - Listar productos
- `GET /api/inventory/products/low_stock/` - Productos con stock bajo
- `GET /api/inventory/movements/` - Movimientos de inventario

### Empleados y Préstamos
- `GET /api/employees/` - Listar empleados
- `GET /api/employees/loans/` - Listar préstamos
- `POST /api/employees/loans/{id}/register_payment/` - Registrar pago

### Auditorías
- `GET /api/audits/logs/` - Registros de auditoría
- `GET /api/audits/logs/summary/` - Resumen de auditoría

## Seguridad

- Contraseñas encriptadas con PBKDF2
- Validación de contraseñas (mínimo 8 caracteres)
- Autenticación JWT con refresh tokens
- CORS configurado
- Middleware de auditoría para registrar todas las acciones

## Personalización

### Colores
Los colores se pueden modificar en:
- Frontend: `app/src/index.css` (variables CSS)
- Backend: Configuración en `estilera/settings.py`

### Servicios
Los servicios se pueden gestionar desde el panel de administración de Django o desde la interfaz de servicios.

## Soporte

Para reportar problemas o solicitar características, por favor contactar al administrador del sistema.

## Licencia

Este proyecto es propiedad de Estilera. Todos los derechos reservados.
