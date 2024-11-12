from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True) 
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    address = models.TextField()                                                                 #Username: placeholder_user                                                                                         #Password: temporarypassword
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    def __str__(self):
        return self.name

class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    medicines = models.ManyToManyField(Medicine)
    date_issued = models.DateField(auto_now_add=True)
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True)  # Added field for file upload
    is_approved = models.BooleanField(default=False)  
    def __str__(self):
        return f"Prescription by {self.doctor_name} for {self.customer.name}"

class Sales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=datetime.now)
    payment_method = models.CharField(max_length=50, choices=(('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI')))
    

    def __str__(self):
        return f"Sale {self.id} - {self.customer.name}"
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    else:
        # Check if the user has a Customer profile and create one if not
        if not hasattr(instance, 'customer'):
            Customer.objects.create(user=instance)
        else:
            instance.customer.save()


# Create your models here.
