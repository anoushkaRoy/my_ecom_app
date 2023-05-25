from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import Order

class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'complete']
    list_filter = ['complete']
    search_fields = ['customer__username']
    actions = ['export_as_excel']

    def export_as_excel(self, request, queryset):
        # Define the fields to export in the Excel sheet
        fields = ['id', 'customer', 'date_ordered', 'complete']

        # Generate the exported Excel file
        return self.export_excel(request, queryset, fields)

    export_as_excel.short_description = 'Export selected orders as Excel'


