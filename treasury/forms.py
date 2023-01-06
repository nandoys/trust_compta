from django.forms import ModelForm, Form
from django.utils import timezone
from django import forms
from django.forms.widgets import TextInput, NumberInput, Select, DateInput
from .models import Currency, CurrencyDailyRate, Outcome
from accounting_plan.models import Main, Adjunct


class OutcomeModelForm(ModelForm):
    class Meta:
        model = Outcome
        fields = ['accounting_main', 'accounting_additional', 'slip_number', 'amount', 'out_at',
                  'more']
        labels = {
            'accounting_main': 'Compte principal',
            'slip_number': '# de bordereau',
            'amount': 'Montant',
            'out_at': 'Date de la sortie',
            'more': 'Autres détails'
        }
        widgets = {
            'accounting_main': Select(attrs={'id': 'accounting-field', 'class': 'form-select mb-3',
                                             'data-placeholder': 'Entrez le compte', 'required': True,
                                             'data-choices': True,
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


class OutcomeForm(Form):
    accounting_main = forms.ModelChoiceField(label='Compte principal', queryset=Main.objects.filter(account_type='decaissement'),
                                             empty_label='Entrez un compte principal',
                                             widget=forms.widgets.Select(
                                                 attrs={'class': 'form-select', 'data-choices': True,
                                                        'id': 'accounting-field'}))

    slip_number = forms.CharField(label='Numéro bordereau', widget=forms.widgets.TextInput(
        attrs={'id': 'slip-number-field', 'class': 'form-control',
               'placeholder': 'Entrez le numéro de bordereau', 'required': True}))

    amount = forms.FloatField(label='Montant',
                              widget=forms.widgets.NumberInput(attrs={'id': 'amount-field', 'class': 'form-control',
                                                                      'placeholder': 'Entrez le montant',
                                                                      'required': True}))

    out_at = forms.DateField(label="Date de l'opération", initial=timezone.now(), localize=True,
                             widget=forms.widgets.DateInput(
                                 attrs={'data-provider': 'flatpickr', 'data-date-format': 'd/m/Y',
                                        'data-deafult-date': 'Your Default Date', 'class': 'form-control',
                                        'placeholder': "Entrez la date de l'opération"}))

    more = forms.CharField(label="Description",
                           widget=forms.widgets.TextInput(attrs={'placeholder': 'Entrez une description', 'class': 'form-control'}))


class IncomeForm(Form):
    accounting_main = forms.ModelChoiceField(label='Compte principal', queryset=Main.objects.filter(account_type='encaissement'),
                                             empty_label='Entrez un compte principal',
                                             widget=forms.widgets.Select(
                                                 attrs={'class': 'form-select', 'data-choices': True,
                                                        'id': 'accounting-field'}))

    slip_number = forms.CharField(label='Numéro bordereau', widget=forms.widgets.TextInput(
        attrs={'id': 'slip-number-field', 'class': 'form-control',
               'placeholder': 'Entrez le numéro de bordereau', 'required': True}))

    amount = forms.FloatField(label='Montant',
                              widget=forms.widgets.NumberInput(attrs={'id': 'amount-field', 'class': 'form-control',
                                                                      'placeholder': 'Entrez le montant',
                                                                      'required': True}))

    in_at = forms.DateField(label="Date de l'opération", initial=timezone.now(), localize=True,
                             widget=forms.widgets.DateInput(
                                 attrs={'data-provider': 'flatpickr', 'data-date-format': 'd/m/Y',
                                        'data-deafult-date': 'Your Default Date', 'class': 'form-control',
                                        'placeholder': "Entrez la date de l'opération"}))

    more = forms.CharField(label="Description",
                           widget=forms.widgets.TextInput(attrs={'placeholder': 'Entrez une description', 'class': 'form-control'}))
