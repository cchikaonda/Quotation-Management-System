from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.shortcuts import reverse
from constance import config
from datetime import date


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name = None ,user_role = None,phone_number = None,password = None, is_active = True, is_admin = False, is_superuser = False):
        if not email:
            raise ValueError ("Users must have an email address")
        if not password:
            raise ValueError ("Users must have a password")
        if not full_name:
            raise ValueError (" Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            phone_number = phone_number,
            user_role = user_role,
        )
        user_obj.set_password(password) # change user password
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.superuser = is_superuser
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email,full_name = None,phone_number =None, password = None, user_role = None):
        user = self.create_user(
                email,
                full_name,
                phone_number,
                password = password,
                is_admin=True,
                is_active = True,
                is_superuser = True,
        )
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank = True, null=True)
    roles =(
        ('Admin','Admin'),
        ('User', 'General User')
    )
    user_role = models.CharField(max_length = 15, choices = roles, default = "General User")
    phone_number = models.CharField(max_length=20, blank = True, null=True)
    username = None
    active = models.BooleanField(default=True) #can login
    admin = models.BooleanField(default=False) # Adminstrator
    superuser = models.BooleanField(default=False) #superuser
    staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default = "avatar0.jpg", null = True, blank = True)

    USERNAME_FIELD = 'email' #loginuser
    REQUIRED_FIELDS = ['full_name','phone_number',]


    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_staff(self):
        return self.staff
    
    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    


class Customer(models.Model):
    name = models.CharField(unique=True, max_length=120)
    address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=50, default= "MALAWI")
    total_quotations = models.IntegerField(default=0)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        # return '{0} ({1})'.format(self.name, self.phone_number)
        return '{0}'.format(self.name)

class Unit(models.Model):
    unit_short_name = models.CharField(max_length=10)
    unit_description = models.CharField(max_length=100)
    def __str__(self):
        return self.unit_short_name

class ItemCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name
    
    @staticmethod
    def get_all_item_categories():
        return ItemCategory.objects.all()


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK')
    discount_price = MoneyField(max_digits=14, null=True, blank=True, decimal_places=2, default_currency='MWK')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.item_name

    def selling_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price

    
    @staticmethod
    def get_all_items():
        return Item.objects.all()

    @staticmethod
    def get_all_items_by_category_id(category_id):
        if category_id:
            return Item.objects.filter(category=category_id)
        else:
            return Item.get_all_items()

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True)
    item = models.ForeignKey(Item, related_name = 'order_item', on_delete = models.PROTECT)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_item_price = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    ordered_items_total = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    
    @property
    def price(self):
        return self.item.selling_price()

    @property
    def amount(self):
        amount = MoneyField()
        amount = self.quantity * self.item.selling_price()
        return amount

    @property
    def get_total_amount(self):
        return self.amount
    
    def get_item_discount(self):
        if self.item.discount_price:
            return self.quantity * self.item.price - self.quantity * self.item.discount_price
        else:
            return 0

    def __str__(self):
        return f"{self.quantity} {self.item.unit} of {self.item.item_name}"

class Order(models.Model):
    def gen_code(self):
            return 'QTD%04d'%self.pk
    code = models.CharField(max_length=50, null=True, default="0000")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField(null=True)
    markup_choices = (
        (config.MARKUP_A, 'Markup A'),
        (config.MARKUP_B, 'Markup B'),
        (config.MARKUP_C, 'Markup C'),
    )
    ordered = models.BooleanField(default=False)
    choices =(
        ('Pending','Pending ...'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    status = models.CharField(max_length = 15, choices = choices, default = "Pending ...")
    markup = models.FloatField(choices=markup_choices, default=config.MARKUP_A)
    markup_value = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    labour_p = models.FloatField(default=config.LABOUR_COST)
    labour_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    order_total_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)
    vat_p = models.FloatField(default=config.TAX_NAME)
    vat_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='MWK', default= 0.0)


    def __str__(self):
        return '{1} {0}'.format(self.order_date, self.customer)

    @property
    def vat_rate(self):
        return float(config.TAX_NAME)
    
    @property
    def get_code(self):
        return self.gen_code
    
    @property
    def labour(self):
        return float(config.LABOUR_COST)

    @property
    def is_order_expire(self):
        if self.expire_date:
            if self.expire_date < date.today():
                return True
            else:
                return False 
        else:
            return False
        

    def get_vat_value(self):
        return self.vat_rate / 100.00 * self.order_total()
        
    @property
    def get_markup_value(self):
        return self.markup / 100.00 * self.all_items_total()
    
    def get_labour_value(self):
        return self.labour / 100.00 * self.all_items_total()


    def order_total_due(self):
        return self.order_total() +  self.get_vat_value()

    def order_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.amount
        return total + self.get_markup_value + self.get_labour_value() 
    
    def all_items_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.amount
        return total

    def get_total_discount(self):
        discount_total = 0
        for ordered_item in self.items.all():
            discount_total += ordered_item.get_item_discount()
        return discount_total
    