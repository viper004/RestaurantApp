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
    return render(request, 'home-pages/admin_home.html')

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
     a = Users.objects.all()
     return render(request, 'admin-account-view/admin_user_view.html',{'data':a})

def login_action(request):
    if request.method=="POST":
        form=loginform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
        try:
            user = Login.objects.filter(email=email).first()
            if user.password==password:
                if user.usertype==1:
                    request.session['user_id']=user.id
                    return redirect('user_home')
                elif user.usertype==2:
                    resstaurant=get_object_or_404(Restaurants,login_id=user.id)
                    if resstaurant.approval_status==0:
                        return render(request,'home-pages/pending_restaurant_home.html')
                    if resstaurant.approval_status==2:
                        return render(request,'home-pages/freezed_Restaurant_home.html')
                    request.session['restaurant_id']=user.id
                    
                    # if user.id.approval_status==2:
                    #     return render(request,'freezed_Restaurant_home.html')
                    return redirect('restaurant_home')
                elif user.usertype==3:
                    request.session['staff_id']=user.id
                    return redirect('staff_home')
                elif user.usertype==4:
                    request.session['department_id']=user.id
                    return redirect('department_home')
                    
                else:
                    messages.error(request,'Incorrect Password')

        except Login.DoesNotExist:
            messages.error(request,'User Does Not Exist')
    else:
        form=loginform()
    return render(request,'login.html',{'form':form})

def user_home(request):
    user_id=request.session.get('user_id')
    login_details=get_object_or_404(Login,id=user_id)
    user_details=get_object_or_404(Users,login_id=login_details)
    return render(request,'home-pages/user_home.html',{'details':user_details})

def restaurant_home(request):
    restaurant_id=request.session.get('restaurant_id')
    res=Restaurants.objects.get(login_id=restaurant_id)
    return render(request,'home-pages/restaurant_home.html',{'details':res})

def staff_home(request):
    return render(request,'home-pages/staff_home.html')

def department_home(request):
    return render(request,'home-pages/department_home.html')

def user_profile(request):
    user_id=request.session.get('user_id')
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
    restaurant_id=request.session.get('restaurant_id')
    login_details=get_object_or_404(Login,id=restaurant_id)
    data=get_object_or_404(Restaurants,login_id=restaurant_id)
    if request.method=='POST':
        form=edit_user(request.POST,instance=data)
        form2=login_form(request.POST,instance=login_details)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('restaurant_home')
    else:
        form=edit_user(instance=data)
        form2=login_form(instance=login_details)
    return render(request,'restaurant_profile_edit.html',{'form':form,'form2':form2})


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
    else:
            form=restaurant_form()
            login=login_form()

    return render(request,'registration-pages/restaurant_registration.html',{'form':form,'login':login})

def staff_profile(request):
    staff_id=request.session.get('staff_id')
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
    if request.method=='POST':
        form=staff_form(request.POST,request.FILES)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=3
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,"Form successfully submitted")
            return redirect('index')
    else:
            form=staff_form()
            login=login_form()

    return render(request,'registration-pages/staff_registration.html',{'form':form,'login':login})

def food_and_safety_department_registration(request):
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
    data=Restaurants.objects.filter(approval_status=0)
    return render(request,'admin-account-view/admin_view_pending_restaurant.html',{'a':data})

def admin_approve_restaurant(request,id):
    restaurant=get_object_or_404(Restaurants,id=id)
    restaurant.approval_status=1
    restaurant.save()
    return redirect('admin_view_pending_restaurant')

def admin_reject_restaurant(request,id):
    restaurant=get_object_or_404(Restaurants,id=id)
    b=restaurant.login_id
    restaurant.delete()
    if b:
        b.delete()
    return redirect('admin_view_pending_restaurant')

def admin_freeze_restaurant(request,id):
    restaurant=get_object_or_404(Restaurants,id=id)
    restaurant.approval_status=2
    restaurant.save()
    return redirect('admin_restaurant_view')

def admin_view_freezed_restaurants(request):
    data=Restaurants.objects.filter(approval_status=2)
    return render(request,'admin-account-view/admin_view_freezed_restaurants.html',{'a':data})


def admin_restaurant_view(request):
     data=Restaurants.objects.filter(approval_status=1)
     return render(request,'admin-account-view/admin_restaurant_view.html',{'a':data})

def admin_staff_view(request):
     data=Staffs.objects.all()
     return render(request,'admin-account-view/admin_staff_view.html',{'a':data})

def restaurant_cards(request):
    restaurants=Restaurants.objects.filter(approval_status=1)
    return render(request,'restaurant_cards.html',{'restaurants':restaurants})

def staff_cards(request):
    res_id=request.session.get('restaurant_id')
    login_details=get_object_or_404(Login,id=res_id)
    data=get_object_or_404(Restaurants,login_id=login_details)
    staffs=Staffs.objects.filter(restaurant_name=data)
    print("data....",staffs)
    return render(request,'staff_cards.html',{'staffs':staffs})

