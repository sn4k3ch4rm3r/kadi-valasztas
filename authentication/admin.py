from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from .models import User, Group

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserCreationForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['password1'].required = False
		self.fields['password2'].required = False

	def save(self, commit=True):
		user = super(MyUserCreationForm, self).save(commit=False)
		user.set_unusable_password()

		if commit:
			user.save()
		
		return user

class MyUserAdmin(UserAdmin):
	form = MyUserChangeForm
	add_form = MyUserCreationForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email',),
		}),
		('Jogosultságok', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
	)
	
	fieldsets = (
		(None, {'fields': ('email', 'display_name')}), 
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