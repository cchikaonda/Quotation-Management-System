from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import (
    add_to_cart,
    remove_from_cart,
    suspend_order,
    add_customer_to_quotation,
    add_expire_date_to_quotation,
    quotation_summery,
    complete_quotation,
    remove_single_item_from_cart,
    add_customer,
) 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LoginView.as_view(), name = 'logout'),
    path('mainapp/logout_request', views.logout_request, name = 'logout_request'),
    path('', views.SystemDashboardView.as_view(), name = 'system_dashboard'),

    path('customers/customer_list/', views.customer_list, name = 'customer_list'),
    path('customers/customer_create/', views.customer_create, name = 'customer_create'),
    path('customers/customer_update/<int:id>/', views.customer_update, name = 'customer_update'),
    path('customers/customer_delete/<int:id>/', views.customer_delete, name = 'customer_delete'),


    path('items/item_list/', views.item_list, name = 'item_list'),
    path('items/item_create/', views.item_create, name = 'item_create'),
    path('items/item_update/<int:id>/', views.item_update, name = 'item_update'),
    path('items/item_delete/<int:id>/', views.item_delete, name = 'item_delete'),

    path('item_categories/category_list/', views.category_list, name = 'category_list'),
    path('item_categories/category_create/', views.category_create, name = 'category_create'),
    path('item_categories/category_update/<int:id>/', views.category_update, name = 'category_update'),
    path('item_categories/category_delete/<int:id>/', views.category_delete, name = 'category_delete'),

    path('units/unit_list/', views.unit_list, name = 'unit_list'),
    path('units/unit_create/', views.unit_create, name = 'unit_create'),
    path('units/unit_update/<int:id>/', views.unit_update, name = 'unit_update'),
    path('units/unit_delete/<int:id>/', views.unit_delete, name = 'unit_delete'),

    path('users/user_list/', views.user_list, name = 'user_list'),
    path('users/user_update/<int:id>/', views.user_update, name = 'user_update'),
    path('users/user_create/', views.user_create, name = 'user_create'),
    path('users/user_delete/<int:id>/', views.user_delete, name = 'user_delete'),
    path('users/user_profile/', views.user_profile, name = 'user_profile'),
    path('users/change_password/', views.change_password, name = 'change_password'),

    path('quotations/quotation/', views.quotation, name = 'quotation'),
    path('quotations/quotation_dashboard/', csrf_exempt(views.quotation_dashboard), name = 'quotation_dashboard'),

    path('quotations/quotation_list/', views.quotation_list, name = 'quotation_list'),
    path('quotations/quotation_update/<int:id>/', views.quotation_update, name = 'quotation_update'),
    path('quotations/quotation_delete/<int:id>/', views.quotation_delete, name = 'quotation_delete'),


    path('quotations/quotation_summery/<int:id>/', quotation_summery, name = 'quotation_summery'),

    

    path('add_to_cart/<slug>/', add_to_cart, name = 'add_to_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name = 'remove_single_item_from_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name = 'remove_from_cart'),
    path('suspend_order/', suspend_order, name = 'suspend_order'),

    path('add_customer_to_quotation/', add_customer_to_quotation, name = 'add_customer_to_quotation'),
    path('change_markup/', views.change_markup, name = 'change_markup'),

    path('add_expire_date_to_quotation/', add_expire_date_to_quotation, name = 'add_expire_date_to_quotation'),
    
    path('add_customer/', add_customer, name = 'add_customer'),
    
    
    path('complete_quotation/', complete_quotation, name = 'complete_quotation'),
    
]