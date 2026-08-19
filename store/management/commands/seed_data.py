from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Seed sample categories and products for demo purposes"

    def handle(self, *args, **options):
        categories_data = [
            ("Kitchen", "🍳", "Cookware, cutlery and kitchen essentials"),
            ("Home Decor", "🏺", "Decor pieces to style your space"),
            ("Furniture", "🪑", "Functional and stylish furniture"),
            ("Lighting", "💡", "Lamps and lighting fixtures"),
            ("Textiles", "🧺", "Cushions, throws and linens"),
            ("Storage", "📦", "Baskets, boxes and organizers"),
        ]

        categories = {}
        for name, icon, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon, "description": desc})
            categories[name] = cat

        products_data = [
            ("Cast Iron Skillet 12\"", "Kitchen", 4500, 3800, 20, "Pre-seasoned cast iron skillet, perfect for stovetop and oven cooking.", True),
            ("Ceramic Dinner Set (16pc)", "Kitchen", 8900, None, 12, "Hand-glazed ceramic dinnerware set for everyday dining.", True),
            ("Wooden Chopping Board", "Kitchen", 2200, None, 30, "Solid acacia wood board, gentle on knife edges.", False),
            ("Copper Pour-Over Kettle", "Kitchen", 5600, 4900, 8, "Precision-spout kettle for slow, even pour-over brewing.", True),
            ("Woven Storage Basket", "Storage", 3200, None, 25, "Handwoven seagrass basket for blankets or laundry.", False),
            ("Stackable Glass Jars (Set of 4)", "Storage", 1800, None, 40, "Airtight glass jars for pantry organization.", False),
            ("Linen Throw Pillow Cover", "Textiles", 1500, 1200, 35, "Soft-washed linen cover in a natural weave.", True),
            ("Chunky Knit Throw Blanket", "Textiles", 6200, None, 15, "Oversized cable-knit throw for the couch or bed.", False),
            ("Rattan Pendant Light", "Lighting", 7400, 6500, 10, "Handwoven rattan shade pendant light, warm ambient glow.", True),
            ("Brass Table Lamp", "Lighting", 5200, None, 18, "Minimalist brass lamp with a linen shade.", False),
            ("Solid Oak Side Table", "Furniture", 12500, 10900, 6, "Compact side table in solid oak with a natural finish.", True),
            ("Boucle Accent Chair", "Furniture", 24500, None, 4, "Curved accent chair upholstered in boucle fabric.", True),
            ("Ceramic Vase Trio", "Home Decor", 3900, None, 22, "Set of three matte ceramic vases in varying heights.", False),
            ("Handblown Glass Candle Holders", "Home Decor", 2600, 2100, 28, "Set of two handblown glass tealight holders.", False),
            ("Macrame Wall Hanging", "Home Decor", 3300, None, 14, "Handknotted cotton macrame for a textured wall accent.", True),
            ("Marble Coasters (Set of 4)", "Home Decor", 2100, None, 33, "Polished marble coasters with cork backing.", False),
        ]

        created = 0
        for name, cat_name, price, discount, stock, desc, featured in products_data:
            if not Product.objects.filter(name=name).exists():
                Product.objects.create(
                    category=categories[cat_name],
                    name=name,
                    price=price,
                    discount_price=discount,
                    stock=stock,
                    description=desc,
                    is_featured=featured,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(categories_data)} categories and {created} products."))
