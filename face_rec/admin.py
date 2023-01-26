from django.contrib import admin

from .forms import EnrollForm
from .models import *
# Register your models here.
class AdministraionAdmin(admin.ModelAdmin):
    list_display=('username','f_name','l_name')
class EnrollAdmin(admin.ModelAdmin):
    form = EnrollForm
    list_display=('first_name','last_name', 'Arid_no','img')
admin.site.register(Administraion, AdministraionAdmin)
admin.site.register(Enroll,EnrollAdmin)
