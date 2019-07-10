from django.contrib.auth.models import User
from django.db import models
from PIL import Image


# region UserInformation model not for use just for testing
# class ModelUserInformation(models.Model):
#     userName = models.CharField(max_length=50)
#     country_code = models.CharField(max_length=4)
#     mobile = models.CharField(max_length=10)
#     email = models.CharField(max_length=50)
#     address = models.TextField()
#     gender = models.BooleanField()
#     dob = models.DateTimeField()
#
#     def __str__(self):
#         return self.title
# endregion

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
