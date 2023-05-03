from rest_framework.serializers import ModelSerializer

from accounting.serializer import PlanSerializer
from treasury.models import Currency
from .models import Journal, JournalType


# this serializer is to avoid circular import when import it from treasury app
class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class JournalTypeSerializer(ModelSerializer):
    class Meta:
        model = JournalType
        fields = '__all__'


class JournalSerializer(ModelSerializer):
    account = PlanSerializer(many=False, read_only=True)
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = Journal
        fields = ['id', 'name', 'account', 'type_journal', 'currency', 'is_active']
