from django.contrib import admin
from .models import  *


admin.site.register(Cart)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    
@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'random_id', 'created_at')
    readonly_fields = ('random_id',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('customer', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'message', 'response')
    readonly_fields = ('customer', 'subject', 'message', 'created_at')  # Make these fields read-only

    fieldsets = (
        (None, {
            'fields': ('customer', 'subject', 'message', 'created_at')
        }),
        ('Response', {
            'fields': ('response', 'status'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Automatically set status to "Resolved" if a response is provided
        if obj.response and not obj.response.isspace():
            obj.status = 'Resolved'
        super().save_model(request, obj, form, change)

