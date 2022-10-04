from django.shortcuts import get_object_or_404 , render , redirect
from .models import Order, OrderDetails, Produit
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from django.utils import timezone
import re
# Create your views here.
def index(request):
    pro = Produit.objects.all()
    name = None
    if 'namesearch' in request.GET:
        name = request.GET['namesearch']
        if name :
            pro = pro.filter(name__icontains=name) 
    context = {
        'products' : pro,
        'name' : name
    }
    return render(request , 'store/index.html' , context)
def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total += sub.prix * sub.quantity
            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total
            }

    return render(request , 'store/cart.html',context)
def test(request):
    return render(request , 'store/test.html')
def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        return redirect('profile')
    else:
        if request.user.id == None: return redirect('index')
        if request.user is not None:
            userprofile = UserProfile.objects.get(user=request.user)
            context = {
                'fname' : request.user.first_name,
                'lname' : request.user.last_name,
                'address':userprofile.address,
                'address2':userprofile.address2,
                'city':userprofile.city,
                'state':userprofile.state,
                'zip':userprofile.zip_number,
                'email' : request.user.email,
                'user' : request.user.username,
                'passord' : request.user.password,
            }
            return render(request , 'store/profile.html',context)
        else:
            return redirect('profile')
        
def signin(request):
    if request.method == 'POST' and 'btnSignin' in request.POST:
        username = request.POST['user']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            #messages.success(request, 'You are now logged in')
        else:
            messages.error(request, 'Username or password invalid')
        return redirect('signin')
    else:
        return render(request , 'store/signin.html')
def checkout(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total += sub.prix * sub.quantity
            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total
            }

    return render(request , 'store/checkout.html',context)
    
def product(request , pro_id):
    context = {
        'pro' : get_object_or_404(Produit, pk=pro_id)
    }
    return render(request , 'store/product.html' , context)
def About(request):
    return render(request , 'store/About.html')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')
def signup(request):
    if request.method == 'POST' and 'btnSibnup' in request.POST:
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None
        zip_number = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None
        if 'fname' in request.POST:
            fname = request.POST['fname']
        else: messages.error(request, 'Error in first name')
        if 'lname' in request.POST:
            lname = request.POST['lname']
        else: messages.error(request, 'Error in last name')
        if 'address' in request.POST:
            address = request.POST['address']
        else: messages.error(request, 'Error in address')
        if 'address2' in request.POST:
            address2 = request.POST['address2']
        else: messages.error(request, 'Error in address 2')
        if 'password' in request.POST:
            password = request.POST['password']
        else: messages.error(request, 'Error in password')
        if 'city' in request.POST:
            city = request.POST['city']
        else: messages.error(request, 'Error in city')
        if 'state' in request.POST:
            state = request.POST['state']
        else: messages.error(request, 'Error in state')
        if 'zip' in request.POST:
            zip_number= request.POST['zip']
        else: messages.error(request, 'Error in zip')
        if 'email' in request.POST:
            email = request.POST['email']
        else: messages.error(request, 'Error in email')
        if 'user' in request.POST:
            username = request.POST['user']
        else: messages.error(request, 'Error in username')
        if 'terms' in request.POST:
            terms = request.POST['terms']
        if fname and lname and address and address2 and city and state and zip_number and email and username and password:
            if terms == 'on':
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This usename is taken')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        patt = "^\w+([-+.'])*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt, email):
                            # add user
                            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=password)
                            user.save()
                            # add user profille
                            userprofile = UserProfile(user=user, address=address, address2=address2, city=city, state=state, zip_number=zip_number)
                            userprofile.save()
                            # success message
                            messages.success(request, 'Your account is created')
                            fname = ''
                            lname = ''
                            address = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip_number = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None
                            is_added = True
                        else:
                            messages.error(request, 'Invalide Email')
            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'check empty fields')

        return render(request , 'store/signup.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'zip':zip_number,
            'city':city,
            'state':state,
            'user':username,
            'password':password,
            'email':email,
            'is_added':is_added
        })
    else:
        return render(request , 'store/signup.html')
def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Produit.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user ,product_favorites=pro_fav).exists():
            messages.success(request,"Already product in the favorite list")
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request,'Product has been favorited')
       # return redirect('/'+str(pro_id))
        
    else:
        messages.error(request,'Your must be logged in')
    return redirect('/'+str(pro_id))
def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context={
            'products':pro
        }
    return render(request,'store/index.html',context)
def add_to_cart(request):
    if 'pro_id' in request.GET and 'qty' in request.GET and 'prix' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        order = Order.objects.all().filter(user=request.user,is_finished=False)
        # if Produit.objects.all().filter(id=pro_id).exists():
        #     return redirect('index')
        pro = Produit.objects.get(id=pro_id)
        if order:
            messages.success(request,'Was added to cart for old order')
            old_order = Order.objects.get(user=request.user,is_finished=False)
            orderdetails = OrderDetails.objects.create(product=pro,order=old_order,prix=pro.prix,quantity=qty)
        else:
            messages.success(request,'Was added to cart new order')
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            orderdetails = OrderDetails.objects.create(product=pro,order=new_order,prix=pro.prix,quantity=qty)
        return redirect('/'+request.GET['pro_id'])
    else:
        # if 'pro_id' in request.GET:
        #     messages.error(redirect,"You must be logged in")
        #     return redirect('/'+request.GET['pro_id'])
        # else:

        return redirect('signin')
def remove_from_cart(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.delete()
    return redirect('cart')
def add_qty(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.quantity +=1
        orderdetails.save()
    return redirect('cart')
def sub_qty(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity>1: 
            orderdetails.quantity -=1
            orderdetails.save()
        else: orderdetails.delete()
    return redirect('cart')
