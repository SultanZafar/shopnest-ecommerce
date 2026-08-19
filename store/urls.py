from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),

    path("checkout/", views.checkout, name="checkout"),
    path("order/success/<str:order_number>/", views.order_success, name="order_success"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<str:order_number>/", views.order_detail, name="order_detail"),

    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
]
