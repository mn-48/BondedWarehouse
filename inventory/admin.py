from django.contrib import admin
from .models import Supplier, Category, Product, Warehouse, Stock, StockMovement, HSCode, BondLicense, ImportDeclaration, ExportDeclaration, IOCO


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "supplier", "unit_price", "is_active")
    list_filter = ("category", "supplier", "is_active")
    search_fields = ("sku", "name")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name", "location")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "updated_at")
    list_filter = ("warehouse", "product")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "movement_type", "quantity", "reason", "document_number", "created_at")
    list_filter = ("movement_type", "reason", "warehouse", "product")


@admin.register(HSCode)
class HSCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description")


@admin.register(BondLicense)
class BondLicenseAdmin(admin.ModelAdmin):
    list_display = ("license_number", "warehouse", "issue_date", "expiry_date")
    search_fields = ("license_number",)
    list_filter = ("warehouse",)


@admin.register(ImportDeclaration)
class ImportDeclarationAdmin(admin.ModelAdmin):
    list_display = ("bill_of_entry_no", "bill_of_entry_date", "supplier", "hs_code", "declared_quantity")
    search_fields = ("bill_of_entry_no",)
    list_filter = ("hs_code", "supplier")


@admin.register(ExportDeclaration)
class ExportDeclarationAdmin(admin.ModelAdmin):
    list_display = ("export_number", "export_date", "bond_license", "destination_country")
    search_fields = ("export_number",)
    list_filter = ("bond_license",)


@admin.register(IOCO)
class IOCOAdmin(admin.ModelAdmin):
    list_display = ("product", "hs_code", "input_quantity", "output_quantity", "effective_date")
    list_filter = ("hs_code",)
