from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    db_name = models.CharField(max_length=255)
    db_user = models.CharField(max_length=255)
    db_password = models.CharField(max_length=255)
    db_host = models.CharField(max_length=255)
    db_port = models.CharField(max_length=5)

    def __str__(self):
        return self.name
