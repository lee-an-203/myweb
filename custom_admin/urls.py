from django.urls import path
from . import views


app_name = "custom_admin"

urlpatterns = [



    path("admin_dashboard/", views.admin_dashboard, name="dashboard"),

    path("brands/", views.brand_list, name="brand_list"),
    path("brands/add/", views.brand_add, name="brand_add"),
    path("brands/<int:pk>/edit/", views.brand_edit, name="brand_edit"),
    path("brands/<int:pk>/delete/", views.brand_delete, name="brand_delete"),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),


    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),


    path('details/', views.detail_list, name='detail_list'),
    path('details/add/', views.detail_add, name='detail_add'),
    path('details/<int:pk>/edit/', views.detail_edit, name='detail_edit'),
    path('details/<int:pk>/delete/', views.detail_delete, name='detail_delete'),


    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/update-status/', views.order_update_status, name='order_update_status'),
    path('orders/<int:pk>/detail/', views.order_detail, name='order_detail'),


    path('order-details/', views.order_detail_list, name='order_detail_list'),
    path('order-details/<int:pk>/edit/', views.order_detail_edit, name='order_detail_edit'),
    path('order-details/<int:pk>/delete/', views.order_detail_delete, name='order_detail_delete'),


    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/add/', views.promotion_add, name='promotion_add'),
    path('promotions/<int:pk>/edit/', views.promotion_edit, name='promotion_edit'),
    path('promotions/<int:pk>/delete/', views.promotion_delete, name='promotion_delete'),


    path('ratings/', views.rating_list, name='rating_list'),
    path('ratings/add/', views.rating_add, name='rating_add'),
    path('ratings/<int:pk>/edit/', views.rating_edit, name='rating_edit'),
    path('ratings/<int:pk>/delete/', views.rating_delete, name='rating_delete'),

    path('users/', views.user_list, name='user_list'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

]
