from django.contrib.auth.models import AbstractUser
from django.db import models

# A default model with the created_at, modified_at, is_deleted field
class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Team(DefaultModel, models.Model):
    # Teams model
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name

# Only the super admin can create admins and does not have the field user ?
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
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
            raise ValueError('Normal users must have a team')
        user = self.model(username=username, team=team)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, team=None):
        # Cuando se crea un superusuario, el equipo puede ser None
        user = self.create_user(username=username, password=password, team=team)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    # Use email as the username field
    username = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    

    def __str__(self):
        return self.username
    
