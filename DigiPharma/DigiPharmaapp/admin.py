from django.contrib import admin
from .models import *

class Medicineadmin(admin.ModelAdmin):
    list_display=('name','price','stock','expiry_date','image')
    search_fields = ('name',)
class Customeradmin(admin.ModelAdmin):
    list_display=['name','contact_info','address']
class Prescriptionadmin(admin.ModelAdmin):
    list_display=['customer','doctor_name','date_issued']
class Salesadmin(admin.ModelAdmin):
    list_display=['customer','medicine','total_amount','sale_date','payment_method']


admin.site.register(Medicine,Medicineadmin)
admin.site.register(Customer,Customeradmin)
admin.site.register(Prescription,Prescriptionadmin)
admin.site.register(Sales,Salesadmin)
