from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from mainapp.forms import UserAdminCreationForm, EditUserPermissionsForm, EditProfileForm, ChangeUserPasswordForm, CustomConfigForm, EditUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from mainapp.models import CustomUser, Customer, ItemCategory, Item, Unit, Order, OrderItem
from django.template.loader import render_to_string
from django.http import JsonResponse
from constance import config
from constance.admin import ConstanceAdmin, ConstanceForm, Config
from mainapp.forms import AddCustomerForm, AddItemForm,AddUnitForm, AddCategoryForm, SearchForm, UpdateQuotationForm, ChangeMarkupForm
from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.filters import SearchFilter, OrderingFilter

from django.contrib.messages.views import SuccessMessageMixin
import json
from mainapp.templatetags.cart_template_tags import cart_item_count
import datetime
from django.utils import timezone
import json
from django.http import JsonResponse
from django.contrib.sessions.models import Session

# Create your views here.
class SystemDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "system_dashboard.html"
    # getting total quotes for the current week day
    def get_total_quotes_this_week(self, this_day):
        week_start = datetime.date.today()
        week_start -= datetime.timedelta(days=week_start.weekday())
        week_end = week_start + datetime.timedelta(days=6)
        total_quotes = Order.objects.filter(ordered=True).filter(order_date__gte=week_start, order_date__lt=week_end).filter(
            order_date__week_day=this_day).count()
        # total_quotes = Order.objects.filter(ordered=True).filter(order_date__gte=week_start, order_date__lt=week_end).count()
        return total_quotes
    
    def get_total_lastwk_sale(self, this_day_lw):
        some_day_last_week = timezone.now().date() - datetime.timedelta(days=7)
        monday_of_last_week = some_day_last_week - datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)
        total_quotes = Order.objects.filter(ordered=True).filter(order_date__gte=monday_of_last_week,
                                                      order_date__lt=monday_of_this_week).filter(
        order_date__week_day = this_day_lw).count()
        return total_quotes

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all().order_by('-id')[:10]
        orders = Order.objects.all().order_by('-order_date')[:10]

        pending_quotes = Order.objects.filter(ordered=True).filter(status='Pending')
        total_pending_orders = pending_quotes.count()

        pending_total_cost = 0
        for pending_quote in pending_quotes:
            pending_total_cost += pending_quote.order_total_cost

        cancelled_quotes = Order.objects.filter(ordered=True).filter(status='Cancelled')
        total_cancelled_orders = cancelled_quotes.count()

        cancelled_total_cost = 0
        for cancelled_quote in cancelled_quotes:
            cancelled_total_cost += cancelled_quote.order_total_cost

        completed_quotes = Order.objects.filter(status='Completed')
        total_completed_orders = completed_quotes.count()

        completed_total_cost = 0
        for completed_quote in completed_quotes:
            completed_total_cost += completed_quote.order_total_cost
        
        monday_total_quotes = self.get_total_quotes_this_week(2)
        
        tuesday_total_quotes = self.get_total_quotes_this_week(3)
        wednesday_total_quotes = self.get_total_quotes_this_week(4)
        thursday_total_quotes = self.get_total_quotes_this_week(5)
        friday_total_quotes = self.get_total_quotes_this_week(6)
        saturday_total_quotes = self.get_total_quotes_this_week(7)
        sunday_total_quotes = self.get_total_quotes_this_week(1)

        lw_monday_total_quotes = self.get_total_lastwk_sale(2)
        lw_tuesday_total_quotes = self.get_total_lastwk_sale(3)
        lw_wednesday_total_quotes = self.get_total_lastwk_sale(4)
        lw_thursday_total_quotes = self.get_total_lastwk_sale(5)
        lw_friday_total_quotes = self.get_total_lastwk_sale(6)
        lw_saturday_total_quotes = self.get_total_lastwk_sale(7)
        lw_sunday_total_quotes = self.get_total_lastwk_sale(1)
       

        today = datetime.datetime.today()
        expired_quotations = Order.objects.filter(expire_date__lt=today).count()
        all_customers = Customer.objects.all().count()
        all_users = CustomUser.objects.all().count()

        total_quotes = Order.objects.filter(ordered=True).count()
        total_quotes_today = Order.objects.filter(ordered=True).filter(order_date__gte=datetime.date.today()).count()

        total_item_cat = ItemCategory.objects.all().count()
        total_items = Item.objects.all().count()
        total_units = Unit.objects.all().count()

        queryset = get_current_users()
        count_logged_in_users = get_current_users().count()
        

        return {'header':'System Dashboard','config':config,'orders':orders,'customers':customers,'total_pending_orders':total_pending_orders,
        'total_cancelled_orders':total_cancelled_orders,'total_completed_orders':total_completed_orders,'expired_quotations':expired_quotations,
        'pending_total_cost':pending_total_cost,'cancelled_total_cost':cancelled_total_cost,'completed_total_cost':completed_total_cost,
        'monday_total_quotes':monday_total_quotes, 'tuesday_total_quotes':tuesday_total_quotes, 'wednesday_total_quotes':wednesday_total_quotes,
        'thursday_total_quotes':thursday_total_quotes,'friday_total_quotes':friday_total_quotes,
        'saturday_total_quotes':saturday_total_quotes,'sunday_total_quotes':sunday_total_quotes, 'total_quotes':total_quotes,'total_quotes_today':total_quotes_today,
        'all_customers':all_customers,'all_users':all_users,'lw_monday_total_quotes':lw_monday_total_quotes,'lw_tuesday_total_quotes':lw_tuesday_total_quotes,
        'lw_wednesday_total_quotes':lw_wednesday_total_quotes, 'lw_thursday_total_quotes':lw_thursday_total_quotes,'lw_friday_total_quotes':lw_friday_total_quotes,'lw_saturday_total_quotes':lw_saturday_total_quotes, 'lw_sunday_total_quotes':lw_sunday_total_quotes, 'queryset':queryset, 'count_logged_in_users':count_logged_in_users,
        'total_item_cat':total_item_cat, 'total_items':total_items,'total_units':total_units }

