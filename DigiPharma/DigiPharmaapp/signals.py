from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    else:
        if not hasattr(instance, 'customer'):
            Customer.objects.create(user=instance)
        else:
            instance.customer.save()
