from django.contrib import admin

# Register your models here.
from web.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ("__str__", "postal_code")
    readonly_fields = ("creation_time",)
