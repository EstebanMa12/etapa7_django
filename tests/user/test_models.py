import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from user.models import CustomUserManager
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db

User = get_user_model()

class TestUserModel:
    @pytest.mark.django_db
    def test_create_user(self, user_factory):
        username = "test@example.com"
        password = "StrongPassword123!"
        team = "Test Team"
        is_admin = False
        is_superuser = False
        user = user_factory(username=username,
                            password=password,
                            team=team)
        assert user.username == username
        assert user.team == team
        assert user.is_admin == is_admin
        assert user.is_superuser == is_superuser
        
    @pytest.mark.django_db
    def test_validate_unique_username(self, user_factory):
        username = "test@example.com"
        password = "StrongPassword123!"
        team = "Test Team"
        is_admin = False
        is_superuser = False
        
        # Crea un usuario con el mismo correo electrónico antes de la prueba
        user_factory(username=username,
                    password=password,
                    team=team,
                    is_admin=is_admin,
                    is_superuser=is_superuser)

        # Intenta crear otro usuario con el mismo correo electrónico
        with pytest.raises(IntegrityError, match='UNIQUE constraint failed'):
            user_factory(username=username,
                        password=password,
                        team=team,
                        is_admin=is_admin,
                        is_superuser=is_superuser)
    
    @pytest.mark.django_db
    def test_create_user_invalid_email(self, user_factory):
        username = "invalid"
        password = "StrongPassword123!"
        team = "Test Team"
        is_admin = False
        is_superuser = False
        
        create_user_with_invalid_email = lambda: user_factory(
            username=username,
            password=password,
            team=team,
            is_admin=is_admin,
            is_superuser=is_superuser
        )
        try:
            create_user_with_invalid_email()
        except ValueError as e:
            assert str(e) == 'Invalid email address'
            
    
    @pytest.mark.django_db
    def test_create_user_invalid_password(self, user_factory):
        username = "test@example.com"
        password = "weak"
        team = "Test Team"
        is_admin = False
        is_superuser = False
        try:
            user_factory(username=username,
                        password=password,
                        team=team,
                        is_admin=is_admin,
                        is_superuser=is_superuser)
        except ValueError as e:
            print(str(e))
            assert str(e) == 'Invalid password'
    
    @pytest.mark.django_db
    def test_create_user_missing_username(self, user_factory):
        username = ""
        password = "StrongPassword123!"
        team = "Test Team"
        is_admin = False
        is_superuser = False
        try:
            user_factory(username=username,
                        password=password,
                        team=team,
                        is_admin=is_admin,
                        is_superuser=is_superuser)
        except ValueError as e:
            assert str(e) == 'Users must have a username'
    
    @pytest.mark.django_db
    def test_create_user_missing_team(self, user_factory):
        username = "test@example.com"
        password = "StrongPassword123!"
        team = ""
        is_admin = False
        is_superuser = False
        # This should not raise an exception because the field is nullable
        user = user_factory(username=username,
                            password=password,
                            team=team,
                            is_admin=is_admin,
                            is_superuser=is_superuser)
    
    @pytest.mark.django_db
    def test_create_superuser(self, user_factory):
        username = "admin@example.com"
        password = "VeryStr0ngPa55word!"
        
        user = user_factory.create_superuser(username=username,
                            password=password)
        assert user.username == username
        assert user.team == "SuperUser"
        assert user.is_admin == True
        assert user.is_superuser == True