@login_required
def logout_request(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('modalShown')
    return response

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
        'header': 'Manage Customers',
        'config':config,
    }
    return render(request, 'customers/customer_list.html', context)

@login_required
def save_customer_list(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            customers = Customer.objects.all()
            data['customer_list'] = render_to_string('customers/customer_list_2.html', {'customers': customers})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
    else:
        form = AddCustomerForm()
    return save_customer_list(request, form, 'customers/customer_create.html')

@login_required
def customer_update(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = AddCustomerForm(request.POST, instance=customer)
    else:
        form = AddCustomerForm(instance=customer)
    return save_customer_list(request, form, 'customers/customer_update.html')

@login_required
def customer_delete(request, id):
    data = dict()
    customer = get_object_or_404(Customer, id=id)
    if request.method == "POST":
        customer.delete()
        data['form_is_valid'] = True
        customers = Customer.objects.all()
        data['customer_list'] = render_to_string('customers/customer_list_2.html', {'customers': customers})
    else:
        context = {'customer': customer}
        data['html_form'] = render_to_string('customers/customer_delete.html', context, request=request)
    return JsonResponse(data)

@login_required
def unit_list(request):
    units = Unit.objects.all()
    context = {
        'header': 'Manage Units',
        'units': units,
        'config':config,
    }
    return render(request, 'units/unit_list.html', context)

@login_required
def save_unit_list(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            units = Unit.objects.all()
            data['unit_list'] = render_to_string('units/unit_list_2.html', {'units': units})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def unit_create(request):
    if request.method == 'POST':
        form = AddUnitForm(request.POST)
    else:
        form = AddUnitForm()
    return save_unit_list(request, form, 'units/unit_create.html')

@login_required
def unit_update(request, id):
    unit = get_object_or_404(Unit, id=id)
    if request.method == 'POST':
        form = AddUnitForm(request.POST, instance=unit)
    else:
        form = AddUnitForm(instance=unit)
    return save_unit_list(request, form, 'units/unit_update.html')

@login_required
def unit_delete(request, id):
    data = dict()
    unit = get_object_or_404(Unit, id=id)
    if request.method == "POST":
        unit.delete()
        data['form_is_valid'] = True
        units = Unit.objects.all()
        data['unit_list'] = render_to_string('units/unit_list_2.html', {'units': units})
    else:
        context = {'unit': unit}
        data['html_form'] = render_to_string('units/unit_delete.html', context, request=request)
    return JsonResponse(data)


@login_required
def category_list(request):
    items = Item.objects.all()
    item_cats = ItemCategory.objects.all()
    context = {
        'items': items,
        'header': 'Manage Categories',
        'item_cats': item_cats,
        'config':config,
    }
    return render(request, 'item_categories/category_list.html', context)

@login_required
def save_all_categories(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            item_cats = ItemCategory.objects.all()
            data['category_list'] = render_to_string('item_categories/category_list_2.html',{'item_cats': item_cats})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
    else:
        form = AddCategoryForm()
    return save_all_categories(request, form, 'item_categories/category_create.html')

@login_required
def category_update(request, id):
    category = get_object_or_404(ItemCategory, id=id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
    else:
        form = AddCategoryForm(instance=category)
    return save_all_categories(request, form, 'item_categories/category_update.html')

@login_required
def category_delete(request, id):
    data = dict()
    category = get_object_or_404(ItemCategory, id=id)
    if request.method == "POST":
        category.delete()
        data['form_is_valid'] = True
        item_cats = ItemCategory.objects.all()
        data['category_list'] = render_to_string('item_categories/category_list_2.html',{'item_cats': item_cats})
    else:
        context = {'category': category}
        data['html_form'] = render_to_string('item_categories/category_delete.html', context, request=request)
    return JsonResponse(data)

@login_required
def item_list(request):
    items = None
    item_cats = ItemCategory.get_all_item_categories()

    items = None
    item_cat_id = request.GET.get('category')
    if item_cat_id:
        items = Item.get_all_items_by_category_id(item_cat_id)
    else:
        items = Item.get_all_items()
    context = {
        'items': items,
        'header': 'Manage Items',
        'item_cats': item_cats,
        'config':config,
    }
    return render(request, 'items/item_list.html', context)

@login_required
def save_all_items(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            items = Item.get_all_items()
            data['item_list'] = render_to_string('items/item_list_2.html', {'items': items})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
    else:
        form = AddItemForm()
    return save_all_items(request, form, 'items/item_create.html')

@login_required
def item_update(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        form = AddItemForm(request.POST, instance=item)
    else:
        form = AddItemForm(instance=item)
    return save_all_items(request, form, 'items/item_update.html')

@login_required
def item_delete(request, id):
    data = dict()
    item = get_object_or_404(Item, id=id)
    if request.method == "POST":
        item.delete()
        data['form_is_valid'] = True
        items = Item.get_all_items()
        data['item_list'] = render_to_string('items/item_list_2.html', {'items': items})
    else:
        context = {'item': item}
        data['html_form'] = render_to_string('items/item_delete.html', context, request=request)
    return JsonResponse(data)

@login_required
def user_list(request):
    users = CustomUser.objects.exclude(email = request.user)
    context = {
    'users': users,
    'header': 'Manage users',
    'config':config,
    }
    return render(request, 'users/user_list.html',context)

@login_required
def save_all_users(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			users = CustomUser.objects.exclude(email = request.user)
			data['user_list'] = render_to_string('users/user_list_2.html',{'users':users})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def user_create(request):
	if request.method == 'POST':
		form = UserAdminCreationForm(request.POST)
	else:
		form = UserAdminCreationForm()
	return save_all_users(request,form,'users/user_create.html')

@login_required
def user_update(request,id):
	user = get_object_or_404(CustomUser,id=id)
	if request.method == 'POST':
		form = EditUserPermissionsForm(request.POST,instance=user)
	else:
		form = EditUserPermissionsForm(instance=user)
	return save_all_users(request,form,'users/user_update.html')

@login_required
def user_delete(request,id):
	data = dict()
	user = get_object_or_404(CustomUser,id=id)
	if request.method == "POST":
		user.delete()
		data['form_is_valid'] = True
		users = CustomUser.objects.exclude(email = request.user)
		data['user_list'] = render_to_string('users/user_list_2.html',{'users':users})
	else:
		context = {'user':user}
		data['html_form'] = render_to_string('users/user_delete.html',context,request=request)
	return JsonResponse(data)

@login_required
def user_profile(request):
    user = request.user
    form = EditProfileForm(instance = user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, "User Profile Successfully updated")
            
    context = {
        'form': form,
        'config':config,
    }
    return render(request, 'users/user_profile.html', context)

@login_required
def change_password(request):
    user = request.user
    form = ChangeUserPasswordForm(instance = user)
    if request.method == 'POST':
        form = ChangeUserPasswordForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'config':config,
    }
    return render(request, 'users/change_password.html', context)

def quotation(request):
    current_quotation = Order.objects.get(user=request.user, ordered = False)
    context = {
        'config':config,
        'current_quotation':current_quotation,
    }
    return render(request, 'quotations/quotation.html',context )

def quotation_dashboard(request):
    item_cat = ItemCategory.get_all_item_categories()
    customers = Customer.objects.all()

    items = None
    item_cat_id = request.GET.get('category')
    if item_cat_id:
        items = Item.get_all_items_by_category_id(item_cat_id)
    else:
        items = Item.get_all_items()

    try:
        order = Order.objects.get(user=request.user, ordered = False)
    except ObjectDoesNotExist:
        order = ""
    
    query = request.GET.get("barcode", None)
    if query is not None:
        items = (items.filter(barcode__startswith  = query) | items.filter(item_name__startswith  = query))|items.filter(item_name__icontains = query)
    
    items_in_order = cart_item_count(user=request.user)

    item_search_form = SearchForm()
   
    customer_form = AddCustomerForm()

    markup_form = ChangeMarkupForm()

    context = {
     'items_in_order':items_in_order,
      'items':items,
      'order':order,
      'item_cat':item_cat,
      'item_search_form':item_search_form,
      'customers':customers,
      'customer_form':customer_form,
      'config':config,
      'markup_form':markup_form,
    }
    return render(request, 'quotations/quotation_dashboard.html',context)

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user = request.user, ordered = False)
    Order_qs = Order.objects.filter(user=request.user, ordered= False)
    if Order_qs.exists():
        order = Order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            item.save()
        else:
            order.items.add(order_item)
            item.save()
    else:
        order_date = timezone.now()
        order = Order.objects.create(user = request.user, order_date = order_date)
        order.items.add(order_item)
        item.save()
    return redirect('quotation_dashboard')

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    Order_qs = Order.objects.filter(user=request.user, ordered= False)

    if Order_qs.exists():
        order = Order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered = False)[0]
            order_item.ordered = True
            order.items.remove(order_item)
            order_item.delete()
            item.save()
        else:
        # add a message saying the user doesnt have an order
            messages.info(request, "This Item is not in Cart!")
            return redirect ('quotation_dashboard')
    else:
        messages.info(request, "You do not have an active Order!")
        return redirect ('quotation_dashboard')
    return redirect ('quotation_dashboard')

def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    Order_qs = Order.objects.filter(user=request.user, ordered= False)
    if Order_qs.exists():
        order = Order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user = request.user, ordered = False)[0]
            if order_item.quantity >1:
                order_item.quantity -=1
                order_item.save()
                item.save()
            else:
                order.items.remove(order_item)
                item.save()
            return redirect("quotation_dashboard")
        else:
            return redirect("quotation_dashboard")
    else:
        messages.info(request, "You do not have an active order!")
    return redirect('quotation_dashboard')

def suspend_order(request):
    order = Order.objects.get(user=request.user, ordered = False)
    orderitems = order.items.all()
    #Making sure that ordered items are un checked to allow new items start form 1 on new order
    for orderitem in orderitems:
        orderitem.ordered = True
        orderitem.save()
    order.delete()
    return redirect('quotation_dashboard')

def complete_quotation(request):
    order_items = OrderItem.objects.filter(user = request.user, ordered = False)
    for order_item in order_items:
        order_item.ordered_item_price = order_item.price
        order_item.ordered_items_total = order_item.amount
        order_item.ordered = True
        order_item.save()
    order = Order.objects.get(user = request.user, ordered = False)
    order.customer.total_quotations +=1
    order.status = 'Pending'
    order.customer.save()
    order.order_total_cost = order.order_total_due()
    order.markup_value = order.get_markup_value
    order.labour_cost = order.get_labour_value()
    order.labour_p = order.labour
    order.vat_cost = order.get_vat_value()
    order.vat_p = order.vat_rate
    order.code = order.get_code()
    order.ordered = True
    order.save()
    
    return redirect("quotation_dashboard")

def add_customer_to_quotation(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(user = request.user, ordered = False)
            selected_customer = request.POST.get('customer_name')
            order.customer = Customer.objects.get(name=selected_customer)
            order.save()
            return redirect("quotation_dashboard")
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("quotation_dashboard")
        return None

def change_markup(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(user = request.user, ordered = False)
            selected_markup = request.POST.get('markup')
            order.markup = selected_markup
            order.save()
            return redirect("quotation_dashboard")
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("quotation_dashboard")
        return None
  
def add_expire_date_to_quotation(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(user = request.user, ordered = False)
            selected_expire_date = request.POST.get('expire_date')
            order.expire_date = selected_expire_date
            order.save()
            return redirect("quotation_dashboard")
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("quotation_dashboard")
        return None

def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect("quotation_dashboard")

def quotation_summery(request, id):
    current_quotation = get_object_or_404(Order, id=id)
    time_now = datetime.datetime.today()
    order_item = OrderItem.objects.filter(user = request.user, ordered = False)
    for order_item in order_item:
        order_item.ordered = True
        order_item.save()
    context = {
        'current_quotation':current_quotation,
        'time_now':time_now,
        'header': 'Orders',
        'config':config,
    }
    return render(request, 'quotations/quotation_summery.html', context)

@login_required
def quotation_list(request):
    quotations = Order.objects.all()
    context = {
    'quotations': quotations,
    'header': 'Manage Quotations',
    'config':config,
    }
    return render(request, 'quotations/quotation_list.html',context)

@login_required
def quotation_update(request, id):
    quotation = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        form = UpdateQuotationForm(request.POST, instance=quotation)
    else:
        form = UpdateQuotationForm(instance=quotation)
    return save_all_quotations(request, form, 'quotations/quotation_update.html')

@login_required
def quotation_delete(request, id):
    data = dict()
    quotation = get_object_or_404(Order, id=id)
    if request.method == "POST":
        quotation.delete()
        data['form_is_valid'] = True
        quotations = Order.objects.all()
        data['quotation_list'] = render_to_string('quotations/quotation_list_2.html', {'quotations': quotations})
    else:
        context = {'quotation': quotation}
        data['html_form'] = render_to_string('quotations/quotation_delete.html', context, request=request)
    return JsonResponse(data)

@login_required
def save_all_quotations(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            quotations = Order.objects.all()
            data['quotation_list'] = render_to_string('quotations/quotation_list_2.html', {'quotations': quotations})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return CustomUser.objects.filter(id__in=user_id_list)

def get_items_in_order(request):
    return OrderItem.objects.filter(user = request.user, ordered = False).count()
