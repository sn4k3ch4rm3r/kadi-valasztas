from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group as BaseGroup

class UserManager(BaseUserManager):
	def create_user(self, email):
		if not email:
			raise ValueError("Email address is required")
		user = self.model(
			email = self.normalize_email(email)
		)
		user.save()
		return user

	def create_superuser(self, email, password):
		user = self.model(
			email = self.normalize_email(email),
		)
		user.set_password(password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save()
		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name='Email cím', unique=True)
	display_name = models.CharField(verbose_name='Név', max_length=100, blank=True)

	date_joined	= models.DateTimeField(verbose_name='Csatlakozás dátuma', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='Utolsó bejelentkezés', auto_now=True)

	is_staff = models.BooleanField(verbose_name='Személyzet státusz', help_text='Megadja, hogy ez a felhasználó megtekintheti-e az admin felületet.', default=False)
	is_active = models.BooleanField(verbose_name='Aktív', default=True)

	has_voted = models.BooleanField(verbose_name='Szavazott', default=False)
	can_vote = models.BooleanField(verbose_name='Szavazhat', default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'Felhasználó'
		verbose_name_plural = 'Felhasználók'

class Group(BaseGroup):
	class Meta:
		verbose_name = "Csoport"
		verbose_name_plural = 'Csoportok'
		proxy = True