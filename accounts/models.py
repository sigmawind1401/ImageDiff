from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

class UserSession(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
