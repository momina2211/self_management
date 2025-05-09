from django.db import models
import uuid

class UUIDMODEL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Created_at =models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract =True