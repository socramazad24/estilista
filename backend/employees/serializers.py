"""
Employees serializers for estilera project.
"""
from rest_framework import serializers
from .models import Employee, EmployeeLoan, LoanPayment, EmployeeAttendance, EmployeeCommission


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    contract_type_display = serializers.CharField(source='get_contract_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    active_loans_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'user_name', 'first_name', 'last_name', 'full_name',
                  'document_type', 'document_number', 'phone', 'email', 'address',
                  'birth_date', 'hire_date', 'termination_date', 'contract_type',
                  'contract_type_display', 'base_salary', 'commission_rate', 'status',
                  'status_display', 'active_loans_total', 'notes', 'created_at', 'updated_at']


class EmployeeListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'phone', 'contract_type', 'status', 'base_salary']


class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = ['id', 'installment_number', 'amount', 'payment_date', 'paid_date', 'is_paid', 'notes']


class EmployeeLoanSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    payments = LoanPaymentSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeLoan
        fields = ['id', 'employee', 'employee_name', 'amount', 'interest_rate', 'total_amount',
                  'remaining_amount', 'installment_amount', 'number_of_installments',
                  'paid_installments', 'request_date', 'approval_date', 'first_payment_date',
                  'status', 'status_display', 'reason', 'approved_by', 'approved_by_name',
                  'payments', 'progress_percentage', 'notes', 'created_at']
    
    def get_progress_percentage(self, obj):
        if obj.total_amount > 0:
            return ((obj.total_amount - obj.remaining_amount) / obj.total_amount) * 100
        return 0


class EmployeeLoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLoan
        fields = ['employee', 'amount', 'interest_rate', 'number_of_installments', 
                  'request_date', 'first_payment_date', 'reason']
    
    def create(self, validated_data):
        loan = super().create(validated_data)
        
        # Create payment schedule
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        
        payment_date = loan.first_payment_date
        for i in range(1, loan.number_of_installments + 1):
            LoanPayment.objects.create(
                loan=loan,
                installment_number=i,
                amount=loan.installment_amount,
                payment_date=payment_date
            )
            payment_date = payment_date + relativedelta(months=1)
        
        return loan


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EmployeeAttendance
        fields = ['id', 'employee', 'employee_name', 'date', 'check_in', 'check_out',
                  'status', 'status_display', 'notes', 'created_at']


class EmployeeCommissionSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeCommission
        fields = ['id', 'employee', 'employee_name', 'sale', 'amount', 'percentage',
                  'is_paid', 'paid_date', 'created_at']
