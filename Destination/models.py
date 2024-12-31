from django.db import models
from Account.models import AccountModel
# Create your models here.
class DestinationModel(models.Model):
    account = models.ForeignKey(AccountModel, related_name="destinations", on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')], max_length=10)
    #header for destiantion, jsonfield is not used since it is not available in some version of sqlite
    app_id = models.CharField(max_length=200)
    app_sectet = models.UUIDField()
    content_type = models.CharField(max_length=200)
    accept = models.CharField(max_length=200)
    def __str__(self):
        return self.account.account_name