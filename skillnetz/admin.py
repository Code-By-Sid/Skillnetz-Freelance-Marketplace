from django.contrib import admin
from . models import CustomUser,Job,Skills,JobApplication,ActiveJob,Message,PaymentApplication,Payment,Fileattachment,Work
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
   list_display=('job_title','price','description','post_date')


admin.site.register(Job,UsersAdmin)
admin.site.register(CustomUser)
admin.site.register(Skills)
admin.site.register(JobApplication)
admin.site.register(ActiveJob)
admin.site.register(Message)
admin.site.register(PaymentApplication)
admin.site.register(Fileattachment)
admin.site.register(Work)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    search_fields = ('name','payment_id')