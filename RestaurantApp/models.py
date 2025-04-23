from django.db import models
import uuid

class Users(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_id=models.OneToOneField('Login',on_delete=models.CASCADE, related_name='users')
    

class Login(models.Model):
        email=models.CharField(max_length=100)
        password=models.CharField(max_length=100)
        usertype=models.IntegerField(default=0)

class Restaurants(models.Model):
        category=models.CharField(max_length=100)
        name=models.CharField(max_length=100)
        image=models.FileField(upload_to='image/')
        address=models.CharField(max_length=500)
        district=models.CharField(max_length=50)
        city=models.CharField(max_length=100)
        contact=models.CharField(max_length=100)
        approval_status=models.IntegerField(default=0,null=False)#1-pending, 2-approved, 3-freezed
        login_id=models.ForeignKey('Login',on_delete=models.CASCADE)
        def __str__(self):
            return self.name
        
        

class Staffs(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    contact = models.CharField(max_length=15)
    restaurant_name = models.ForeignKey(Restaurants, on_delete=models.CASCADE, default=True, related_name='staffs')
    login_id = models.ForeignKey('Login', on_delete=models.CASCADE)

    
class FoodSafetyDepartment(models.Model):
    department_id=models.IntegerField()
    contact=models.CharField(max_length=15)
    login_id=models.ForeignKey('Login',on_delete=models.CASCADE)

class Dishes(models.Model):
    category=models.CharField(max_length=50)
    sub_category=models.CharField(max_length=50)
    dish_name=models.CharField(max_length=100)
    description=models.TextField(max_length=200)
    price=models.CharField(max_length=10)
    image=models.FileField(upload_to='dishes/')
    added_date=models.DateField(auto_now_add=True)
    login_id=models.ForeignKey('Staffs',on_delete=models.CASCADE)
    status=models.IntegerField(default=0)

class UserCart(models.Model):
    cartid = models.UUIDField(editable=False)  # Remove default uuid.uuid4()
    user_id=models.ForeignKey("Users", on_delete=models.CASCADE, related_name='user')
    restaurant_loginid=models.ForeignKey("Restaurants", on_delete=models.CASCADE,related_name='restaurant')
    product_id=models.ForeignKey("Dishes",on_delete=models.CASCADE)
    current_date=models.DateField(auto_now_add=True)
    current_time=models.TimeField(auto_now_add=True)
    payment_status=models.IntegerField(default=0)
    order_status=models.IntegerField(default=0)
    remove_status=models.IntegerField(default=0)
    cancel_status=models.IntegerField(default=0)
    quantity=models.IntegerField(null=False,default=1)
    def save(self, *args, **kwargs):
        if not self.cartid:
            # Check if the user already has a cartid
            existing_cart = UserCart.objects.filter(user_id=self.user_id).first()
            if existing_cart:
                self.cartid = existing_cart.cartid  # Assign existing cartid
            else:
                self.cartid = uuid.uuid4()  # Generate new cartid if the user has no cart

        super(UserCart, self).save(*args, **kwargs)
    
class PaymentDetails(models.Model):
    card_number = models.IntegerField(max_length=16,null=True)  
    expiry_month = models.IntegerField(max_length=2,null=True)
    expiry_year = models.IntegerField(max_length=4,null=True)
    cvv_code = models.IntegerField(max_length=3,null=True)  
    owner_name = models.CharField(max_length=100,null=True)
    amount = models.IntegerField(default=0,null=True)
    cart_id = models.CharField(max_length=100,null=True)
    upi=models.CharField(default=False,null=True,max_length=100)
    upi_id=models.CharField(null=True,max_length=100)
    pickup=models.CharField(max_length=100,default=False,null=True)

class Chat(models.Model):
     user_sender_id=models.ForeignKey('Users',on_delete=models.CASCADE,related_name='user_sender_id',null=True)
     user_reciever_id=models.ForeignKey('Users',on_delete=models.CASCADE,related_name='user_reciever_id',null=True)
     restaurant_sender_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE,related_name='restaurant_sender_id',null=True)
     restaurant_reciever_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE,related_name='restaurant_reciever_id',null=True)
     messages=models.TextField()
     date_and_time=models.DateTimeField(auto_now_add=True)

class Table(models.Model):
    user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
    restaurant_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE)
    number_of_people=models.IntegerField()
    rdate=models.DateField()
    rtime=models.TimeField()
    notes=models.TextField()

class Reviews(models.Model):
    user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
    restaurant_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE)
    images=models.FileField(upload_to='image/',null=False)
    star=models.IntegerField(null=False,default=0)
    review=models.TextField()
    current_date=models.DateField(auto_now_add=True)

class Complaints(models.Model):
     user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
     restaurant_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE)
     subject=models.CharField(max_length=100)
     complaint=models.TextField()

class UserReports(models.Model):
     user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
     restuarant_id=models.ForeignKey('Restaurants',on_delete=models.CASCADE)
     text=models.CharField(max_length=500)