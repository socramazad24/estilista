"""
Employees models for estilera project.
"""
from django.db import models
from django.conf import settings


class Employee(models.Model):
    CONTRACT_TYPE_CHOICES = [
        ('full_time', 'Tiempo completo'),
        ('part_time', 'Medio tiempo'),
        ('freelance', 'Independiente'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('on_leave', 'En licencia'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                null=True, blank=True, related_name='employee_profile', verbose_name='Usuario')
    first_name = models.CharField(max_length=150, verbose_name='Nombres')
    last_name = models.CharField(max_length=150, verbose_name='Apellidos')
    document_type = models.CharField(max_length=20, default='CC', verbose_name='Tipo de documento')
    document_number = models.CharField(max_length=20, unique=True, verbose_name='Número de documento')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    address = models.TextField(blank=True, verbose_name='Dirección')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    hire_date = models.DateField(verbose_name='Fecha de contratación')
    termination_date = models.DateField(null=True, blank=True, verbose_name='Fecha de terminación')
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES, default='full_time', verbose_name='Tipo de contrato')
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Salario base')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='% Comisión')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_active_loans_total(self):
        return sum(loan.remaining_amount for loan in self.loans.filter(status='active'))


class EmployeeLoan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loans', verbose_name='Empleado')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Tasa de interés %')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto total')
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto pendiente')
    installment_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor cuota')
    number_of_installments = models.PositiveIntegerField(verbose_name='Número de cuotas')
    paid_installments = models.PositiveIntegerField(default=0, verbose_name='Cuotas pagadas')
    request_date = models.DateField(verbose_name='Fecha de solicitud')
    approval_date = models.DateField(null=True, blank=True, verbose_name='Fecha de aprobación')
    first_payment_date = models.DateField(null=True, blank=True, verbose_name='Primera fecha de pago')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
    reason = models.TextField(blank=True, verbose_name='Motivo')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='approved_loans', verbose_name='Aprobado por')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Préstamo a empleado'
        verbose_name_plural = 'Préstamos a empleados'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Préstamo #{self.id} - {self.employee} - ${self.amount:,.0f}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            interest = self.amount * (self.interest_rate / 100)
            self.total_amount = self.amount + interest
        if not self.remaining_amount:
            self.remaining_amount = self.total_amount
        if not self.installment_amount and self.number_of_installments:
            self.installment_amount = self.total_amount / self.number_of_installments
        super().save(*args, **kwargs)


class LoanPayment(models.Model):
    loan = models.ForeignKey(EmployeeLoan, on_delete=models.CASCADE, related_name='payments', verbose_name='Préstamo')
    installment_number = models.PositiveIntegerField(verbose_name='Número de cuota')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
    payment_date = models.DateField(verbose_name='Fecha de pago')
    paid_date = models.DateField(null=True, blank=True, verbose_name='Fecha pagada')
    is_paid = models.BooleanField(default=False, verbose_name='Pagado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    class Meta:
        verbose_name = 'Pago de préstamo'
        verbose_name_plural = 'Pagos de préstamos'
        ordering = ['installment_number']
    
    def __str__(self):
        return f"Cuota {self.installment_number} - Préstamo #{self.loan.id}"


class EmployeeAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Presente'),
        ('absent', 'Ausente'),
        ('late', 'Tarde'),
        ('leave', 'Permiso'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances', verbose_name='Empleado')
    date = models.DateField(verbose_name='Fecha')
    check_in = models.TimeField(null=True, blank=True, verbose_name='Hora de entrada')
    check_out = models.TimeField(null=True, blank=True, verbose_name='Hora de salida')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present', verbose_name='Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-date']
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee} - {self.date} - {self.get_status_display()}"


class EmployeeCommission(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='commissions', verbose_name='Empleado')
    sale = models.ForeignKey('sales.Sale', on_delete=models.CASCADE, related_name='commissions', verbose_name='Venta')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Porcentaje')
    is_paid = models.BooleanField(default=False, verbose_name='Pagado')
    paid_date = models.DateField(null=True, blank=True, verbose_name='Fecha de pago')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    class Meta:
        verbose_name = 'Comisión'
        verbose_name_plural = 'Comisiones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comisión {self.employee} - ${self.amount:,.0f}"
