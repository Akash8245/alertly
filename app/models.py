from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name="Full Name")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    pin_code = models.CharField(max_length=6, verbose_name="Pin Code")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']  

    def __str__(self):
        return self.name

class Disaster(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField()  
    pin_code = models.CharField(max_length=10)  
    date = models.DateTimeField(auto_now_add=True)  
    severity = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]) 

    def __str__(self):
        return f"{self.name} - {self.pin_code}"