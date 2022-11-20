from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self,
                    username: str,
                    password: str,
                    usertype: str,
                    email: str,
                    is_active: bool = True):
        if not username:
            raise ValidationError("Users must have a username")

        if not password:
            raise ValidationError("Users must have a password")

        if not email:
            raise ValidationError("Users must have a email")

        obj = self.model(username=username)
        obj.set_password(password)
        obj.email = email
        obj.is_active = is_active
        obj.usertype = usertype

        if usertype in [User.Usertype.NORMAL, User.Usertype.HEAD]:
            obj.is_superuser = False
            obj.is_staff = False
        elif usertype == User.Usertype.ADMIN:
            obj.is_superuser = True
            obj.is_staff = True
        else:
            raise ValidationError(f"Invalid usertype -> {usertype}")

        obj.save(using=self._db)
        return obj

    def create_superuser(self, **kwargs):
        return self.create_user(usertype=User.Usertype.ADMIN, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):

    class Usertype(models.TextChoices):
        NORMAL = 'N', 'Normal'
        HEAD = 'H', 'Head'
        ADMIN = 'A', 'Admin'

    usertype = models.CharField(max_length=1,
                                choices=Usertype.choices,
                                default=Usertype.NORMAL)
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
