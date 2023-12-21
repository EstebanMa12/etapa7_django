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
    """
    Custom user manager for creating and managing user objects.
    """

    def create_user(self, username,
                    password=None,
                    team=None,
                    is_admin=False,
                    is_superuser=False,
                    **extra_fields):
        """
        Creates a new user object with the provided username, password, team, and additional fields.

        Args:
            username (str): The username of the user.
            password (str, optional): The password of the user. Defaults to None.
            team (str, optional): The team of the user. Defaults to None.
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.
            is_superuser (bool, optional): Whether the user is a superuser. Defaults to False.
            **extra_fields: Additional fields to be included in the user object.

        Returns:
            User: The created user object.

        Raises:
            ValueError: If the username or team is not provided.
        """
        
        if not username:
            raise ValueError('Users must have a username')
        
        if not team:
            raise ValueError('Users must have a team')
        
        #Dado que se requiere que el almacenado de los usuarios falle si no cumple con las excepciones, se deja por fuera las siguientes validaciones de un try/except
        validate_email(username)
        validate_password(password)
        
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
        """
        Creates a new superuser object with the provided username, password, team, and additional fields.

        Args:
            username (str): The username of the superuser.
            password (str): The password of the superuser.
            team (str, optional): The team of the superuser. Defaults to None.
            admin (bool, optional): Whether the superuser is an admin. Defaults to True.
            superuser (bool, optional): Whether the superuser is a superuser. Defaults to True.
            **extra_fields: Additional fields to be included in the superuser object.

        Returns:
            User: The created superuser object.

        Raises:
            ValueError: If the username is not provided.
        """
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
    
