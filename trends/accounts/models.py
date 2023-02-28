from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from trends.common.models import BaseDateTimeModel


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, usertype: str, is_active: bool = True):
        if not email:
            raise ValidationError("Users must have a email")

        if not password:
            raise ValidationError("Users must have a password")

        obj = self.model(email=email)
        obj.set_password(password)
        obj.is_active = is_active
        obj.usertype = usertype

        if usertype in [User.Usertype.NORMAL, User.Usertype.HEAD]:
            obj.is_superuser = False
        elif usertype == User.Usertype.ADMIN:
            obj.is_superuser = True
        else:
            raise ValidationError(f"Invalid usertype -> {usertype}")

        obj.save(using=self._db)
        return obj

    def create_superuser(self, **kwargs):
        return self.create_user(usertype=User.Usertype.ADMIN, **kwargs)


class User(BaseDateTimeModel, AbstractBaseUser, PermissionsMixin):
    class Usertype(models.TextChoices):
        NORMAL = 'N', 'Normal'
        HEAD = 'H', 'Head'
        ADMIN = 'A', 'Admin'

    usertype = models.CharField(max_length=1, choices=Usertype.choices, default=Usertype.NORMAL)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.usertype} {self.email}"

    @property
    def is_staff(self):
        return self.is_superuser

class Profile(models.Model):
    fullname = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, max_length=255)
    about = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user} {self.fullname}"

    @property
    def get_fullname(self):
        if self.fullname:
            return self.fullname

        return f"User {self.user.id}"
