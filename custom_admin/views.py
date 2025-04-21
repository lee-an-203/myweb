from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from myshop.models import (
    Category,
    Brand,
    Detail,
    Order,
    OrderDetail,
    Promotion,
    Rating,
    Product,
)
from .forms import (
    BrandForm,
    CategoryForm,
    DetailForm,
    ProductForm,
    OrderForm,
    OrderDetailForm,
    PromotionForm,
    RatingForm,
)
from django.contrib.auth.models import User
from django.db.models import Q

from django.utils.timezone import now
from datetime import date
from django.db.models import Count

from django.db.models.functions import TruncMonth
from django.db.models import Sum
import json


# --- Login check ---
def is_admin(user):
    return user.is_staff


# --- Admin login view ---
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("custom_admin:admin_dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("custom_admin:admin_dashboard")
        else:
            error = (
                "Tài khoản hoặc mật khẩu không đúng, hoặc bạn không có quyền truy cập."
            )

    return render(request, "custom_admin/login.html", {"error": error})


# --- Admin logout ---
def admin_logout(request):
    logout(request)
    return redirect("custom_admin:admin_login")


@login_required(login_url="custom_admin:admin_login")
@user_passes_test(is_admin)
def admin_dashboard(request):
    today = date.today()

    # Thống kê tổng
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_revenue = (
        Order.objects.aggregate(Sum("total_amount"))["total_amount__sum"] or 0
    )

    # Thống kê doanh thu theo ngày, tháng, năm (xử lý chuẩn theo kiểu DateField / DateTimeField)
    revenue_today = (
        Order.objects.filter(create_date=today).aggregate(Sum("total_amount"))[
            "total_amount__sum"
        ]
        or 0
    )
    revenue_month = (
        Order.objects.filter(
            create_date__year=today.year, create_date__month=today.month
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0
    )
    revenue_year = (
        Order.objects.filter(create_date__year=today.year).aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0
    )

    # Số lượng đơn hàng
    orders_today = Order.objects.filter(create_date=today).count()
    orders_month = Order.objects.filter(
        create_date__year=today.year, create_date__month=today.month
    ).count()
    orders_year = Order.objects.filter(create_date__year=today.year).count()

    # Người dùng mới trong tháng
    new_users = User.objects.filter(
        date_joined__year=today.year, date_joined__month=today.month
    ).count()

    # Top sản phẩm bán chạy
    top_products = (
        OrderDetail.objects.values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    # Doanh thu theo tháng (vẽ biểu đồ)
    revenue_by_month = (
        Order.objects.annotate(month=TruncMonth("create_date"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    chart_labels = [entry["month"].strftime("%m/%Y") for entry in revenue_by_month]
    chart_data = [entry["total"] for entry in revenue_by_month]

    context = {
        "total_users": total_users,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "revenue_today": revenue_today,
        "revenue_month": revenue_month,
        "revenue_year": revenue_year,
        "orders_today": orders_today,
        "orders_month": orders_month,
        "orders_year": orders_year,
        "new_users": new_users,
        "top_products": top_products,
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
    }

    return render(request, "custom_admin/admin_dashboard.html", context)


# brand_list
@login_required
@user_passes_test(is_admin)
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, "custom_admin/brand_list.html", {"brands": brands})


@login_required
@user_passes_test(is_admin)
def brand_add(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:brand_list")
    else:
        form = BrandForm()
    return render(
        request, "custom_admin/brand_form.html", {"form": form, "title": "Thêm Brand"}
    )


@login_required
@user_passes_test(is_admin)
def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:brand_list")
    else:
        form = BrandForm(instance=brand)
    return render(
        request,
        "custom_admin/brand_form.html",
        {"form": form, "title": "Chỉnh sửa Brand"},
    )


@login_required
@user_passes_test(is_admin)
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    brand.delete()
    return redirect("custom_admin:brand_list")


# category_list
@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(
        request, "custom_admin/category_list.html", {"categories": categories}
    )


@login_required
@user_passes_test(is_admin)
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:category_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "custom_admin/category_form.html",
        {"form": form, "title": "Thêm Category"},
    )


@login_required
@user_passes_test(is_admin)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "custom_admin/category_form.html",
        {"form": form, "title": "Chỉnh sửa Category"},
    )


@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("custom_admin:category_list")


@login_required
@user_passes_test(is_admin)
def product_list(request):
    query = request.GET.get("q", "")

    products = Product.objects.select_related("category", "brand", "detail")

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query)
        )

    return render(
        request,
        "custom_admin/product_list.html",
        {"products": products, "query": query},
    )


@login_required
@user_passes_test(is_admin)
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:product_list")
    else:
        form = ProductForm()
    return render(
        request,
        "custom_admin/product_form.html",
        {"form": form, "title": "Thêm sản phẩm"},
    )


@login_required
@user_passes_test(is_admin)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "custom_admin/product_form.html",
        {"form": form, "title": "Chỉnh sửa sản phẩm"},
    )


@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("custom_admin:product_list")


@login_required
@user_passes_test(is_admin)
def detail_list(request):
    query = request.GET.get("query", "")
    if query:
        details = Detail.objects.filter(name__icontains=query).all()
    else:
        details = Detail.objects.all()
    return render(
        request, "custom_admin/detail_list.html", {"details": details, "query": query}
    )

    # details = Detail.objects.all()
    # return render(request, 'custom_admin/detail_list.html', {'details': details})


@login_required
@user_passes_test(is_admin)
def detail_add(request):
    if request.method == "POST":
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:detail_list")
    else:
        form = DetailForm()
    return render(
        request,
        "custom_admin/detail_form.html",
        {"form": form, "title": "Thêm cấu hình sản phẩm"},
    )


@login_required
@user_passes_test(is_admin)
def detail_edit(request, pk):
    detail = get_object_or_404(Detail, pk=pk)
    if request.method == "POST":
        form = DetailForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:detail_list")
    else:
        form = DetailForm(instance=detail)
    return render(
        request,
        "custom_admin/detail_form.html",
        {"form": form, "title": "Chỉnh sửa cấu hình sản phẩm"},
    )


@login_required
@user_passes_test(is_admin)
def detail_delete(request, pk):
    detail = get_object_or_404(Detail, pk=pk)
    detail.delete()
    return redirect("custom_admin:detail_list")


@login_required
@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.all()
    return render(request, "custom_admin/order_list.html", {"orders": orders})


@login_required
@user_passes_test(is_admin)
def order_list(request):
    search_query = request.GET.get("search", "")
    orders = Order.objects.all()
    if search_query:
        orders = orders.filter(Q(phone__icontains=search_query))
    return render(
        request,
        "custom_admin/order_list.html",
        {"orders": orders, "search_query": search_query},
    )


@login_required
@user_passes_test(is_admin)
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:order_list")
    else:
        form = OrderForm(instance=order)
    return render(
        request,
        "custom_admin/order_form.html",
        {"form": form, "title": "Chỉnh sửa đơn hàng"},
    )


@login_required
@user_passes_test(is_admin)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect("custom_admin:order_list")


@login_required
@user_passes_test(is_admin)
def order_detail_list(request):
    order_details = OrderDetail.objects.select_related("order", "product").all()
    return render(
        request, "custom_admin/order_detail_list.html", {"order_details": order_details}
    )


@login_required
@user_passes_test(is_admin)
def order_detail_edit(request, pk):
    order_detail = get_object_or_404(OrderDetail, pk=pk)
    if request.method == "POST":
        form = OrderDetailForm(request.POST, instance=order_detail)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:order_detail_list")
    else:
        form = OrderDetailForm(instance=order_detail)
    return render(
        request,
        "custom_admin/order_detail_form.html",
        {"form": form, "title": "Chỉnh sửa chi tiết đơn hàng"},
    )


@login_required
@user_passes_test(is_admin)
def order_detail_delete(request, pk):
    order_detail = get_object_or_404(OrderDetail, pk=pk)
    order_detail.delete()
    return redirect("custom_admin:order_detail_list")


@login_required
@user_passes_test(is_admin)
def promotion_list(request):
    promotions = Promotion.objects.select_related("product").all()
    return render(
        request, "custom_admin/promotion_list.html", {"promotions": promotions}
    )


@login_required
@user_passes_test(is_admin)
def promotion_add(request):
    if request.method == "POST":
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:promotion_list")
    else:
        form = PromotionForm()
    return render(
        request,
        "custom_admin/promotion_form.html",
        {"form": form, "title": "Thêm khuyến mãi"},
    )


@login_required
@user_passes_test(is_admin)
def promotion_edit(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == "POST":
        form = PromotionForm(request.POST, instance=promotion)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:promotion_list")
    else:
        form = PromotionForm(instance=promotion)
    return render(
        request,
        "custom_admin/promotion_form.html",
        {"form": form, "title": "Chỉnh sửa khuyến mãi"},
    )


@login_required
@user_passes_test(is_admin)
def promotion_delete(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    promotion.delete()
    return redirect("custom_admin:promotion_list")


@login_required
@user_passes_test(is_admin)
def rating_list(request):
    ratings = Rating.objects.all()
    return render(request, "custom_admin/rating_list.html", {"ratings": ratings})


@login_required
@user_passes_test(is_admin)
def rating_add(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:rating_list")
    else:
        form = RatingForm()
    return render(
        request,
        "custom_admin/rating_form.html",
        {"form": form, "title": "Thêm đánh giá"},
    )


@login_required
@user_passes_test(is_admin)
def rating_edit(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect("custom_admin:rating_list")
    else:
        form = RatingForm(instance=rating)
    return render(
        request,
        "custom_admin/rating_form.html",
        {"form": form, "title": "Chỉnh sửa đánh giá"},
    )


@login_required
@user_passes_test(is_admin)
def rating_delete(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    rating.delete()
    return redirect("custom_admin:rating_list")
