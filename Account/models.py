from django.db import models
import uuid
# Account model
class AccountModel(models.Model):
    
    email = models.EmailField(unique=True)
    #using UUID to generate unique account id for each user
    account_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    account_name = models.CharField(max_length=255)
    #secret token to identify user in destination
    app_secret_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.account_name

