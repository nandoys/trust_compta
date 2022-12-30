from django.forms import ModelForm
from django.forms.widgets import TextInput, NumberInput, Select, DateInput
from .models import Currency, CurrencyDailyRate, Outcome
from accounting_plan.models import Adjunct


class OutcomeForm(ModelForm):
    class Meta:
        model = Outcome
        fields = ['accounting', 'slip_number', 'amount', 'out_at', 'more']
        labels = {
            'accounting': 'Compte associé',
            'slip_number': '# de bordereau',
            'amount': 'Montant',
            'out_at': 'Date de la sortie',
            'more': 'Autres détails'
        }
        widgets = {
            'accounting': Select(attrs={'id': 'accounting-field', 'class': 'form-select mb-3',
                                        'data-placeholder': 'Entrez le compte', 'required': True, 'data-choices': True,
                                        'data-choices-removeItem': True}),
            'slip_number': TextInput(attrs={'id': 'slip-number-field', 'class': 'form-control',
                                            'placeholder': 'Entrez le numéro de bordereau', 'required': True}),
            'amount': NumberInput(attrs={'id': 'amount-field', 'class': 'form-control',
                                         'placeholder': 'Entrez le montant', 'required': True}),
            'out_at': DateInput(attrs={'id': 'out_at-field', 'class': 'form-control',
                                       'placeholder': 'Entrez la date', 'required': True}),
            'more': TextInput(attrs={'id': 'more-field', 'class': 'form-control',
                                     'placeholder': 'Entrez une description'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



