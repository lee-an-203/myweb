# myshop/views_admin.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User

from .models import Order, OrderDetail, Product

@staff_member_required
def admin_dashboard(request):
    today = now().date()
    current_month = today.month
    current_year = today.year

    # Doanh thu hôm nay / tháng / năm
    revenue_today = Order.objects.filter(create_date=today, status=1).aggregate(total=Sum('total_amount'))['total'] or 0
    revenue_month = Order.objects.filter(create_date__month=current_month, create_date__year=current_year, status=1).aggregate(total=Sum('total_amount'))['total'] or 0
    revenue_year = Order.objects.filter(create_date__year=current_year, status=1).aggregate(total=Sum('total_amount'))['total'] or 0

    # Số đơn hàng hôm nay / tháng / năm
    orders_today = Order.objects.filter(create_date=today, status=1).count()
    orders_month = Order.objects.filter(create_date__month=current_month, create_date__year=current_year, status=1).count()
    orders_year = Order.objects.filter(create_date__year=current_year, status=1).count()

    # Sản phẩm bán chạy (top 5)
    top_products = (OrderDetail.objects
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5])

    # Người dùng mới trong tháng
    new_users = User.objects.filter(date_joined__month=current_month, date_joined__year=current_year).count()

    context = {
        'revenue_today': revenue_today,
        'revenue_month': revenue_month,
        'revenue_year': revenue_year,
        'orders_today': orders_today,
        'orders_month': orders_month,
        'orders_year': orders_year,
        'top_products': top_products,
        'new_users': new_users,
    }
    return render(request, 'admin_dashboard.html', context)
