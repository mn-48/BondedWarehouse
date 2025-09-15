from rest_framework import serializers
from .models import Supplier, Category, Product, Warehouse, Stock, StockMovement, HSCode, BondLicense, ImportDeclaration, ExportDeclaration, IOCO, UOM


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    hs_code_code = serializers.CharField(source="hs_code.code", read_only=True)
    uom_code = serializers.CharField(source="uom.code", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "category",
            "category_name",
            "supplier",
            "supplier_name",
            "description",
            "unit_price",
            "is_active",
            "hs_code",
            "hs_code_code",
            "uom",
            "uom_code",
            "country_of_origin",
            "customs_value",
            "created_at",
            "updated_at",
        ]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product",
            "product_name",
            "warehouse",
            "warehouse_name",
            "quantity",
            "created_at",
            "updated_at",
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"


class HSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSCode
        fields = "__all__"


class BondLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BondLicense
        fields = "__all__"


class ImportDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportDeclaration
        fields = "__all__"


class ExportDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportDeclaration
        fields = "__all__"


class IOCOSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOCO
        fields = "__all__"


class UOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UOM
        fields = "__all__"

