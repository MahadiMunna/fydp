from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='./profile-images/uploads/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"