"""
Seed data for estilera project.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estilera.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import ServiceCategory, Service
from sales.models import Client, Sale, SaleItem
from inventory.models import ProductCategory, Product
from providers.models import Provider
from employees.models import Employee, EmployeeLoan
from audits.models import AuditLog
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()


def create_users():
    print("Creando usuarios...")
    
    # Admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@estilera.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('Admin123!')
        admin.save()
        print(f"  - Admin creado: admin / Admin123!")
    
    # Stylist users
    stylists_data = [
        {'username': 'maria.gomez', 'first_name': 'María', 'last_name': 'Gómez', 'email': 'maria@estilera.com'},
        {'username': 'ana.lopez', 'first_name': 'Ana', 'last_name': 'López', 'email': 'ana@estilera.com'},
        {'username': 'carla.ruiz', 'first_name': 'Carla', 'last_name': 'Ruiz', 'email': 'carla@estilera.com'},
    ]
    
    for data in stylists_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': 'stylist'
            }
        )
        if created:
            user.set_password('Estilista123!')
            user.save()
            print(f"  - Estilista creado: {data['username']} / Estilista123!")
    
    # Cashier user
    cashier, created = User.objects.get_or_create(
        username='cajero1',
        defaults={
            'email': 'cajero@estilera.com',
            'first_name': 'Pedro',
            'last_name': 'Martínez',
            'role': 'cashier'
        }
    )
    if created:
        cashier.set_password('Cajero123!')
        cashier.save()
        print(f"  - Cajero creado: cajero1 / Cajero123!")
    
    print("Usuarios creados exitosamente!")
    return User.objects.all()


def create_service_categories():
    print("\nCreando categorías de servicios...")
    
    categories_data = [
        {'name': 'Cepillado', 'description': 'Servicios de cepillado de cabello', 'color': '#E91E63'},
        {'name': 'Planchado', 'description': 'Servicios de planchado de cabello', 'color': '#9C27B0'},
        {'name': 'Uñas', 'description': 'Servicios de manicure y pedicure', 'color': '#673AB7'},
        {'name': 'Tintes', 'description': 'Servicios de coloración', 'color': '#3F51B5'},
        {'name': 'Cortes', 'description': 'Cortes de cabello', 'color': '#2196F3'},
        {'name': 'Tratamientos', 'description': 'Tratamientos capilares', 'color': '#00BCD4'},
        {'name': 'Maquillaje', 'description': 'Servicios de maquillaje', 'color': '#FF5722'},
        {'name': 'Depilación', 'description': 'Servicios de depilación', 'color': '#795548'},
    ]
    
    for data in categories_data:
        category, created = ServiceCategory.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'color': data['color']
            }
        )
        if created:
            print(f"  - Categoría creada: {data['name']}")
    
    print("Categorías de servicios creadas exitosamente!")
    return ServiceCategory.objects.all()


def create_services(categories):
    print("\nCreando servicios...")
    
    services_data = [
        # Cepillado
        {'category': 'Cepillado', 'name': 'Cepillado Sencillo', 'price': 35000, 'duration': 60},
        {'category': 'Cepillado', 'name': 'Cepillado con Plancha', 'price': 45000, 'duration': 90},
        {'category': 'Cepillado', 'name': 'Cepillado con Keratina', 'price': 85000, 'duration': 120},
        
        # Planchado
        {'category': 'Planchado', 'name': 'Planchado Sencillo', 'price': 25000, 'duration': 45},
        {'category': 'Planchado', 'name': 'Planchado Profundo', 'price': 40000, 'duration': 60},
        
        # Uñas
        {'category': 'Uñas', 'name': 'Manicure Básico', 'price': 18000, 'duration': 30},
        {'category': 'Uñas', 'name': 'Manicure Semipermanente', 'price': 35000, 'duration': 45},
        {'category': 'Uñas', 'name': 'Pedicure Básico', 'price': 25000, 'duration': 45},
        {'category': 'Uñas', 'name': 'Pedicure Semipermanente', 'price': 45000, 'duration': 60},
        {'category': 'Uñas', 'name': 'Uñas Acrílicas', 'price': 65000, 'duration': 90},
        
        # Tintes
        {'category': 'Tintes', 'name': 'Tinte Raíz', 'price': 45000, 'duration': 60},
        {'category': 'Tintes', 'name': 'Tinte Completo', 'price': 75000, 'duration': 90},
        {'category': 'Tintes', 'name': 'Mechas', 'price': 95000, 'duration': 120},
        {'category': 'Tintes', 'name': 'Balayage', 'price': 120000, 'duration': 150},
        {'category': 'Tintes', 'name': 'Decoloración', 'price': 80000, 'duration': 120},
        
        # Cortes
        {'category': 'Cortes', 'name': 'Corte Mujer', 'price': 25000, 'duration': 45},
        {'category': 'Cortes', 'name': 'Corte Hombre', 'price': 18000, 'duration': 30},
        {'category': 'Cortes', 'name': 'Corte Niño', 'price': 15000, 'duration': 30},
        {'category': 'Cortes', 'name': 'Corte con Lavado', 'price': 35000, 'duration': 60},
        
        # Tratamientos
        {'category': 'Tratamientos', 'name': 'Hidratación Capilar', 'price': 45000, 'duration': 45},
        {'category': 'Tratamientos', 'name': 'Botox Capilar', 'price': 85000, 'duration': 60},
        {'category': 'Tratamientos', 'name': 'Keratina', 'price': 150000, 'duration': 120},
        
        # Maquillaje
        {'category': 'Maquillaje', 'name': 'Maquillaje Social', 'price': 55000, 'duration': 60},
        {'category': 'Maquillaje', 'name': 'Maquillaje Novia', 'price': 150000, 'duration': 90},
        {'category': 'Maquillaje', 'name': 'Maquillaje Fiesta', 'price': 75000, 'duration': 60},
        
        # Depilación
        {'category': 'Depilación', 'name': 'Depilación Cejas', 'price': 12000, 'duration': 15},
        {'category': 'Depilación', 'name': 'Depilación Bigote', 'price': 8000, 'duration': 15},
        {'category': 'Depilación', 'name': 'Depilación Axilas', 'price': 18000, 'duration': 20},
    ]
    
    category_map = {c.name: c for c in categories}
    
    for data in services_data:
        category = category_map.get(data['category'])
        if category:
            service, created = Service.objects.get_or_create(
                category=category,
                name=data['name'],
                defaults={
                    'price': data['price'],
                    'duration_minutes': data['duration']
                }
            )
            if created:
                print(f"  - Servicio creado: {data['name']} - ${data['price']:,}")
    
    print("Servicios creados exitosamente!")
    return Service.objects.all()


def create_clients():
    print("\nCreando clientes...")
    
    clients_data = [
        {'first_name': 'Laura', 'last_name': 'Hernández', 'phone': '3001234567', 'email': 'laura@email.com'},
        {'first_name': 'Carmen', 'last_name': 'Díaz', 'phone': '3102345678', 'email': 'carmen@email.com'},
        {'first_name': 'Patricia', 'last_name': 'Morales', 'phone': '3203456789', 'email': 'patricia@email.com'},
        {'first_name': 'Diana', 'last_name': 'Castro', 'phone': '3004567890', 'email': 'diana@email.com'},
        {'first_name': 'Sofia', 'last_name': 'Vargas', 'phone': '3105678901', 'email': 'sofia@email.com'},
        {'first_name': 'Valentina', 'last_name': 'Romero', 'phone': '3206789012', 'email': 'valentina@email.com'},
        {'first_name': 'Isabella', 'last_name': 'Moreno', 'phone': '3007890123', 'email': 'isabella@email.com'},
        {'first_name': 'Camila', 'last_name': 'Jiménez', 'phone': '3108901234', 'email': 'camila@email.com'},
        {'first_name': 'Mariana', 'last_name': 'Santos', 'phone': '3209012345', 'email': 'mariana@email.com'},
        {'first_name': 'Daniela', 'last_name': 'Ortiz', 'phone': '3010123456', 'email': 'daniela@email.com'},
    ]
    
    for data in clients_data:
        client, created = Client.objects.get_or_create(
            phone=data['phone'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email']
            }
        )
        if created:
            print(f"  - Cliente creado: {data['first_name']} {data['last_name']}")
    
    print("Clientes creados exitosamente!")
    return Client.objects.all()


def create_product_categories():
    print("\nCreando categorías de productos...")
    
    categories_data = [
        {'name': 'Shampoo', 'description': 'Champús para el cabello'},
        {'name': 'Acondicionador', 'description': 'Acondicionadores y tratamientos'},
        {'name': 'Tintes', 'description': 'Coloración capilar'},
        {'name': 'Tratamientos', 'description': 'Tratamientos capilares'},
        {'name': 'Styling', 'description': 'Productos de peinado'},
        {'name': 'Uñas', 'description': 'Productos para uñas'},
        {'name': 'Herramientas', 'description': 'Herramientas y equipos'},
    ]
    
    for data in categories_data:
        category, created = ProductCategory.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        if created:
            print(f"  - Categoría creada: {data['name']}")
    
    print("Categorías de productos creadas exitosamente!")
    return ProductCategory.objects.all()


def create_products(categories):
    print("\nCreando productos...")
    
    products_data = [
        {'category': 'Shampoo', 'name': 'Shampoo Hidratante 500ml', 'stock': 25, 'purchase_price': 25000, 'sale_price': 45000},
        {'category': 'Shampoo', 'name': 'Shampoo Anticaspa 400ml', 'stock': 18, 'purchase_price': 22000, 'sale_price': 38000},
        {'category': 'Shampoo', 'name': 'Shampoo Color 500ml', 'stock': 15, 'purchase_price': 28000, 'sale_price': 48000},
        {'category': 'Acondicionador', 'name': 'Acondicionador Hidratante 500ml', 'stock': 20, 'purchase_price': 23000, 'sale_price': 42000},
        {'category': 'Acondicionador', 'name': 'Mascarilla Nutritiva 300ml', 'stock': 12, 'purchase_price': 18000, 'sale_price': 32000},
        {'category': 'Tintes', 'name': 'Tinte Permanente Negro', 'stock': 30, 'purchase_price': 12000, 'sale_price': 22000},
        {'category': 'Tintes', 'name': 'Tinte Permanente Castaño', 'stock': 28, 'purchase_price': 12000, 'sale_price': 22000},
        {'category': 'Tintes', 'name': 'Tinte Permanente Rubio', 'stock': 25, 'purchase_price': 15000, 'sale_price': 28000},
        {'category': 'Tintes', 'name': 'Decolorante en Polvo 500g', 'stock': 10, 'purchase_price': 35000, 'sale_price': 55000},
        {'category': 'Tintes', 'name': 'Peróxido 20 Vol', 'stock': 15, 'purchase_price': 8000, 'sale_price': 15000},
        {'category': 'Tintes', 'name': 'Peróxido 30 Vol', 'stock': 12, 'purchase_price': 9000, 'sale_price': 16000},
        {'category': 'Tratamientos', 'name': 'Ampolleta Reparadora', 'stock': 40, 'purchase_price': 5000, 'sale_price': 10000},
        {'category': 'Tratamientos', 'name': 'Keratina Líquida 250ml', 'stock': 8, 'purchase_price': 45000, 'sale_price': 75000},
        {'category': 'Styling', 'name': 'Gel Fijador 200ml', 'stock': 22, 'purchase_price': 10000, 'sale_price': 18000},
        {'category': 'Styling', 'name': 'Spray de Brillo 300ml', 'stock': 18, 'purchase_price': 12000, 'sale_price': 22000},
        {'category': 'Styling', 'name': 'Crema para Peinar 400ml', 'stock': 20, 'purchase_price': 14000, 'sale_price': 25000},
        {'category': 'Uñas', 'name': 'Esmalte Regular Rojo', 'stock': 35, 'purchase_price': 5000, 'sale_price': 12000},
        {'category': 'Uñas', 'name': 'Esmalte Semipermanente', 'stock': 25, 'purchase_price': 15000, 'sale_price': 28000},
        {'category': 'Uñas', 'name': 'Removedor de Esmalte', 'stock': 20, 'purchase_price': 6000, 'sale_price': 12000},
        {'category': 'Uñas', 'name': 'Acrílico para Uñas', 'stock': 15, 'purchase_price': 25000, 'sale_price': 45000},
        {'category': 'Herramientas', 'name': 'Tijeras Profesionales', 'stock': 5, 'purchase_price': 80000, 'sale_price': 120000},
        {'category': 'Herramientas', 'name': 'Secador de Cabello', 'stock': 8, 'purchase_price': 120000, 'sale_price': 180000},
        {'category': 'Herramientas', 'name': 'Plancha de Cabello', 'stock': 6, 'purchase_price': 150000, 'sale_price': 220000},
    ]
    
    category_map = {c.name: c for c in categories}
    
    for data in products_data:
        category = category_map.get(data['category'])
        if category:
            product, created = Product.objects.get_or_create(
                category=category,
                name=data['name'],
                defaults={
                    'stock': data['stock'],
                    'purchase_price': data['purchase_price'],
                    'sale_price': data['sale_price'],
                    'min_stock': 5
                }
            )
            if created:
                print(f"  - Producto creado: {data['name']}")
    
    print("Productos creados exitosamente!")
    return Product.objects.all()


def create_providers():
    print("\nCreando proveedores...")
    
    providers_data = [
        {'name': 'Distribuidora Belleza Total', 'contact_name': 'Juan Pérez', 'phone': '6012345678', 'email': 'ventas@bellezatotal.com', 'city': 'Bogotá', 'nit': '900123456-7'},
        {'name': 'Productos Capilares SAS', 'contact_name': 'Carlos Rodríguez', 'phone': '6013456789', 'email': 'info@productoscapilares.com', 'city': 'Bogotá', 'nit': '800234567-8'},
        {'name': 'Importadora de Belleza', 'contact_name': 'Luis Martínez', 'phone': '6014567890', 'email': 'contacto@importadorabelleza.com', 'city': 'Medellín', 'nit': '900345678-9'},
        {'name': 'Uñas y Más Distribuciones', 'contact_name': 'Andrea Sánchez', 'phone': '6015678901', 'email': 'pedidos@unyasymas.com', 'city': 'Cali', 'nit': '800456789-0'},
        {'name': 'Equipos Profesionales Spa', 'contact_name': 'Roberto Gómez', 'phone': '6016789012', 'email': 'ventas@equiposspa.com', 'city': 'Bogotá', 'nit': '900567890-1'},
    ]
    
    for data in providers_data:
        provider, created = Provider.objects.get_or_create(
            nit=data['nit'],
            defaults={
                'name': data['name'],
                'contact_name': data['contact_name'],
                'phone': data['phone'],
                'email': data['email'],
                'city': data['city']
            }
        )
        if created:
            print(f"  - Proveedor creado: {data['name']}")
    
    print("Proveedores creados exitosamente!")
    return Provider.objects.all()


def create_employees(users):
    print("\nCreando empleados...")
    
    employees_data = [
        {'first_name': 'María', 'last_name': 'Gómez', 'document': '1012345678', 'phone': '3001112222', 'salary': 1500000, 'commission': 10},
        {'first_name': 'Ana', 'last_name': 'López', 'document': '1023456789', 'phone': '3002223333', 'salary': 1400000, 'commission': 10},
        {'first_name': 'Carla', 'last_name': 'Ruiz', 'document': '1034567890', 'phone': '3003334444', 'salary': 1300000, 'commission': 8},
        {'first_name': 'Pedro', 'last_name': 'Martínez', 'document': '1045678901', 'phone': '3004445555', 'salary': 1200000, 'commission': 0},
        {'first_name': 'Diana', 'last_name': 'Castro', 'document': '1056789012', 'phone': '3005556666', 'salary': 1100000, 'commission': 5},
    ]
    
    for i, data in enumerate(employees_data):
        employee, created = Employee.objects.get_or_create(
            document_number=data['document'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'hire_date': date(2023, 1, 15),
                'base_salary': data['salary'],
                'commission_rate': data['commission']
            }
        )
        if created:
            print(f"  - Empleado creado: {data['first_name']} {data['last_name']}")
    
    print("Empleados creados exitosamente!")
    return Employee.objects.all()


def create_loans(employees):
    print("\nCreando préstamos...")
    
    # Create a loan for the first employee
    employee = employees[0]
    loan, created = EmployeeLoan.objects.get_or_create(
        employee=employee,
        amount=500000,
        defaults={
            'interest_rate': 0,
            'number_of_installments': 5,
            'request_date': date.today() - timedelta(days=30),
            'first_payment_date': date.today() - timedelta(days=15),
            'reason': 'Emergencia médica familiar'
        }
    )
    if created:
        print(f"  - Préstamo creado para {employee.get_full_name()}: $500,000")
    
    print("Préstamos creados exitosamente!")


def create_sales(users, clients, services):
    print("\nCreando ventas de ejemplo...")
    
    stylists = users.filter(role='stylist')
    cashier = users.filter(role='cashier').first() or users.filter(role='admin').first()
    payment_methods = ['cash', 'card', 'transfer', 'nequi']
    
    # Create 20 sales for the last 30 days
    for i in range(20):
        client = random.choice(list(clients))
        stylist = random.choice(list(stylists))
        
        # Random date in the last 30 days
        sale_date = timezone.now() - timedelta(days=random.randint(0, 30))
        
        # Create sale
        sale = Sale.objects.create(
            client=client,
            stylist=stylist,
            cashier=cashier,
            date=sale_date,
            subtotal=0,
            discount=0,
            tax=0,
            total=0,
            payment_method=random.choice(payment_methods),
            status='completed'
        )
        
        # Add 1-3 random services
        num_services = random.randint(1, 3)
        selected_services = random.sample(list(services), num_services)
        
        subtotal = 0
        for service in selected_services:
            quantity = 1
            unit_price = service.price
            SaleItem.objects.create(
                sale=sale,
                service=service,
                quantity=quantity,
                unit_price=unit_price,
                total=quantity * unit_price
            )
            subtotal += quantity * unit_price
        
        sale.subtotal = subtotal
        sale.total = subtotal
        sale.save()
        
        print(f"  - Venta creada: {sale.invoice_number} - ${sale.total:,.0f}")
    
    print("Ventas creadas exitosamente!")


def create_audit_logs():
    print("\nCreando logs de auditoría...")
    
    actions = ['CREATE', 'UPDATE', 'DELETE', 'VIEW']
    models = ['users', 'services', 'sales', 'inventory', 'providers']
    
    for i in range(30):
        AuditLog.objects.create(
            action=random.choice(actions),
            model_name=random.choice(models),
            description=f"Acción de sistema automática {i+1}"
        )
    
    print("Logs de auditoría creados exitosamente!")


if __name__ == '__main__':
    from django.utils import timezone
    
    print("=" * 60)
    print("INICIANDO CREACIÓN DE DATOS DE PRUEBA")
    print("=" * 60)
    
    users = create_users()
    categories = create_service_categories()
    services = create_services(categories)
    clients = create_clients()
    product_categories = create_product_categories()
    products = create_products(product_categories)
    providers = create_providers()
    employees = create_employees(users)
    create_loans(employees)
    create_sales(users, clients, services)
    create_audit_logs()
    
    print("\n" + "=" * 60)
    print("DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
    print("=" * 60)
    print("\nCredenciales de acceso:")
    print("  - Admin: admin / Admin123!")
    print("  - Estilistas: maria.gomez / Estilista123!")
    print("  - Cajero: cajero1 / Cajero123!")
