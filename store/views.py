from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction

from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, Wishlist
from .forms import ReviewForm, CheckoutForm


def home(request):
    featured = Product.objects.filter(is_featured=True)[:8]
    categories = Category.objects.all()
    latest = Product.objects.all()[:8]
    return render(request, "store/home.html", {
        "featured": featured,
        "categories": categories,
        "latest": latest,
    })


def product_list(request):
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")
    sort = request.GET.get("sort", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "name":
        products = products.order_by("name")
    else:
        products = products.order_by("-created_at")

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "selected_category": category_slug,
        "sort": sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.select_related("user").all()
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    review_form = ReviewForm()
    user_has_reviewed = False
    in_wishlist = False

    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

        if request.method == "POST" and not user_has_reviewed:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, "Thanks! Your review has been posted.")
                return redirect("store:product_detail", slug=slug)

    return render(request, "store/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "related": related,
        "review_form": review_form,
        "user_has_reviewed": user_has_reviewed,
        "in_wishlist": in_wishlist,
    })


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request.user)
    quantity = int(request.POST.get("quantity", 1)) if request.method == "POST" else 1

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'"{product.name}" added to your cart.')
    return redirect(request.POST.get("next") or "store:cart")


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get("action")

    if action == "increase":
        item.quantity += 1
        item.save()
    elif action == "decrease":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
    elif action == "remove":
        item.delete()

    return redirect("store:cart")


@login_required
def cart_view(request):
    cart = _get_or_create_cart(request.user)
    return render(request, "store/cart.html", {"cart": cart})


@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)
    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("store:product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = cart.total_price
                order.save()

                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        price=item.product.current_price,
                        quantity=item.quantity,
                    )
                    item.product.stock = max(item.product.stock - item.quantity, 0)
                    item.product.save()

                cart.items.all().delete()
            messages.success(request, f"Order {order.order_number} placed successfully!")
            return redirect("store:order_success", order_number=order.order_number)
    else:
        form = CheckoutForm(initial={"full_name": request.user.get_full_name() or request.user.username})

    return render(request, "store/checkout.html", {"cart": cart, "form": form})


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "store/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "store/order_detail.html", {"order": order})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        messages.success(request, f'"{product.name}" added to wishlist.')
    return redirect("store:product_detail", slug=product.slug)


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "store/wishlist.html", {"items": items})
