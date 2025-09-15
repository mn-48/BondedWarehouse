from django.core.management.base import BaseCommand
from inventory.models import Supplier, Category, Product, Warehouse, StockMovement


class Command(BaseCommand):
    help = "Seed initial data for the inventory system"

    def handle(self, *args, **options):
        supplier, _ = Supplier.objects.get_or_create(name="Default Supplier")
        cat, _ = Category.objects.get_or_create(name="General")
        wh, _ = Warehouse.objects.get_or_create(name="Main Warehouse", location="HQ")

        products = [
            ("SKU-001", "Item A", 10.00),
            ("SKU-002", "Item B", 25.50),
            ("SKU-003", "Item C", 5.75),
        ]
        for sku, name, price in products:
            product, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    "name": name,
                    "category": cat,
                    "supplier": supplier,
                    "unit_price": price,
                },
            )
            StockMovement.objects.create(
                product=product,
                warehouse=wh,
                movement_type=StockMovement.INBOUND,
                quantity=100,
                reference="Initial stock",
            ).apply()

        self.stdout.write(self.style.SUCCESS("Seed data created."))

