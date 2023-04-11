from rest_framework.serializers import ModelSerializer

from .models import Main, Additional, Plan


class MainSerializer(ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'


class AdditionalSerializer(ModelSerializer):
    class Meta:
        model = Additional
        fields = '__all__'


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'account_number', 'account_namen']

        extra_kwargs = {
            'path': {'write_only': True},
            'depth': {'write_only': True},
            'numchild': {'write_only': True},
            'group': {'write_only': True},
        }
