from django.contrib import admin
from .models import Menu, MenuItem


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'menu', 'parent')


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)