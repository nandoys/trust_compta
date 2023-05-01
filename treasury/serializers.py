from rest_framework import serializers

from accounting.serializer import PlanSerializer
from billing.serializers import PartnerSerializer, BillLineSerializer, CustomerBillSerializer
from .models import Income, Outcome, AccountingEntry, Currency
from accounting.models import Main


class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    accounting_main = MainSerializer(many=False)

    class Meta:
        model = Income
        fields = '__all__'


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class AccountingEntrySerializer(serializers.ModelSerializer):
    account = PlanSerializer(many=False, read_only=True)
    partner = PartnerSerializer(many=False, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)
    ref_billing_customer = CustomerBillSerializer(many=False, read_only=True)
    ref_bill_line = BillLineSerializer(many=False, read_only=True)

    class Meta:
        model = AccountingEntry
        fields = ['id', 'account', 'date_at', 'label', 'partner', 'rate', 'currency', 'debit', 'credit',
                  'amount_foreign', 'ref_billing_customer', 'ref_billing_supplier', 'ref_bill_line', 'is_verified']
