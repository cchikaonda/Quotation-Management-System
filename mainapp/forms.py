from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import CustomUser, Customer,Unit, ItemCategory, Item, Order
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.views.generic import UpdateView
from django.db import models
from django_countries.fields import CountryField
from constance.admin import ConstanceAdmin, ConstanceForm, Config
from djmoney.forms.widgets import MoneyWidget
from django.contrib.auth import authenticate, login, logout, get_user_model



class UserAdminCreationForm(forms.ModelForm):
    # a form for creating new users. Includes all the required fields
    #plus a repeated password
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email','full_name','image','phone_number','active', 'admin','staff','user_role')
    def clean_password2(self):
        #check that the 2 password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't Match!")
        return password2
    def save(self, commit = True):
        # save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','full_name','phone_number','user_role','image','active', 'admin','staff')
    def save(self, commit = True):
        user = super(EditUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class EditUserPermissionsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','full_name','phone_number','user_role','image','active', 'admin','staff')
        widgets = {
                'email':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                'full_name':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                'phone_number':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                }

    def save(self, commit = True):
        user = super(EditUserPermissionsForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class LogInForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','password',)
        exclude = ('email',)
        widgets = {
                'password':forms.PasswordInput(attrs={'class': 'form-control login-form',}),
                }

class UserLockForm(forms.Form):

    def __init__(self,request,*args,**kwargs):
        super (UserLockForm,self).__init__(*args,**kwargs)
        self.fields['username'] = forms.CharField(label='Username',max_length=100, initial= 'chiccochikaonda@gmail.com')
    
class CustomConfigForm(forms.Form):
    class Meta:
        model = Config
        fields = ('SHOP_NAME','LOGO_IMAGE','ADDRESS','LOCATION','PHONES','EMAIL','TAX_NAME')
        exclude = ('SHOP_NAME',)
        widgets = {
                'SHOP_NAME':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                }
    def save(self, commit = True):
        config = super(CustomConfigForm, self).save(commit=False)
        if commit:
            config.save()
        return config
        

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email','full_name','phone_number','image')
        widgets = {
                'email':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                }
    def save(self, commit = True):
        user = super(EditProfileForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
        #A form for updating users.Includes all the fields on the
        #user, but replaces the password field with admin's password hashe
        #displayfield
        password = ReadOnlyPasswordHashField()
        class meta:
            model = CustomUser
            fields = ('full_name','email','phone_number','image', 'password','active', 'admin', 'user_role')
        def clean_password2(self):
                #regardless of what the user provides, return the initial Value
                #This is done here, rather than on the field, because the
                #field does not have access to the initial Value
            return self.initial("password")

class UserEditForm(UpdateView):
        #A form for updating users.Includes all the fields on the
        #user, but replaces the password field with admin's password hashe
        #displayfield
        password = ReadOnlyPasswordHashField()
        class meta:
            model = CustomUser
            fields = ('full_name','email','phone_number','image','active', 'admin','user_role')
        def save(self, commit = True):
            user = super(UserEditForm, self).save(commit = False)
            password = self.cleaned_data["password"]
            if password:
                user.set_password(password)
            if commit:
                user.save()
            return user

#class LogInForm(forms.Form):
#    email = forms.EmailField(label = 'Email', max_length = 25)
#    password = forms.CharField(label = 'Password', max_length = 8, widget = forms.PasswordInput)

class ChangeUserPasswordForm(forms.ModelForm):
    # a form for creating new users. Includes all the required fields
    #plus a repeated password
    old_password = forms.CharField(label = 'Current Password', widget = forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
                'email':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                }

    def clean_password2(self):
        old_password = self.cleaned_data.get("old_password")
        if CustomUser.check_password(old_password, CustomUser.password ) != True:
            raise forms.ValidationError("Enter Correct Password!")
        return old_password
        #check that the 2 password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't Match!")
        return password2

    def save(self, commit = True):
        # save the provided password in hashed format
        user = super(ChangeUserPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address','country','phone_number','email','total_quotations')
        widgets = {
            "name": forms.TextInput(attrs={'class': 'js-max-length form-control payment_form'}),
            "address": forms.TextInput(attrs={'class': 'js-max-length form-control payment_form'}),
            "phone_number": forms.TextInput(attrs={'class': 'js-max-length form-control payment_form'}),
            "total_quotations": forms.TextInput(attrs={'class': 'js-max-length form-control payment_form','readonly':'readonly'}),
        }

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ('category_name', 'category_description', )
    
class AddUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('unit_short_name', 'unit_description', )


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'item_name', 'price','discount_price',
        'category',
        'item_description', 'slug', 'active', 'unit',)
        widgets = {
            'description': forms.TextInput(attrs={'class': 'js-max-length form-control','max-length': '70', 'id': 'example-max-length4','placeholder': '50 chars limit..', 'data-always-show': 'True',
                                                  'data-pre-text': 'Used', 'data-separator': 'of',
                                                  'data-post-text': 'characters'})
        }

class CustomMoneyWidget(MoneyWidget):
    def format_output(self, rendered_widgets):
        return ('<div class="row">'
                    '<div class="col-xs-6 col-sm-10">%s</div>'
                    '<div class="col-xs-6 col-sm-2">%s</div>'
                '</div>') % tuple(rendered_widgets)

class SearchForm(forms.ModelForm):
     class Meta:
         model = Item
         fields = ('item_name',)
         widgets = {
                  'item_name': forms.TextInput(attrs={'class': 'form-control payment_form','placeholder':'Search Item','id':'search-form',
                  })
          }

class UpdateQuotationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('code', 'status', )
        widgets = {
                'code':forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
                }

class ChangeMarkupForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('markup', )