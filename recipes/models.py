from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    process = models.TextField()
    recipe_images = models.ImageField(upload_to='recipe_images/')

    def __str__(self):
        return self.name


# class User(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Use Django's built-in password hashing
#     profile_pic = models.ImageField(upload_to='profile_pics/')
#
#     def __str__(self):
#         return self.username


class MyUserManager(BaseUserManager):
    def create_user(self, email,profile_pic, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
            profile_pic=profile_pic,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=100)
   # date_of_birth = models.DateField()
    profile_pic = models.ImageField(upload_to='profile_pics/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
