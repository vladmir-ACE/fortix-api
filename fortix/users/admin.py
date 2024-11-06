from django.contrib import admin

from .models import Country, Forcasseur, Parieur,User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number','username','password','first_name', 'last_name', 'is_forcasseur', 'is_parieur')
    search_fields = ('phone_number', 'first_name', 'last_name')  # Pour faciliter la recherche dans l'admin
    
@admin.register(Parieur)
class ParieurAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription_active', 'subscription_start_date', 'subscription_end_date')
    search_fields = ('user__first_name', 'user__phone_number')
    
@admin.register(Forcasseur)
class ForcasseurAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_winnings', 'success_rate')
    search_fields = ('user__first_name', 'user__phone_number')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


