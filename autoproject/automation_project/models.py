from typing import Any
from django.db import models

# Create your models here.
class ScrappedLeads(models.Model):
    query = models.CharField(max_length=100)
    company_name = models.TextField()
    company_location = models.TextField()
    company_number = models.TextField()
    company_email = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.id