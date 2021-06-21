from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # additional
    sellerid = models.AutoField(primary_key=True)
    sellertoken = models.CharField(max_length=100)
    sellertitle = models.CharField(max_length=200)
    sellerEmail = models.CharField(max_length=100)
    sellerEmailConfirmed = models.BooleanField(null=True)
    sellerActive = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
class Create(models.Model):
    sellerCreatedBy = models.ForeignKey(UserProfileInfo,on_delete=models.CASCADE)
    sellerCreatedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sellerCreatedOn

class Modify(models.Model):
    sellerModifiedBy = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    sellerModifiedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sellerModifiedOn
