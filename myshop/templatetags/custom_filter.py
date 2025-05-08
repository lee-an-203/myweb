from django import template
from django.utils import timezone
from numpy import prod
from myshop.models import Promotion, Product, Order

register = template.Library()


@register.filter
def check_product_sale(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id=product_id,  # product_id có trong bảng promotion hay không
            start_date__lte=timezone.now(),  # ngày bắt dầu kmai < ngày hiện tại (trước ngày hiện tại)
            end_date__gt=timezone.now(),  # ngày kết thúc kmai > ngày hiện tại
        )
        return True
    except Promotion.DoesNotExist:
        return False


@register.filter
def get_price_sale(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id=product_id,  
            start_date__lte=timezone.now(), 
            end_date__gt=timezone.now(),  
        )
        return int(
            (1 - product_in_promotion.discount / 100)
            * product_in_promotion.product.price
        )
    except Promotion.DoesNotExist:
        return ""


@register.filter
def get_price(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id=product_id,  
            start_date__lte=timezone.now(),  
            end_date__gt=timezone.now(),  
        )
        return int(
            (1 - product_in_promotion.discount / 100)
            * product_in_promotion.product.price
        )
    except Promotion.DoesNotExist:
        product = Product.objects.get(id=product_id)
        return int(product.price)


@register.filter
def get_product_discount(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id=product_id,  
            start_date__lte=timezone.now(),  
            end_date__gt=timezone.now(),  
        )
        return product_in_promotion.discount
    except Promotion.DoesNotExist:
        return ""


@register.filter
def getattribute(obj, arg):
    if hasattr(obj, str(arg)):
        return getattr(obj, str(arg))


@register.filter
def getlabel(obj, arg):
    if hasattr(obj, str(arg)):
        return obj._meta.get_field(arg).verbose_name


@register.filter
def count_product_in_card(logged_user):
    try:
        user_ordered = Order.objects.get(
            user=logged_user, status=0
        )  # Đếm sản phẩm của đơn hàng chưa thành công
        return sum([item.quantity for item in user_ordered.orderdetail_set.all()])
    except:
        return 0


@register.filter
def message_alert(product_id):
    product = Product.objects.get(id=product_id)
    if product.stock_quantity > 0:
        return "Bạn đã thêm sản phẩm thành công"
    else:
        return "Bạn không thể thêm sản phẩm này"


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""
