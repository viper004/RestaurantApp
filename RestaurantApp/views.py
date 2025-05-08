from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone
from .forms import *
from .models import *
from itertools import chain
from operator import attrgetter

# Create your views here.

def index(request):
    return render(request,'index.html')

def admin(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    a=Restaurants.objects.all().count()
    b=Staffs.objects.all().count()
    return render(request, 'home-pages/admin_home.html',{'a':a,'b':b})

def login(request):
    return render(request,'login.html')

def user_register(request):
    if request.method=='POST':
        form=user_form(request.POST)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=1
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,"Form successfully submitted")
            return redirect('login')
    else:
            form=user_form()
            login=login_form()

    return render(request, 'registration-pages/user_register.html',{'form':form,'login':login})

def admin_user_view(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    a = Users.objects.all()
    return render(request, 'admin-account-view/admin_user_view.html',{'data':a})

def login_action(request):
    if request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = Login.objects.filter(email=email).first()
            if user is not None:
                if user.password == password:
                    if user.usertype == 1:
                        request.session['user_id'] = user.id
                        return redirect('user_home')
                    elif user.usertype == 2:
                        resstaurant = get_object_or_404(Restaurants, login_id=user.id)
                        request.session['restaurant_id'] = user.id
                        if resstaurant.have_certificate == 0:
                            return render(request, 'no_certificate.html', {'data': resstaurant})
                        if resstaurant.department_approved == 0 or resstaurant.approval_status == 0:
                            return render(request, 'home-pages/pending_restaurant_home.html')
                        if resstaurant.approval_status == 2:
                            return render(request, 'home-pages/freezed_Restaurant_home.html')
                        return redirect('restaurant_home')
                    elif user.usertype == 3:
                        request.session['staff_id'] = user.id
                        return redirect('staff_home')
                    elif user.usertype == 4:
                        request.session['department_id'] = user.id
                        return redirect('department_home')
                    elif user.usertype==5:
                        request.session['admin_id']=user.id
                        return redirect('adminpage')
                else:
                    messages.error(request, 'Incorrect Password')
            else:
                messages.error(request, 'User Does Not Exist')
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})


