
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Produit(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6 , decimal_places=2)
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d/')
    public_date = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    # class Meta:
    #     ordering = ['public_date']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_favorites = models.ManyToManyField(Produit)
    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zip_number = models.CharField(max_length=6)
    def __str__(self):
        return self.user.username
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Produit, through='OrderDetails')
    is_finished = models.BooleanField() 
    def __str__(self):
        return 'User: ' + self.user.username + ', Order id: '+ str(self.id)
class OrderDetails(models.Model):
    product = models.ForeignKey(Produit,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=6 , decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'User: '+ self.order.user.username +', Product' + self.product.name+', Order id: ' + str(self.order.id)
    class Meta:
        ordering = ['id']