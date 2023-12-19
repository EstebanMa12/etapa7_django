from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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
from django.contrib.auth.password_validation import validate_password
    
class CustomUserManager(BaseUserManager):
    # Custom user manager
    def create_user(self, username,
                    password=None,
                    team=None,
                    is_admin=False,
                    is_superuser=False,
                    **extra_fields):
        
        if not username:
            raise ValueError('Users must have a username')
        
        if not team:
            raise ValueError('Users must have a team')
        
        try:
            validate_email(username)
        except ValidationError as e:
            raise ValueError(f'Invalid email address:{e}')
        
        try:
            validate_password(password)
        except ValidationError:
            
            raise ValueError('Invalid password')
            
        normalize_username = self.normalize_email(username)
        
        
        
        user = self.model(
                        username=normalize_username,
                        team=team,
                        is_admin=is_admin,
                        is_superuser=is_superuser,
                        **extra_fields,
                        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,
                        username,
                        password,
                        team=None,
                        admin=True,
                        superuser=True,
                        **extra_fields):
        # Asigna el valor predeterminado si no se proporciona un equipo
        if team is None:
            team = "SuperUser"

        return self.create_user(username=username,
                                password=password,
                                team=team,
                                is_admin=admin,
                                is_superuser=superuser,
                                **extra_fields)

class CustomUser(PermissionsMixin, AbstractBaseUser, DefaultModel):
    # Use email as the username field
    username = models.EmailField(unique=True)
    team = models.CharField(max_length=255, blank = False, null= False, validators = [validate_slug])
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    
    objects = CustomUserManager()
    

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ("-created_at",)
    
