from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Wishlist, Cart, CartItem, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_price", "stock", "is_featured", "created_at")
    list_filter = ("category", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "added_at")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "full_name", "city", "status", "payment_method", "total_amount", "created_at")
    list_filter = ("status", "payment_method", "city")
    search_fields = ("order_number", "full_name", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("order_number", "user", "total_amount", "created_at")


admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.site_header = "ShopNest Administration"
admin.site.site_title = "ShopNest Admin"
admin.site.index_title = "Manage your store"
