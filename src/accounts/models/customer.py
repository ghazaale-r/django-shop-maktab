from django.core.validators import (MaxLengthValidator,
                                    MinLengthValidator)
from django.db import models

from .custom_user import User, UserManager

class CustomerManager(UserManager):
    def create_customer(self, email, password, **extra_fields):
        extra_fields.setdefault('is_customer', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return super().create_user(email, password, **extra_fields)
    
    
class Customer(User):
    objects = CustomerManager()
    address = models.ManyToManyField('Address', through='CustomerAddress', related_name='customer_address')

    class Meta:
        verbose_name="مشتری"
        verbose_name_plural = 'مشتری ها' 
        
    def save(self,*args, **kwargs):
        if not self.id:
            self.is_staff = False
            self.is_superuser = False
            self.is_customer = True
        return super(Customer,self).save(*args,**kwargs)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False

class CustomerAddress(models.Model):
    main_address = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, related_name='customer_related')
    address = models.ForeignKey('Address', on_delete=models.SET_NULL , null=True,related_name='address_related')

    class Meta:
        verbose_name = "آدرس مشتری"
        verbose_name_plural = "آدرس مشتریان"
        
    def __str__(self) -> str:
        return f"{self.customer}-address"



class Address(models.Model):
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10, blank=True,
                               validators=[
                                   MinLengthValidator(10),
                                    MaxLengthValidator(10)
                               ])

    def __str__(self):
        return f"{self.state}, {self.city}, {self.street}"
    

from django.db.models.signals import post_save
from .custom_user import save_profile

# Connect the signal manually
post_save.connect(save_profile, sender=Customer)