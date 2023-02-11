from django.contrib import admin
from .models import Whatsapp
# Register your models here.


admin.AdminSite.site_header = "SMAV Dashboard"
admin.AdminSite.site_title = "SMAV"
admin.AdminSite.index_title = "WhatsApp and Telegram Setting"


class WhatsAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Whatsapp, WhatsAdmin)
