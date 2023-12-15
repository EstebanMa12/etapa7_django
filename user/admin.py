
from django.contrib import admin


#Models for teams
from .models import Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name',)
    list_filter = ('team_name',)
    search_fields = ('team_name',)
    ordering = ('team_name',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('team_name',)
        }),
    )
    
    

#Models for users
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','username', 'team', 'is_superuser', 'is_admin')
    list_filter = ('username', 'team', 'is_superuser', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'team')
    list_per_page = 10
    
    fieldsets = (
        (None, {'fields': ('username',
                        'password')}),
        ('Personal Info', {'fields':('team',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin','is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'team', 'is_superuser', 'is_admin', 'is_active'),
            }),
    )
admin.site.register(CustomUser, CustomUserAdmin)
