from django.contrib.auth.models import AbstractUser
from django.db import models

# A default model with the created_at, modified_at, is_deleted field
class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

# Only the super admin can create admins and does not have the field user ?
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email, validate_slug
from django.core.exceptions import ValidationError
    
class CustomUserManager(BaseUserManager):
    # Custom user manager
    def create_user(self, username, password=None, team=None):
        try:
            validate_email(username)
        except ValidationError:
            raise ValueError('Invalid email address')
        
        if not username:
            raise ValueError('Users must have a username')
        
        if not team:
            raise ValueError('Users must have a team')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, team = "SuperUser"):
        # Cuando se crea un superusuario, el equipo puede es "SuperUser"
        if not team:
            team = "SuperUser"
        user = self.create_user(username=username, password=password, team= team)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(DefaultModel, AbstractUser):
    # Use email as the username field
    username = models.EmailField(unique=True)
    team = models.CharField(max_length=255, blank = False, null= False, validators = [validate_slug])
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ("-created_at",)
    
