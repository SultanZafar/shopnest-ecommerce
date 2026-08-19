# ShopNest — Django E-Commerce Store (FYP Project)

A full-featured e-commerce web application built with Django. Includes product catalog, cart, checkout, order tracking, reviews, wishlist, and a full admin panel — ready to showcase as a final year project.

## Features

- **Authentication**: Register, login, logout, profile page
- **Product catalog**: Categories, search, price filter, sorting, pagination
- **Product detail**: Ratings & reviews, related products, discount pricing, stock status
- **Cart**: Add / increase / decrease / remove items, live cart count in navbar
- **Checkout**: Shipping form, Cash on Delivery or Card, auto-generated order number
- **Orders**: Order history, order detail/tracking with status (pending → delivered)
- **Wishlist**: Save products, toggle from product page
- **Admin panel**: Full CRUD for products, categories, orders (with inline order items), reviews, wishlist — customized with ShopNest branding
- **Custom design**: Tailwind CSS with a bespoke forest-green / clay color palette and Fraunces + Inter typography (not a default template look)

## Tech Stack

- Python 3, Django 6
- SQLite (default, zero setup)
- Tailwind CSS (via CDN, no build step needed)
- Pillow (for product images)

## Setup Instructions

1. **Extract the project and open a terminal inside the folder.**

2. **Install dependencies:**
   ```bash
   pip install django pillow
   ```

3. **Run migrations** (already applied, but run again if you make model changes):
   ```bash
   python manage.py migrate
   ```

4. **Create your own admin account** (a demo one is already included, see below):
   ```bash
   python manage.py createsuperuser
   ```

5. **(Optional) Re-seed sample products/categories:**
   ```bash
   python manage.py seed_data
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Open in browser:**
   - Store: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Demo Admin Login

- Username: `admin`
- Password: `admin12345`

(Change this before showing it to anyone outside your own machine.)

## Project Structure

```
shopnest/
├── core/               # Project settings, root urls
├── store/              # Main app: products, cart, orders, reviews, wishlist
│   ├── models.py        # Category, Product, Cart, Order, Review, Wishlist...
│   ├── views.py          # All storefront logic
│   ├── admin.py          # Admin panel customization
│   └── management/commands/seed_data.py   # Sample data seeder
├── accounts/           # Register / login / logout / profile
├── templates/           # All HTML templates (Tailwind-styled)
├── static/               # Static files
├── media/                # Uploaded product images (created at runtime)
└── manage.py
```

## Notes for Your FYP Report / Demo

- Add product images through the **Admin Panel** (`/admin/`) → Products → edit a product → upload image. Products without an image show a category icon placeholder automatically.
- Payment is simulated (Cash on Delivery / Card selection only, no real payment gateway) — mention this clearly in your report as a "future scope: integrate Stripe/JazzCash/Easypaisa" if your evaluator asks.
- Stock automatically decreases when an order is placed.
- Order status (`pending`, `processing`, `shipped`, `delivered`, `cancelled`) can be updated from the Admin panel — good to demo live during your defense.
- Each user can leave only **one review per product**, and average rating is calculated automatically.

## Suggested Talking Points for Your Defense

1. Custom user-facing cart & checkout flow (not just Django admin CRUD)
2. Search + category + price filtering with pagination
3. Wishlist and review system tied to authenticated users
4. Order lifecycle management from the admin side
5. Clean, distinct UI (not a default Bootstrap template) — shows frontend care
