from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from constance.admin import ConstanceAdmin, ConstanceForm, Config
#from bootstrap_modal_forms.forms import BSModalModelForm

# Register your models here.
CustomUser = get_user_model()

from mainapp.models import Customer, ItemCategory, Unit, Item, OrderItem, Order

class CustomeUserAdmin(BaseUserAdmin):
    #the forms to add and change user instances
    change_form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    #the fields to be used in dispaying the user models
    #these override the definitions on the base UserAdmin
    #that reference specific fields on auth.user
    list_display = ('full_name','email', 'admin','phone_number', 'image','password')
    list_filter = ('superuser','admin','active','staff','staff')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal information', {'fields': ('full_name','phone_number','image')}),
        ('Permissions', {'fields': ('superuser','admin', 'active','staff','password')}),
    )
    #add_fieldsets is not a standard ModelAdmin attribute. UserAdmins
    #overrides get_fieldsets to use this attribute when creating a user
    add_fieldsets = (
        (None,{
             'classes': ('wide',),
             'fields': ('email','full_name','phone_number','image','admin','active','superuser','staff','password1', 'password2'),}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomeUserAdmin)
admin.site.unregister(Group)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','address','country','total_quotations','phone_number','email')
    search_fields = ['name',]
    class Meta:
        model = Customer
admin.site.register(Customer, CustomerAdmin)


class CustomConfigForm(ConstanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         #... do stuff to make your settings form nice ...
    

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_description',)
    search_fields = ['category_name', ]

    class Meta:
        model = ItemCategory
admin.site.register(ItemCategory, ItemCategoryAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_short_name', 'unit_description',
        )
    search_fields = ['unit_short_name', ]
    class Meta:
        model = Unit
admin.site.register(Unit, UnitAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_name', 'price', 'selling_price', 'discount_price',
        'category',
        'item_description', 'slug', 'active', 'unit',
        )
    search_fields = ['item_name', ]
    class Meta:
        model = Item
admin.site.register(Item, ItemAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user','item','quantity','ordered_item_price','price','ordered_items_total','amount','get_total_amount')
    search_fields = ['item',]
    class Meta:
        model = CustomUser

admin.site.register(OrderItem, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','code','user','markup','get_markup_value','markup_value','labour_p','labour_cost','vat_p','vat_cost','order_date','expire_date','is_order_expire','status','order_total_cost')
    search_fields = ['order_date',]
    class Meta:
        model = CustomUser
admin.site.register(Order, OrderAdmin)

