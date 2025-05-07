from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class user_form(forms.ModelForm):
    class Meta:
        model=Users
        fields=['name','contact']

class login_form(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email','password']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.password = make_password(self.cleaned_data['password'])  # Hash here
    #     if commit:
    #         user.save()
    #     return user

class loginform(forms.Form):
    email=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Password'}))

class edit_user(forms.ModelForm):
    class Meta:
        model=Users
        fields=['name','contact']

class restaurant_form(forms.ModelForm):
    class Meta:
        model=Restaurants
        fields=['category','name','image','address','district','city','contact','about']



class certificate_form(forms.ModelForm):
    HAVE_CERTIFICATE_CHOICES = [
        (0, 'Yes'),
        (1, 'No'),
    ]

    have_certificate = forms.ChoiceField(
        choices=HAVE_CERTIFICATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Restaurants
        fields = ['have_certificate', 'fssai_nunmber']
        widgets = {
            'fssai_nunmber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter FSSAI License Number'
            })
        }

class staff_form(forms.ModelForm):

    GENDER_CHOICES = [
        ('','Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender=forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = Staffs
        fields = ['name', 'gender', 'age', 'contact']

class food_and_safety_department_form(forms.ModelForm):
    class Meta:
        model = FoodSafetyDepartment
        fields=['department_id','contact']
    
class dishes_form(forms.ModelForm):
  
    class Meta:
        model=Dishes
        fields=['category','sub_category','dish_name','description','price','image']

    SUB_CATEGORY=[
        ('','Select'),
        ('VEG','VEG'),
        ('NON VEG','NON VEG'),
    ]
    sub_category=forms.ChoiceField(choices=SUB_CATEGORY)

    CATEGORY=[
        ('','Select Category'),
        ('ARABIC','ARABIC'),
        ('NORTH INDIAN','NORTH INDIAN'),
        ('CHINESE','CHINESE'),
        ('TRADITIONAL','TRADITIONAL')
    ]

    category=forms.ChoiceField(choices=CATEGORY)

class payment_form(forms.ModelForm):
    class Meta:
        model=PaymentDetails
        fields=['card_number','expiry_month','expiry_year','cvv_code','owner_name']
    
class messages_form(forms.ModelForm):
    class Meta:
        model=Chat
        fields=['messages']

class table_reservation_form(forms.ModelForm):
    class Meta:
        model=Table
        fields=['rdate','rtime','notes','number_of_people']
        # widget={'rdate':forms.DateInput()}

class user_review(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=['images','review','star']
        widget={'images':forms.FileInput()}

class user_complaint(forms.ModelForm):
    class Meta:
        model = Complaints
        fields=['subject','complaint']
        