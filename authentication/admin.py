from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from .models import User, Group

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
	form = MyUserChangeForm
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
		('Jogosultságok', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
	)
	
	fieldsets = (
		(None, {'fields': ('email', 'display_name', 'password')}), 
		('Szavazás', {'fields': ('can_vote', 'has_voted')}),
		('Jogosultságok', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
		('Fontos dátumok', {'fields': ('last_login', 'date_joined')}),
	)

@admin.register(User)
class UserAdmin(MyUserAdmin):
	list_display = ['email', 'is_staff', 'has_voted']
	ordering = ['-is_staff', 'email']
	readonly_fields = ['has_voted', 'can_vote', 'date_joined', 'last_login']

admin.site.unregister(DjangoGroup)
admin.site.register(Group, GroupAdmin)