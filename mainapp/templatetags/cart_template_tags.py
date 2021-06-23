from django import template
from mainapp.models import Order,Item, ItemCategory, OrderItem, CustomUser
import datetime
from djmoney.money import Money
from constance import config
from django.template.loader import get_template
from django.contrib.sessions.models import Session
from django.utils import timezone


register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered = False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def total_sales_query(user):
    sales = Order.objects.filter(ordered = True).all()
    total_sales = 0
    for sales in sales:
        total_sales += sales.get_total()
    return total_sales

@register.filter
def expected_total_sale(user):
    items = Item.objects.all()
    expected_total_sale = 0
    for item in items:
        expected_total_sale += item.expected_total_sale
    return expected_total_sale

     
@register.filter
def todays_sale(user):
    today = datetime.datetime.today()
    todays_sales = Order.objects.filter(ordered=True).filter(order_date = today)
    todays_total_sales = Money('0.00','MWK')
    for todays_s in todays_sales:
        todays_total_sales += todays_s.get_after_tax_final_price()
        return todays_total_sales
    else:
        return todays_total_sales
    
# def show_loggedin_users():
#     users = get_current_users()
#     return {'users': users}

# users_template = get_template('logged_in_users.html')
# register.inclusion_tag(users_template)(show_loggedin_users)

# def get_current_users():
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     user_id_list = []
#     for session in active_sessions:
#         data = session.get_decoded()
#         user_id_list.append(data.get('_auth_user_id', None))
#     # Query all logged in users based on id list
#     return CustomUser.objects.filter(id__in=user_id_list)
