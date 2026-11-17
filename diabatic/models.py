from django.db import models

class patient(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150,default="default@example.com")
    password = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    blood_group = models.CharField(max_length=150)
    phone = models.CharField(max_length=150, null=True, blank=True)


class patient_result(models.Model):
    u_id = models.CharField(max_length=150)  
    image = models.CharField(max_length=150)
    result = models.CharField(max_length=150)  
    created_at = models.DateTimeField(auto_now_add=True)

class expert_tbl(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    experience = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    status = models.CharField(max_length=150, null=True, blank=True)
    certificate = models.FileField(max_length=255)

class Recommendation(models.Model):
    SEVERITY_CHOICES = [
        ("No DR", "No DR"),
        ("Mild DR", "Mild DR"),
        ("Moderate DR", "Moderate DR"),
        ("Severe DR", "Severe DR"),
    ]
    severity_level = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    diet = models.TextField()
    lifestyle = models.TextField()
    created_by_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class feed_tbl(models.Model):
    message = models.CharField(max_length=150)
    user = models.ForeignKey(patient,on_delete=models.CASCADE,null=True,blank=True)