def user_home(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    login_details=get_object_or_404(Login,id=user_id)
    user_details=get_object_or_404(Users,login_id=login_details)
    return render(request,'home-pages/user_home.html',{'details':user_details})

def restaurant_home(request):
    restaurant_id=request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('index')
    res=Restaurants.objects.get(login_id=restaurant_id)
    return render(request,'home-pages/restaurant_home.html',{'details':res})

def staff_home(request):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    return render(request,'home-pages/staff_home.html')

def department_home(request):
    department_id=request.session.get('department_id')
    if not department_id:
        return redirect('index')
    return render(request,'home-pages/department_home.html')

def user_profile(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    login_details=get_object_or_404(Login,id=user_id)
    data=get_object_or_404(Users,login_id=user_id)
    if request.method=='POST':
        form=edit_user(request.POST,instance=data)
        form2=login_form(request.POST,instance=login_details)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('user_home')
    else:
        form=edit_user(instance=data)
        form2=login_form(instance=login_details)
    return render(request,'user_profile_edit.html',{'form':form,'form2':form2})

def restaurant_profile(request):
    restaurant_id = request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('index')
    login_details = get_object_or_404(Login, id=restaurant_id)
    data = get_object_or_404(Restaurants, login_id=restaurant_id)

    if request.method == 'POST':
        form=restaurant_form(request.POST,instance=data)
        form2=login_form(request.POST,instance=login_details)
        if form.is_valid() and form2.is_valid():

        # update fields manually
        # data.category = request.POST.get('category')
        # data.name = request.POST.get('name')
        # data.address = request.POST.get('address')
        # data.district = request.POST.get('district')
        # data.city = request.POST.get('city')
        # data.contact = request.POST.get('contact')
            data.have_certificate = int(request.POST.get('have_certificate'))
            print (data.have_certificate)
            data.fssai_nunmber = request.POST.get('fssai_nunmber')
            print (data.fssai_nunmber)
            data.save()

        # login_details.username = request.POST.get('username')
        # login_details.email = request.POST.get('email')
        # login_details.save()
        return redirect('restaurant_home')
    else:
        form=restaurant_form(instance=data)
        form2=login_form(instance=login_details)
    
    return render(request, 'restaurant_profile_edit.html', {
        'data': data,
        'login_details': login_details,
        'form':form,
        'form2':form2
    })

def restaurant_profile_update(request,id):
    res=request.session.get('restaurant_id')
    if not res:
        return redirect('index')
    restaurant=Restaurants.objects.get(id=id)

    return redirect('restaurant_profile')

def have_certificate_yes(request,id):
    restaurant=get_object_or_404(Restaurants,id=id)
    restaurant.have_certificate=1
    restaurant.save()

def restaurant_registration(request):
    if request.method=='POST':
        form=restaurant_form(request.POST,request.FILES)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=2
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,"Form successfully submitted")
            return redirect('index')
            have_certificate=request.POST.get('have_certificate')
            fssai_license=request.POST.get('fssai_license')
            Restaurants.objects.create(
                have_certificate=have_certificate,
                fssai_license=fssai_license
            )
    else:
            form=restaurant_form()
            login=login_form()

    return render(request,'registration-pages/restaurant_registration.html',{'form':form,'login':login})

def staff_profile(request):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    login_details=get_object_or_404(Login,id=staff_id)
    data=get_object_or_404(Staffs,login_id=staff_id)
    if request.method=='POST':
        form=edit_user(request.POST,instance=data)
        form2=login_form(request.POST,instance=login_details)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('staff_home')
    else:
        form=edit_user(instance=data)
        form2=login_form(instance=login_details)
    return render(request,'staff_profile_edit.html',{'form':form,'form2':form2})

def staff_registration(request):
    restaurant_id = request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('index')
    res_id = get_object_or_404(Restaurants,login_id=restaurant_id)
    if request.method=='POST':
        form=staff_form(request.POST,request.FILES)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=3
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.restaurant_name=res_id
            b.save()
            
            messages.success(request,"Form successfully submitted")
            return redirect('index')
    else:
            form=staff_form()
            login=login_form()

    return render(request,'registration-pages/staff_registration.html',{'form':form,'login':login})

def food_and_safety_department_registration(request):
    dept=request.session.get('department_id')
    if not dept:
        return redirect('index')
    if request.method=='POST':
        form=food_and_safety_department_form(request.POST,request.FILES)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=4
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,"Form successfully submitted")
            return redirect('index')
    else:
            form=food_and_safety_department_form()
            login=login_form()

    return render(request,'registration-pages/food_and_safety_registration.html',{'form':form,'login':login})

