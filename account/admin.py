from django.contrib import admin
from .models import Register, Address, ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject')


admin.site.register(Register)
admin.site.register(Address)
