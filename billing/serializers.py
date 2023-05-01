from rest_framework.serializers import ModelSerializer

from accounting.serializer import PlanSerializer
from .models import BillLine, BillLineTax, Partner, CustomerBill, SupplierBill
from treasury.models import Currency


# this serializer is to avoid circular import when import it from treasury app
class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PartnerSerializer(ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class CustomerBillSerializer(ModelSerializer):
    partner = PartnerSerializer(many=False, read_only=True)
    account = PlanSerializer(many=False, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = CustomerBill
        fields = ['id', 'bill_at', 'deadline_at', 'partner', 'rate', 'amount', 'amount_foreign', 'account', 'currency',
                  'label', 'reference', 'is_lettered', 'is_paid']


class SupplierBillSerializer(ModelSerializer):
    class Meta:
        model = SupplierBill
        fields = '__all__'


class BillLineTaxSerializer(ModelSerializer):
    class Meta:
        model = BillLineTax
        fields = ['id', 'tax', 'tax_amount']


class BillLineSerializer(ModelSerializer):
    account = PlanSerializer(many=False, read_only=True)
    bill_line_tax = BillLineTaxSerializer(many=True, read_only=True)

    class Meta:
        model = BillLine
        fields = ['id', 'label', 'account', 'quantity', 'price', 'price_with_tax', 'bill_line_tax']
