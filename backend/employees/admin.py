"""
Employees admin for estilera project.
"""
from django.contrib import admin
from .models import Employee, EmployeeLoan, LoanPayment, EmployeeAttendance, EmployeeCommission


class LoanPaymentInline(admin.TabularInline):
    model = LoanPayment
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'document_number', 'phone', 'contract_type', 'base_salary', 'status']
    list_filter = ['status', 'contract_type', 'hire_date']
    search_fields = ['first_name', 'last_name', 'document_number']


@admin.register(EmployeeLoan)
class EmployeeLoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'amount', 'remaining_amount', 'status', 'request_date']
    list_filter = ['status', 'request_date']
    search_fields = ['employee__first_name', 'employee__last_name']
    inlines = [LoanPaymentInline]


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name']


@admin.register(EmployeeCommission)
class EmployeeCommissionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'sale', 'amount', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name']
