from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError("Users must have an email")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(
        max_length=100, unique=True, default='user name', primary_key=True)
    first_name = models.CharField(max_length=100, default='first name')
    last_name = models.CharField(max_length=100, default='last name')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserAccountManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    USER_ROLES = [
        ('Candidate', 'Candidate'),
        ('Employer', 'Employer'),
    ]

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='location')
    city = models.CharField(max_length=100, default='City')
    country = models.CharField(max_length=100, default='Country')
    date_of_birth = models.DateField(default=datetime.now)
    role = models.CharField(
        max_length=20, choices=USER_ROLES, default='Candidate')

    bio = models.TextField()
    # profile_picture = models.ImageField(upload_to='profile_pictures/')
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    company = models.CharField(blank=True)
    industry = models.TextField(blank=True)
    job_title = models.CharField(blank=True)
    company_location = models.TextField(blank=True)

    def __str__(self):
        return f"Email: {self.user.get_username()} \nName: {self.user.get_full_name()}"
