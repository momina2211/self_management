import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djstripe.models  import Customer,Account

from users.utils.models import UUIDMODEL


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email of User"), unique=True)
    stripe_customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL,
                                        help_text="The user's Stripe Customer Object object, if it exists")
    stripe_account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL,
                                       help_text="The user's Stripe Account Object object, if it exists")

    def __str__(self):
        return self.email

class Language(UUIDMODEL):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserProfile(UUIDMODEL):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    language=models.ManyToManyField(Language,blank=True)


    def __str__(self):
        return self.user.username








