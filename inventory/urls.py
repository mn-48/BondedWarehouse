from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet,
    CategoryViewSet,
    ProductViewSet,
    WarehouseViewSet,
    StockViewSet,
    StockMovementViewSet,
    HSCodeViewSet,
    BondLicenseViewSet,
    ImportDeclarationViewSet,
    ExportDeclarationViewSet,
    IOCOViewSet,
)


router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stock', StockViewSet, basename='stock')
router.register(r'movements', StockMovementViewSet)
router.register(r'hs-codes', HSCodeViewSet)
router.register(r'bond-licenses', BondLicenseViewSet)
router.register(r'import-declarations', ImportDeclarationViewSet)
router.register(r'export-declarations', ExportDeclarationViewSet)
router.register(r'ioco', IOCOViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

