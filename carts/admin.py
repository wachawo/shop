from django.contrib import admin
from .models import Invoice

# Register your models here.


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'paid', 'amount']
    list_filter = ['name', 'phone']
    list_editable = ['paid']


admin.site.register(Invoice, InvoiceAdmin)
