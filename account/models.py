from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extras):
        if not email:
            raise ValueError("user must have a valid email address")
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extras
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def creat_user(self, email, password, **extras):
        return self._create_user(email, password, False, False, **extras)

    def create_superuser(self, email, password, **extras):
        return self._create_user(email, password, True, True, **extras)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def get_absolute_url(self):
        return "users/%i/" % (self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ConfirmEmailModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=256, unique=True)
