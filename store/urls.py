from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index , name = 'index'),
    path('cart/' , views.cart , name = 'cart'),
    path('checkout/' , views.checkout , name = 'checkout'),
    path('About/' , views.About, name = 'about'),
    path('signin/' , views.signin, name = 'signin'),
    path('signup/' , views.signup, name = 'signup'),
    path('product_favorite/<int:pro_id>', views.product_favorite,name='product_favorite'),
    path('logout/' , views.logout, name = 'logout'),
    path('profile/' , views.profile, name = 'profile'),
    path('add_qty/<int:orderdetails_id>' , views.add_qty, name = 'add_qty'),
    path('sub_qty/<int:orderdetails_id>' , views.sub_qty, name = 'sub_qty'),
    path('add_to_cart/' , views.add_to_cart, name = 'add_to_cart'),
    path('test/' , views.test, name = 'test'),
    path('remove_from_cart/<int:orderdetails_id>/' , views.remove_from_cart, name = 'remove_from_cart'),
    path('show_product_favorite',views.show_product_favorite,name='show_product_favorite'),
    path('<int:pro_id>/' , views.product , name = 'product')
]