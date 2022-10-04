from django.contrib import admin
from .models import Produit
from .models import UserProfile
from .models import Order
from .models import OrderDetails
# Register your models here.
admin.site.register(Produit)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderDetails)