def add_dish(request):
    staff_id = request.session.get('staff_id')
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
    print(user_login)
    restaurant = get_object_or_404(Restaurants,login_id=user_login)
    dishes = Dishes.objects.filter(login_id__restaurant_name=restaurant)
    
    
    return render(request, 'restaurant_dish_view.html', {'dishes': dishes})

def user_restaurant_view(request,id):
    user_id=request.session.get('user_id')
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
    login_details=Staffs.objects.get(login_id=staff)
    dishes=Dishes.objects.filter(login_id=login_details)
    return render(request,'staff_dish_view.html',{'dishes':dishes})

def staff_dish_edit(request,id):
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
    dishes=get_object_or_404(Dishes,id=id)
    dishes.delete()
    return redirect('staff_dish_view')

def add_to_menu(request,id):
    dishes=get_object_or_404(Dishes,id=id)
    dishes.status=1
    dishes.save()
    return redirect('staff_menu')


def staff_menu_view(request):
    staff_id = request.session.get('staff_id') 
    login_details = get_object_or_404(Login, id=staff_id)  
    staff = get_object_or_404(Staffs, login_id=login_details) 
    dishes = Dishes.objects.filter(login_id=staff, status=1)
    return render(request, 'staff_menu_view.html', {'dishes': dishes})


def menu_item_remove(request,id):
    dishes=get_object_or_404(Dishes,id=id)
    dishes.status=0
    dishes.save()
    return redirect('staff_menu')


def add_to_cart(request, restaurant_id, product_id):
    user=request.session.get('user_id')
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
    return JsonResponse({"message": "Product added to cart successfully!"})


def user_cart_view(request):
    user=request.session.get('user_id')
    log_details=get_object_or_404(Users,login_id=user)
    product=UserCart.objects.filter(user_id=log_details).exclude(remove_status=1)
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
    log_details=get_object_or_404(Users,login_id=user_id)
    user_cart=UserCart.objects.filter(user_id=log_details,payment_status=1).exclude(cancel_status=1)
    return render(request,'user_order_view.html',{'details':user_cart})

def user_cancel_order(request,id):
    cart=get_object_or_404(UserCart,id=id)
    cart.cancel_status=1
    cart.save()
    return redirect('user_order_view')

def restaurant_order_view(request):
    res_id=request.session.get('restaurant_id')
    log_details=get_object_or_404(Restaurants,login_id=res_id)
    orders=UserCart.objects.filter(restaurant_loginid=log_details,payment_status=1).select_related('user_id__users').order_by('current_time')
    return render(request,'restaurant_order_view.html',{'details':orders})

def user_restaurant_chat(request,id):
    usr=request.session.get('user_id')
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
    restaurant=get_object_or_404(Restaurants,login_id=res_id)
    res=Chat.objects.filter(restaurant_reciever_id=restaurant)
    print(res)
    user = Chat.objects.filter(restaurant_reciever_id=restaurant).values_list('user_sender_id__name','user_sender_id__id',flat=False).distinct()

    return render(request,'restaurant_chat_list_view.html',{'res':user})

def restaurant_user_chat(request,id):
    res=request.session.get('restaurant_id')
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
    reservation=get_object_or_404(Restaurants,login_id=res_id)
    reservations = Table.objects.filter(restaurant_id=reservation).order_by('-rdate', '-rtime')
    return render(request,'restaraunt_reservation_view.html',{'details':reservations})

def staff_reservation_view(request):
    staff_id=request.session.get('staff_id')
    current_date = timezone.now().date() 
    staff=get_object_or_404(Staffs,login_id=staff_id)
    reservations=Table.objects.filter(restaurant_id=staff.restaurant_name,rdate=current_date).order_by('-rtime')
    return render(request,'staff_reservation_view.html',{'details':reservations})

def staff_order_view(request):
    staff_id=request.session.get('staff_id')
    staff=get_object_or_404(Staffs,login_id=staff_id)
    current_date=timezone.now().date()
    orders=UserCart.objects.filter(restaurant_loginid=staff.restaurant_name,current_date = current_date)
    return render(request,'staff_order_view.html',{'details':orders})

def order_ready(request,id):
    a=get_object_or_404(UserCart,id=id)
    a.order_status=1
    a.save()
    return redirect('staff_order_view')

def user_reservation_view(request):
    user_id=request.session.get('user_id')
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
    reports=UserReports.objects.all()
    return render(request,'admin_report_view.html',{'data':reports})

def view_ratings(request,id):
    reviews=Reviews.objects.filter(restaurant_id=id)
    restaurant=get_object_or_404(Restaurants,id=id)
    return render(request,'user_view_ratings.html',{'reviews':reviews,'restaurant':restaurant})


def logout_view(request):
    request.session.clear()
    return redirect('login')

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
