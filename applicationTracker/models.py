from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ("Applied", "Applied"),
    ("Interview", "Interview"),
    ("Offer", "Offer"),
    ("Rejected", "Rejected"),
]

# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(
        max_length=100,
        verbose_name="Company"
        )
    title = models.CharField(
        max_length=150,
        verbose_name="Position Title"
        )
    applicationStatus = models.CharField(
        choices=STATUS_CHOICES, 
        default="Applied",
        verbose_name="Application Status"
        )
    dateApplied = models.DateField(
        verbose_name="Date Applied"
        )
    link = models.URLField(
        blank=True, 
        null=True,
        verbose_name="Link to Application"
        )
    domain = models.CharField(blank=True, null=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.company}"