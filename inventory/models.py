from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class Warehouse(TimeStampedModel):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Stock(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self) -> str:
        return f"{self.product} @ {self.warehouse}: {self.quantity}"


class StockMovement(TimeStampedModel):
    INBOUND = 'IN'
    OUTBOUND = 'OUT'
    MOVEMENT_TYPES = (
        (INBOUND, 'Inbound'),
        (OUTBOUND, 'Outbound'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reference = models.CharField(max_length=255, blank=True)

    def apply(self):
        stock, _ = Stock.objects.get_or_create(product=self.product, warehouse=self.warehouse)
        if self.movement_type == self.INBOUND:
            stock.quantity = stock.quantity + int(self.quantity)
        else:
            stock.quantity = stock.quantity - int(self.quantity)
        stock.save()


# ---------------- NBR Bonded Warehouse Models ----------------

class HSCode(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.code} - {self.description}"


class BondLicense(TimeStampedModel):
    license_number = models.CharField(max_length=64, unique=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bond_licenses')

    def __str__(self) -> str:
        return self.license_number


class IOCO(TimeStampedModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ioco_entries')
    hs_code = models.ForeignKey('HSCode', on_delete=models.PROTECT, related_name='ioco_entries')
    input_quantity = models.DecimalField(max_digits=12, decimal_places=4)
    output_quantity = models.DecimalField(max_digits=12, decimal_places=4)
    effective_date = models.DateField()

    class Meta:
        verbose_name = 'Input-Output Coefficient'
        verbose_name_plural = 'Input-Output Coefficients'


class ImportDeclaration(TimeStampedModel):
    bill_of_entry_no = models.CharField(max_length=64, unique=True)
    bill_of_entry_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='import_declarations')
    bond_license = models.ForeignKey(BondLicense, on_delete=models.PROTECT, related_name='import_declarations')
    hs_code = models.ForeignKey(HSCode, on_delete=models.PROTECT, related_name='import_declarations')
    uom = models.CharField(max_length=32, default='PCS')
    declared_quantity = models.DecimalField(max_digits=14, decimal_places=4)
    customs_value = models.DecimalField(max_digits=14, decimal_places=2)
    country_of_origin = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:
        return self.bill_of_entry_no


class ExportDeclaration(TimeStampedModel):
    export_number = models.CharField(max_length=64, unique=True)
    export_date = models.DateField()
    bond_license = models.ForeignKey(BondLicense, on_delete=models.PROTECT, related_name='export_declarations')
    destination_country = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.export_number


# Units of Measure
class UOM(TimeStampedModel):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.code


# Extend Product with NBR fields
Product.add_to_class('hs_code', models.ForeignKey(HSCode, on_delete=models.PROTECT, null=True, blank=True, related_name='products'))
Product.add_to_class('uom', models.ForeignKey(UOM, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'))
Product.add_to_class('country_of_origin', models.CharField(max_length=64, blank=True))
Product.add_to_class('customs_value', models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True))


# Extend StockMovement with NBR reasons and document linkage
class MovementReason(models.TextChoices):
    BONDED_RECEIPT = 'BONDED_RECEIPT', 'Bonded Receipt (Ex-bond)'
    PRODUCTION_ISSUE = 'PRODUCTION_ISSUE', 'Issue to Production'
    EXPORT_DISPATCH = 'EXPORT_DISPATCH', 'Export Dispatch'
    WASTAGE = 'WASTAGE', 'Wastage/Destruction'
    ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'


StockMovement.add_to_class('reason', models.CharField(max_length=32, choices=MovementReason.choices, default=MovementReason.ADJUSTMENT))
StockMovement.add_to_class('document_number', models.CharField(max_length=64, blank=True))
StockMovement.add_to_class('document_date', models.DateField(null=True, blank=True))
StockMovement.add_to_class('import_declaration', models.ForeignKey(ImportDeclaration, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements'))
StockMovement.add_to_class('export_declaration', models.ForeignKey(ExportDeclaration, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements'))
StockMovement.add_to_class('remarks', models.TextField(blank=True))

