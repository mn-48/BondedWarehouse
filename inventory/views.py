from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier, Category, Product, Warehouse, Stock, StockMovement, HSCode, BondLicense, ImportDeclaration, ExportDeclaration, IOCO
from .serializers import (
    SupplierSerializer,
    CategorySerializer,
    ProductSerializer,
    WarehouseSerializer,
    StockSerializer,
    StockMovementSerializer,
    HSCodeSerializer,
    BondLicenseSerializer,
    ImportDeclarationSerializer,
    ExportDeclarationSerializer,
    IOCOSerializer,
)
from django.shortcuts import render


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all().order_by("name")
    serializer_class = WarehouseSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related("product", "warehouse").all()
    serializer_class = StockSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related("product", "warehouse").all()
    serializer_class = StockMovementSerializer

    def perform_create(self, serializer):
        movement = serializer.save()
        movement.apply()

    @action(detail=False, methods=["post"], url_path="adjust")
    def adjust(self, request):
        serializer = StockMovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movement = serializer.save()
        movement.apply()
        return Response(StockMovementSerializer(movement).data, status=status.HTTP_201_CREATED)


class HSCodeViewSet(viewsets.ModelViewSet):
    queryset = HSCode.objects.all().order_by("code")
    serializer_class = HSCodeSerializer


class BondLicenseViewSet(viewsets.ModelViewSet):
    queryset = BondLicense.objects.select_related("warehouse").all()
    serializer_class = BondLicenseSerializer


class ImportDeclarationViewSet(viewsets.ModelViewSet):
    queryset = ImportDeclaration.objects.select_related("supplier", "hs_code", "bond_license").all()
    serializer_class = ImportDeclarationSerializer


class ExportDeclarationViewSet(viewsets.ModelViewSet):
    queryset = ExportDeclaration.objects.select_related("bond_license").all()
    serializer_class = ExportDeclarationSerializer


class IOCOViewSet(viewsets.ModelViewSet):
    queryset = IOCO.objects.select_related("product", "hs_code").all()
    serializer_class = IOCOSerializer


def dashboard(request):
    stats = {
        'products': Product.objects.count(),
        'warehouses': Warehouse.objects.count(),
        'stock_items': Stock.objects.count(),
        'movements': StockMovement.objects.count(),
    }
    return render(request, 'dashboard.html', {'stats': stats})


def products_page(request):
    items = Product.objects.select_related('category', 'supplier', 'hs_code').all()[:200]
    return render(request, 'products.html', {'items': items})


def stock_page(request):
    items = Stock.objects.select_related('product', 'warehouse').all()[:500]
    return render(request, 'stock.html', {'items': items})


def movements_page(request):
    items = StockMovement.objects.select_related('product', 'warehouse').order_by('-created_at')[:200]
    return render(request, 'movements.html', {'items': items})

# Create your views here.