def admin_view_pending_restaurant(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    data=Restaurants.objects.filter(approval_status = 0 , department_approved = 1)
    return render(request,'admin-account-view/admin_view_pending_restaurant.html',{'a':data})

def admin_approve_restaurant(request,id):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    restaurant=get_object_or_404(Restaurants,id=id)
    restaurant.approval_status=1
    restaurant.save()
    return redirect('admin_view_pending_restaurant')

def admin_reject_restaurant(request,id):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    restaurant=get_object_or_404(Restaurants,id=id)
    b=restaurant.login_id
    restaurant.delete()
    if b:
        b.delete()
    return redirect('admin_view_pending_restaurant')

def admin_freeze_restaurant(request,id):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    restaurant=get_object_or_404(Restaurants,id=id)
    restaurant.approval_status=2
    restaurant.save()
    return redirect('admin_restaurant_view')

def admin_view_freezed_restaurants(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    data=Restaurants.objects.filter(approval_status=2)
    return render(request,'admin-account-view/admin_view_freezed_restaurants.html',{'a':data})


def admin_restaurant_view(request):
     admin_id=request.session.get('admin_id')
     if not admin_id:
        return redirect('index')
     data=Restaurants.objects.filter(approval_status=1)
     return render(request,'admin-account-view/admin_restaurant_view.html',{'a':data})

def admin_staff_view(request):
     admin_id=request.session.get('admin_id')
     if not admin_id:
        return redirect('index')
     data=Staffs.objects.all()
     return render(request,'admin-account-view/admin_staff_view.html',{'a':data})

def restaurant_cards(request):
    user = request.session.get('user_id')
    if not user:
        return redirect('index')

    query = request.GET.get('q')
    if query:
        restaurants = Restaurants.objects.filter(name__icontains=query, approval_status=1)
    else:
        restaurants = Restaurants.objects.filter(approval_status=1)

    return render(request, 'restaurant_cards.html', {'restaurants': restaurants})


def staff_cards(request):
    res_id=request.session.get('restaurant_id')
    if not res_id:
        return redirect('index')
    login_details=get_object_or_404(Login,id=res_id)
    data=get_object_or_404(Restaurants,login_id=login_details)
    staffs=Staffs.objects.filter(restaurant_name=data)
    print("data....",staffs)
    return render(request,'staff_cards.html',{'staffs':staffs})

def add_dish(request):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    login_details = get_object_or_404(Login, id=staff_id)
    data = get_object_or_404(Staffs, login_id=login_details)
    if request.method == 'POST':
        form = dishes_form(request.POST, request.FILES) 
        if form.is_valid():
            dish = form.save(commit=False)
            dish.login_id = data 
            dish.save()
            messages.success(request, "Form successfully submitted")
            return redirect('staff_home')
    else:
        form = dishes_form()

    return render(request, 'dishes/add_dish.html', {'form': form})

def restaurant_dish_view(request):
    user_login = request.session.get('restaurant_id')
    if not user_login:
        return redirect('index')
    print(user_login)
    restaurant = get_object_or_404(Restaurants,login_id=user_login)
    dishes = Dishes.objects.filter(login_id__restaurant_name=restaurant)
    
    
    return render(request, 'restaurant_dish_view.html', {'dishes': dishes})

def user_restaurant_view(request,id):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    user=get_object_or_404(Users,login_id=user_id)
    log_details=get_object_or_404(Login,id=user_id)
    details=get_object_or_404(Restaurants,id=id)
    dishes=Dishes.objects.filter(login_id__restaurant_name=details,status=1)
    reviews=Reviews.objects.filter(restaurant_id=id)
    if request.method=='POST':
        form=user_complaint(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.restaurant_id=details
            a.user_id=user
            a.save()

    return render(request,'user_restaurant_view.html',{'details':details,'dishes':dishes,'user':user,'login':log_details,'reviews':reviews,'id':id})

def staff_dish_view(request):
    staff=request.session.get('staff_id')
    if not staff:
        return redirect('index')
    login_details=Staffs.objects.get(login_id=staff)
    dishes=Dishes.objects.filter(login_id=login_details)
    return render(request,'staff_dish_view.html',{'dishes':dishes})

def staff_dish_edit(request,id):
    staff=request.session.get('staff_id')
    if not staff:
        return redirect('index')
    data=get_object_or_404(Dishes,id=id)
    if request.method=='POST':
        form=dishes_form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        return redirect('staff_home')
    else:
        form=dishes_form(instance=data)
    return render(request,'staff_dish_edit.html',{'dishes':form})

def dish_remove(request,id):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    dishes=get_object_or_404(Dishes,id=id)
    dishes.delete()
    return redirect('staff_dish_view')

def add_to_menu(request,id):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    dishes=get_object_or_404(Dishes,id=id)
    dishes.status=1
    dishes.save()
    return redirect('staff_menu')


def staff_menu_view(request):
    staff_id = request.session.get('staff_id') 
    if not staff_id:
        return redirect('index')
    login_details = get_object_or_404(Login, id=staff_id)  
    staff = get_object_or_404(Staffs, login_id=login_details) 
    dishes = Dishes.objects.filter(login_id=staff, status=1)
    return render(request, 'staff_menu_view.html', {'dishes': dishes})


def menu_item_remove(request,id):
    staff_id = request.session.get('staff_id') 
    if not staff_id:
        return redirect('index')
    dishes=get_object_or_404(Dishes,id=id)
    dishes.status=0
    dishes.save()
    return redirect('staff_menu')


def add_to_cart(request, restaurant_id, product_id):
    user=request.session.get('user_id')
    if not user:
        return redirect('index')
    log_details=get_object_or_404(Users,login_id=user)
    restaurant = get_object_or_404(Restaurants,id=restaurant_id)
    quantity = int(request.POST.get('quantity', 1))
    print(quantity)
    product = Dishes.objects.get(id=product_id)
    UserCart.objects.create(
        user_id=log_details,
        restaurant_loginid=restaurant,
        product_id=product,
        quantity=quantity
    )
    return redirect('user_cart_view')
    # return JsonResponse({"message": "Product added to cart successfully!"})


def user_cart_view(request):
    user=request.session.get('user_id')
    if not user:
        return redirect('index')
    log_details=get_object_or_404(Users,login_id=user)
    product=UserCart.objects.filter(user_id=log_details,payment_status=0).exclude(remove_status=1)
    return render(request,'user_cart.html',{'products':product})

def cart_item_remove(request,id):
    a=UserCart.objects.get(id=id)
    a.remove_status=1
    a.save()
    return redirect('user_cart_view')

from django.http import JsonResponse


def payment_forms(request, id):
    total_price = request.GET.get('total_price', 0) 
    try:
        total_price = int(float(total_price)) 
    except ValueError:
        total_price = 0  # Default to 0 if conversion fails

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv_code = request.POST.get('cvv_code')
        owner_name = request.POST.get('owner_name')

        # Save payment details
        payment = PaymentDetails.objects.create(
            card_number=card_number,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv_code=cvv_code,
            owner_name=owner_name,
            amount=total_price,
            cart_id=id,
            upi=False,
            upi_id=None
        )

        # Update payment status in UserCart
        cart_items = UserCart.objects.filter(cartid=id)
        for cart in cart_items:
            cart.payment_status = 1
            cart.save()


        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True})

        return redirect('user_cart_view')

    return render(request, 'payment_form.html', {'total_price': total_price})

def upi_payment(request,id):
    total_price=request.POST.get('total_price',0)
    upi_id=request.POST.get('upi_id')
    try:
        total_price = int(float(total_price)) 
    except ValueError:
        total_price = 0  
    if request.method=='POST':
        payment = PaymentDetails.objects.create(
            card_number=None,
            expiry_month=None,
            expiry_year=None,
            cvv_code=None,
            owner_name=None,
            amount=total_price,
            cart_id=id,
            upi=True,
            upi_id=upi_id,
            pickup=False
        )
        cart_items = UserCart.objects.filter(cartid=id)
        for cart in cart_items:
            cart.payment_status = 1
            cart.cancel_status=0
            cart.save()
        return redirect('user_order_view')

    return render(request,'upi_payment_form.html')

def pay_at_pickup(request,id):
    total_price = request.GET.get('total_price', 0)
    print(total_price)
    try:
        total_price = int(float(total_price)) 
    except ValueError:
        total_price = 0  
    if request.method=='GET':
        payment = PaymentDetails.objects.create(
                card_number=None,
                expiry_month=None,
                expiry_year=None,
                cvv_code=None,
                owner_name=None,
                amount=total_price,
                cart_id=id,
                upi=False,
                upi_id=False,
                pickup=True
            )
        payment.save()
        print(payment)
        cart_items = UserCart.objects.filter(cartid=id)
        for cart in cart_items:
            cart.payment_status = 1
            cart.cancel_status=0
            print(cart)
            cart.save()
    return redirect('user_order_view')


def user_order_view(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    log_details=get_object_or_404(Users,login_id=user_id)
    user_cart=UserCart.objects.filter(user_id=log_details,payment_status=1).exclude(cancel_status=1)
    return render(request,'user_order_view.html',{'details':user_cart})

def user_cancel_order(request,id):
    cart=UserCart.objects.get(id=id)
    print(cart)
    cart.cancel_status=1
    cart.save()
    return redirect('user_order_view')

def restaurant_order_view(request):
    res_id=request.session.get('restaurant_id')
    log_details=get_object_or_404(Restaurants,login_id=res_id)
    orders=UserCart.objects.filter(restaurant_loginid=log_details,payment_status=1).select_related('user_id__login_id').order_by('current_time')
    return render(request,'restaurant_order_view.html',{'details':orders})

def user_restaurant_chat(request,id):
    usr=request.session.get('user_id')
    if not usr:
        return redirect('index')
    user=get_object_or_404(Users,login_id=usr)
    restaurant_details=get_object_or_404(Restaurants,id=id)
    # user_sender=Chat.objects.filter(user_sender_id=user,restaurant_reciever_id=restaurant_details)
    # restaurant_reciever=Chat.objects.filter(restaurant_sender_id=restaurant_details, user_receiver_id=user)
    if request.method=='POST':
        form=messages_form(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.user_sender_id=user
            f.restaurant_reciever_id=restaurant_details
            # f.user_reciever_id=None
            f.save()
            return redirect('user_restaurant_chat',id=id)
    else:
        form=messages_form()
        send_messages=Chat.objects.filter(user_sender_id=user, restaurant_reciever_id=restaurant_details)
        recieved_messages=Chat.objects.filter(restaurant_sender_id=restaurant_details,user_reciever_id=user)

        messages=sorted(chain(send_messages,recieved_messages),key=attrgetter('date_and_time'))
        texts={
            "messages":messages,
            "user_sender_id":user,
            "restaurant_reciever_id":restaurant_details,
            "form":form,
            
        }
    return render(request,'user_restaurant_chat.html',texts)

def restaurant_chat_list_view(request):
    res_id=request.session.get('restaurant_id')  
    if not res_id:
        return redirect('index')
    restaurant=get_object_or_404(Restaurants,login_id=res_id)
    res=Chat.objects.filter(restaurant_reciever_id=restaurant)
    print(res)
    user = Chat.objects.filter(restaurant_reciever_id=restaurant).values_list('user_sender_id__name','user_sender_id__id',flat=False).distinct()

    return render(request,'restaurant_chat_list_view.html',{'res':user})

def restaurant_user_chat(request,id):
    res=request.session.get('restaurant_id')
    if not res:
        return render ('index')
    restaurant=get_object_or_404(Restaurants,login_id=res)
    user=Users.objects.get(id=id)
    if request.method=='POST':
        form=messages_form(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.restaurant_sender_id=restaurant
            f.user_reciever_id=user
            f.save()
            return redirect('restaurant_user_chat',id=id)
    else:
        form=messages_form()
        send_messages=Chat.objects.filter(restaurant_sender_id=restaurant, user_reciever_id=user)
        recieved_messages=Chat.objects.filter(user_sender_id=user,restaurant_reciever_id=restaurant)
        messages=sorted(chain(send_messages,recieved_messages),key=attrgetter('date_and_time'))
        texts={
            "messages":messages,
            "restaurant_sender_id":restaurant,
            "user_reciever_id":user,
            "form":form,
            
        }
    return render(request,'restaurant_user_chat.html',texts)

def table_reservation(request,id):
    user_id=request.session.get('user_id')
    user=get_object_or_404(Users,login_id=user_id)
    res=get_object_or_404(Restaurants,id=id)
    form=table_reservation_form(request.POST)

    if request.method=='POST':
        rdate=request.POST.get('rdate')

        rtime=request.POST.get('rtime')
        number_of_people=request.POST.get('number_of_people')
        notes=request.POST.get('notes')

        a=Table.objects.create(
            rdate=rdate,
            rtime=rtime,
            notes=notes,
            number_of_people=number_of_people,
            user_id=user,
            restaurant_id=res
        )
    return redirect('user_home')

def restaurant_reservation_view(request):
    res_id=request.session.get('restaurant_id')
    if not res_id:
        return redirect('index')
    reservation=get_object_or_404(Restaurants,login_id=res_id)
    reservations = Table.objects.filter(restaurant_id=reservation).order_by('-rdate', '-rtime')
    return render(request,'restaraunt_reservation_view.html',{'details':reservations})

def staff_reservation_view(request):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    current_date = timezone.now().date() 
    staff=get_object_or_404(Staffs,login_id=staff_id)
    reservations=Table.objects.filter(restaurant_id=staff.restaurant_name,rdate=current_date).order_by('-rtime')
    return render(request,'staff_reservation_view.html',{'details':reservations})

def staff_order_view(request):
    staff_id=request.session.get('staff_id')
    staff=get_object_or_404(Staffs,login_id=staff_id)
    current_date=timezone.now().date()
    orders=UserCart.objects.filter(restaurant_loginid=staff.restaurant_name,current_date = current_date,payment_status=1,cancel_status=0)
    return render(request,'staff_order_view.html',{'details':orders})

def order_ready(request,id):
    a=get_object_or_404(UserCart,id=id)
    a.order_status=1
    a.save()
    return redirect('staff_order_view')

def user_reservation_view(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    user=get_object_or_404(Users,login_id=user_id)
    reservations=Table.objects.filter(user_id=user).order_by('-rdate', '-rtime')
    print(reservations)
    return render(request,'user_reservation_view.html',{'details':reservations})


def user_write_review(request, id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(Users, login_id=user_id)
    restaurant = get_object_or_404(Restaurants, id=id)

    if request.method == 'POST':
        review = request.POST.get('review')  
        image = request.FILES.get('images') 
        star=request.POST.get('star') 
        Reviews.objects.create(
            user_id=user,
            restaurant_id=restaurant,
            star=star,
            review=review,
            images=image
        )
        return redirect('user_home')
    return render(request, 'user_review.html', {'user': user, 'restaurant': restaurant})

def user_review_view(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    user=get_object_or_404(Users,login_id=user_id)
    reviews=Reviews.objects.filter(user_id=user).order_by('-current_date')
    return render(request,'user_review_view.html',{'details':reviews})

def user_edit_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    user_id=request.session.get('user_id')
    user=get_object_or_404(Users,login_id=user_id)
    if request.method == "POST":
        form = user_review(request.POST or None, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = user_review(instance=review)
    return render(request, 'user_review_edit.html', {'form': form, 'data': review, 'user_data':user})

def user_delete_review(request,id):
    review=get_object_or_404(Reviews,id=id)
    review.delete()
    return redirect('user_review_view')

def admin_remove_user(request,id):
    a=get_object_or_404(Users,id=id)
    b=a.login_id
    a.delete()
    if b:
        b.delete()
    return redirect('admin_user_view')

def admin_remove_restuurant(request,id):
    a=get_object_or_404(Restaurants,id=id)
    b=a.login_id
    a.delete()
    if b:
        b.delete()
    return redirect('admin_restaurant_view')

def admin_remove_staff(request,id):
    a=get_object_or_404(Staffs,id=id)
    b=a.login_id
    a.delete()
    if b:
        b.delete()
    return redirect('admin_staff_view')

def user_report_restaurant(request,id):
    user_id=request.session.get('user_id')
    user=get_object_or_404(Users,login_id=user_id)
    restaurant=get_object_or_404(Restaurants,id=id)
    if request.method=='POST':
        text=request.POST.get('text')
        UserReports.objects.create(
            user_id=user,
            restuarant_id=restaurant,
            text=text
        )
    return render(request,'report_to_admin.html',{'restaurant':restaurant})

def admin_view_user_report(request):
    reports=UserReports.objects.filter(forward_to_dept=0)
    return render(request,'admin_report_view.html',{'data':reports})

def view_ratings(request,id):
    reviews=Reviews.objects.filter(restaurant_id=id)
    restaurant=get_object_or_404(Restaurants,id=id)
    return render(request,'user_view_ratings.html',{'reviews':reviews,'restaurant':restaurant})


def logout_view(request):
    request.session.flush()
    return redirect('index')

# from django.views.decorators.csrf import csrf_exempt
import json
# @csrf_exempt  # Only use this if you can't include CSRF token properly, otherwise remove it

def update_cart_quantities(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantities = data.get("quantities", {})

        for cart_item_id, qty in quantities.items():
            try:
                cart_item = UserCart.objects.get(id=cart_item_id)
                cart_item.quantity = int(qty)
                cart_item.save()
            except UserCart.DoesNotExist:
                continue

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid'}, status=400)

def restaurant_document_upload(request):
    return render(request,'restaurant_document_upload.html')

def announcements(request):
    if request.method=='POST':
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        Announcements.objects.create(
            subject=subject,
            message=message
        )
    return render(request,"dept_announcement.html")

def view_announcements(request):
    announcements=Announcements.objects.all().order_by('-current_date', '-current_time')
    return render(request,'view_announcements.html',{'announcements':announcements})

def restaurant_view_announcement(request):
    restaurant_id=request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('index')
    announcements=Announcements.objects.all().order_by('-current_date', '-current_time')
    return render(request,'restaurant_view_announcement.html',{'announcements':announcements})

def certificate_application(request):
    res_id=request.session.get('restaurant_id')
    if not res_id:
        return redirect('index')
    if request.method=='POST':
        res=request.session.get('restaurant_id')
        restaurant=get_object_or_404(Restaurants,login_id=res)
        name=request.POST.get('restaurant_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        district=request.POST.get('district')
        validity=request.POST.get('validity')
        mobile=request.POST.get('mobile')
        tel=request.POST.get('telephone')
        email=request.POST.get('email')
        a=Certificate_Application.objects.create(
            res_id=restaurant,
            name=name,
            address=address,
            district=district,
            validity=validity,
            mobile=mobile,
            tel=tel,
            email=email 
        )
        print (a)
        return JsonResponse({'success': True})
    return render(request,'certificate_application.html')
    
def view_certificate_applications(request):
    applications=Certificate_Application.objects.all().order_by('current_date')
    return render(request,'view_certificate_applications.html',{'applications':applications})

def department_view_pending_restaurant(request):
    res=Restaurants.objects.filter(department_approved='0')
    return render(request,'department_view_pending_restaurant.html',{'data':res})

def department_approve(request,id):
    res=Restaurants.objects.get(id=id)
    res.department_approved=1
    res.save()
    return redirect('department_view_pending_restaurant')

def department_delete(request,id):
    res=Restaurants.objects.filter(id=id)
    res.delete()
    return redirect('department_view_pending_restaurant')

def view_full_application(request,id):
    application=Certificate_Application.objects.get(id=id)
    return render(request,'view_full_application.html',{'application':application})

def delete_application(request,id):
    application=Certificate_Application.objects.get(id=id)
    application.delete()
    return redirect('view_certificate_applications')
    
def forward_to_dept(request,id):
    report=UserReports.objects.get(id=id)
    report.forward_to_dept=1
    report.save()
    return redirect ('admin_view_user_report')

def department_view_user_reports(request):
    reports=UserReports.objects.filter(forward_to_dept=1)
    return render(request,'department_view_user_reports.html',{'data':reports})

def admin_view_transactions(request):
    carts = UserCart.objects.filter(payment_status=1).order_by('-current_date','-current_time')
    transactions = []

    for cart in carts:
        # Matching cartid in PaymentDetails (it's stored as CharField)
        payments = PaymentDetails.objects.filter(cart_id=str(cart.cartid))
        transactions.append({
            'cart': cart,
            'payments': payments
        })

    return render(request, 'admin_view_transactions.html', {'transactions': transactions})

def restaurant_view_review(request):
    res_id = request.session.get('restaurant_id')
    if not res_id:
        return redirect('index')
    login=get_object_or_404(Login,id=res_id)
    restaurant=Restaurants.objects.get(login_id=login)
    print (login)
    
    if not res_id:
        # Optional: Handle case where restaurant_id isn't in session
        return redirect('restaurant_login')  # or show error page

    reviews = Reviews.objects.filter(restaurant_id=restaurant).order_by('-id')  # latest first
    return render(request, 'restaurant_view_review.html', {'reviews': reviews})

# def staff_restaurant_message(request):
#     staff_id=request.session.get('staff_id')
#     staff=get_object_or_404(Staffs,login_id=staff_id)
#     restaurant=Staffs.objects.get(restaurant_name=staff.restaurant_name)
#     if request.method=='POST':
#         message=request.POST.get('messages'),
#         StaffMessages.objects.create(
#             staff_id=staff,
#             restaurant_id=restaurant,
#             message=message
#         )
#     else:
#         messages=StaffMessages.objects.filter(staff_id=staff)
#     return render(request,'staff_restaurant_message.html',{'messages':messages})

from collections import Counter
from .models import UserCart, Dishes

def recommend_dishes_for_user(user):
    # Step 1: Get all paid cart items for the user
    paid_carts = UserCart.objects.filter(user_id=user, payment_status=1)

    # Step 2: Get purchased dish IDs and their categories
    purchased_dishes = [cart.product_id for cart in paid_carts]
    purchased_dish_ids = [dish.id for dish in purchased_dishes]
    purchased_categories = [dish.category for dish in purchased_dishes]

    # Step 3: Count most common categories or dishes
    common_categories = Counter(purchased_categories).most_common()
    # Optionally: common_dishes = Counter(purchased_dish_ids).most_common()

    # Step 4: Recommend dishes from similar categories not already purchased
    recommendations = Dishes.objects.filter(
        category__in=[cat[0] for cat in common_categories]
    ).exclude(id__in=purchased_dish_ids, status=0)[:10]  # Only active dishes

    return recommendations

def recommended_view(request):
    user_id=request.session.get('user_id')
    if not user_id:
        return redirect('index')
    print(user_id)
    # user=get_object_or_404(Users,login_id=user_id)
    user = Users.objects.get(login_id=user_id)  # Adjust based on auth system
    recommended_dishes = recommend_dishes_for_user(user)
    return render(request, 'recommendations.html', {'dishes': recommended_dishes})

def restaurant_staff_chat(request,id):
    res=request.session.get('restaurant_id')
    restaurant=Restaurants.objects.get(login_id=res)
    staff=get_object_or_404(Staffs,id=id)
    if request.method=='POST':
        message=request.POST.get('message')
        StaffMessages.objects.create(
            staff_id=staff,
            restaurant_id=restaurant,
            messages=message
        )
    return render(request,'restaurant_staff_message.html',{'staff_data':staff})

def staff_restaurant_chat(request):
    staff_id=request.session.get('staff_id')
    if not staff_id:
        return redirect('index')
    staff=Staffs.objects.get(login_id=staff_id)
    restaurant=staff.restaurant_name
    messages = StaffMessages.objects.filter(staff_id=staff).order_by('-current_date', '-current_time')

    print(messages)
    return render(request,'staff_restaurant_message.html',{'message_data':messages})

def staff_dish_search(request):
    query = request.GET.get('query', '')
    dishes = Dishes.objects.filter(dish_name__icontains=query)
    return render(request, 'staff_dish_view.html', {'dishes': dishes})
