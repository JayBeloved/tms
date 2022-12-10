from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.

# Create variables to store user types
SUPER_ADMIN = 1
AGENT = 2

USERTYPE_CHOICES = (
    (SUPER_ADMIN, 'Administrator'),
    (AGENT, 'Agent'),
)


class User(AbstractUser):
    # Add User type
    user_type = models.PositiveSmallIntegerField(choices=USERTYPE_CHOICES, default=AGENT)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'user_type']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_prof1.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 400 or img.width > 400:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

