from django.contrib import admin

from .models import Subscription

# Register your models here.

@admin.register(Subscription)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount','date','status','transaction_id', 'parieur')
    
    