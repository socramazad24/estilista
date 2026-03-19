"""
Employees URLs for estilera project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeLoanViewSet, EmployeeAttendanceViewSet, EmployeeCommissionViewSet

router = DefaultRouter()
router.register(r'', EmployeeViewSet, basename='employees')
router.register(r'loans', EmployeeLoanViewSet, basename='loans')
router.register(r'attendance', EmployeeAttendanceViewSet, basename='attendance')
router.register(r'commissions', EmployeeCommissionViewSet, basename='commissions')

urlpatterns = [
    path('', include(router.urls)),
]
