from rest_framework import serializers
from .models import Income, Outcome
from accounting_plan.models import Main


class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    # accounting_main = MainSerializer(many=False)

    class Meta:
        model = Income
        fields = '__all__'


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'
