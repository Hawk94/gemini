from gemini.users.models import User
from django.db import models

class SalesforceCredential(models.Model):
    user = models.OneToOneField(User, related_name="salesforce_credentials",
                                    null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_id = models.CharField(max_length=255, null=True, blank=True)
    oauth_id_token = models.CharField(max_length=1200, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    token_type = models.CharField(max_length=255, null=True, blank=True)
