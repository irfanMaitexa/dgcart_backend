from django.contrib import admin
from .models import  Customer,StaffUser


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'random_id', 'created_at')
    readonly_fields = ('random_id',)
