"""
Runs automatically during Vercel's build step (see pyproject.toml).
- Applies database migrations
- Seeds sample categories/products (safe to run repeatedly)
- Creates a superuser from environment variables, if provided and not already created
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User


def main():
    print("Applying migrations...")
    call_command("migrate", interactive=False)

    print("Seeding sample data (if not already present)...")
    try:
        call_command("seed_data")
    except Exception as e:
        print("Seed step skipped:", e)

    admin_user = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    admin_pass = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    admin_email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

    if admin_user and admin_pass:
        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(admin_user, admin_email, admin_pass)
            print(f"Superuser '{admin_user}' created.")
        else:
            print(f"Superuser '{admin_user}' already exists.")
    else:
        print("DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not set — skipping admin creation.")

    print("Build script finished.")


if __name__ == "__main__":
    main()
