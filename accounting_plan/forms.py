from django.forms import ModelForm
from django.forms.widgets import TextInput, HiddenInput, Select, DateInput, NumberInput, DateTimeInput
from .models import Main, Additional, Adjunct, Budget, FiscalYear


class MainAccountingForm(ModelForm):
    class Meta:
        model = Main
        fields = '__all__'
        labels = {
            'account_number': 'Numéro du compte',
            'account_name': 'Intitulé du compte',
            'account_type': 'Classification',
            'account_description': 'Description'
        }
        widgets = {
            'id': HiddenInput(),
            'account_number': TextInput(
                attrs={'id': 'accounting-number-field', 'class': 'form-control',
                       'placeholder': 'Entrez le numéro de compte', 'required': True}),

            'account_name': TextInput(attrs={'id': 'accounting-name-field', 'class': 'form-control',
                                             'placeholder': "Entrez l'intitulé du compte", 'required': True}),

            'account_type': Select(
                attrs={'id': 'accounting-type-field', 'class': 'form-control', 'name': 'accounting-type-field',
                       'data-trigger': True}),

            'account_description': TextInput(attrs={'id': 'accounting-desc-field', 'class': 'form-control',
                                                    'placeholder': "Entrez la description du compte",
                                                    'required': True}),
        }


class AdditionalAccountingForm(ModelForm):
    class Meta:
        model = Additional
        fields = ['account_number', 'account_name', 'account_description']
        labels = {
            'account_number': 'Numéro du compte',
            'account_name': 'Intitulé du compte',
            'account_description': 'Description'
        }

        widgets = {
            'id': HiddenInput(),
            'account_number': TextInput(
                attrs={'id': 'accounting-number-field', 'class': 'form-control',
                       'placeholder': 'Entrez le numéro de compte', 'required': True}),

            'account_name': TextInput(attrs={'id': 'accounting-name-field', 'class': 'form-control',
                                             'placeholder': "Entrez l'intitulé du compte", 'required': True}),

            'account_description': TextInput(attrs={'id': 'accounting-desc-field', 'class': 'form-control',
                                                    'placeholder': "Entrez la description du compte",
                                                    'required': True}),
        }


class AdjunctAccountingForm(ModelForm):
    class Meta:
        model = Adjunct
        fields = ['adjunct_account_name']
        labels = {
            'adjunct_account_name': 'Libellé'
        }
        widgets = {
            'adjunct_account_name': TextInput(attrs={'id': 'adjunct-accounting-field', 'class': 'form-control',
                                             'placeholder': 'Entrez le libellé', 'required': True})
        }


class FiscalYearForm(ModelForm):
    class Meta:
        model = FiscalYear
        fields = ['year', 'rate']
        labels = {
            'year': 'Année',
            'rate': 'Taux budgetaire'
        }
        widgets = {
            'year': NumberInput(attrs={'id': 'year-field', 'class': 'form-control',
                                       'placeholder': "Entrez l'année",
                                       'required': True}),
            'rate': NumberInput(attrs={'id': 'year-field', 'class': 'form-control',
                                       'placeholder': "Entrez le taux budgetaire",
                                       'required': True})
        }


class BudgetAccountingForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'warning_at']
        labels = {
            'amount': 'Montant',
            'warning_at': "M'avertir à partir de "
        }

        widgets = {
            'amount': NumberInput(attrs={'id': 'amount-field', 'class': 'form-control',
                                         'placeholder': "Entrez le montant",
                                         'required': True}),
            'warning_at': NumberInput(attrs={'id': 'warning-field', 'class': 'form-control',
                                             'placeholder': "Entrez le seuil à surveiller",
                                             'required': True})
        }
