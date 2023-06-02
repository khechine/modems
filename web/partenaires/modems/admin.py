from django.contrib import admin

# Register your models here.

from .models import User,stock_modemsn_gpon,stock_modemsn,contrat,numacces

admin.site.register(User)
admin.site.register(stock_modemsn_gpon)
admin.site.register(stock_modemsn)
admin.site.register(contrat)
admin.site.register(numacces)