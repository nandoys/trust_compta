from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from settings.models import Journal
from treasury.models import AccountingEntry, Currency
from utils.token import set_auth_token
from .models import Partner, CustomerBill, BillLine


def customers(request):
    token = request.COOKIES.get('access_token')

    response = render(request, 'billing/customer.html')

    # verify if there is no token and create one
    if not token:
        set_auth_token(request, response)

    # verify if the existing token is invalid then create one
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.get_validated_token(token)
    except InvalidToken:
        set_auth_token(request, response)

    return response


def suppliers(request):
    token = request.COOKIES.get('access_token')

    response = render(request, 'billing/supplier.html')

    # verify if there is no token and create one
    if not token:
        set_auth_token(request, response)

    # verify if the existing token is invalid then create one
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.get_validated_token(token)
    except InvalidToken:
        set_auth_token(request, response)

    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_partners(request):
    try:
        partners = Partner.objects.all()
        return Response(partners.values('id', 'name'))
    except Partner.DoesNotExist:
        raise NotFound(_("Aucun partenaire trouvé"))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_partner(request):
    data = request.data

    partner = Partner(name=data['name'])
    partner.save()

    message = "Votre partenaire a été créé avec succès"

    return Response({
        'message': message,
        'partner': {'id': partner.id, 'label': partner.name}
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_customer_bills(request):
    try:
        journal_id = request.GET.get('journal')

        journal = Journal.objects.get(id=journal_id)

        bills = CustomerBill.objects.all()

        return Response(
            bills.values('id', 'bill_at', 'deadline_at', 'partner_id', 'partner__name', 'rate', 'amount',
                         'amount_foreign',
                         'account_id', 'account__account_number', 'account__account_name', 'currency__symbol',
                         'currency__name', 'currency__is_local', 'currency_id', 'label', 'reference', 'is_lettered',
                         'is_paid'))
    except Journal.DoesNotExist:
        return Response({'message': "Le journal demandé n'existe pas"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_customer_bill_accounting_entries(request, bill_id):
    entries = []
    try:
        entries = AccountingEntry.objects.filter(ref_billing_customer_id=bill_id, ref_statement__isnull=True).all()
    except AccountingEntry.DoesNotExist:
        pass
    data = []

    for entry in entries:
        partner_name = entry.partner.name if entry.partner is not None else None
        data.append({
            'id': entry.id, 'account_number': entry.account.account_number, 'account_name': entry.account.account_name,
            'date_at': entry.date_at, 'label': entry.label, 'partner_name': partner_name, 'rate': entry.rate,
            'currency_is_local': entry.currency.is_local, 'currency_name': entry.currency.name, 'debit': entry.debit,
            'credit': entry.credit, 'amount_foreign': entry.amount_foreign, 'is_verified': entry.is_verified
        })
    response = Response(data)
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_customer_bill_lines(request):
    bill_id = request.GET.get('billId')
    lines = BillLine.objects.filter(customer_bill_lines__id=bill_id).all()
    return Response(
        lines.values('id', 'label', 'account__account_number', 'account__account_number', 'account_id', 'quantity',
                     'price', 'tax'))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_bill(request):
    try:
        data = request.data
        user = request.user
        bill_date = data['dateBill']
        bill_deadline = data['dateDeadline']
        partner = Partner.objects.get(id=data['partner']) if data['partner'] != '' else None
        reference = data['reference']
        account = data['account']
        currency = Currency.objects.get(id=data['currency'])
        rate = data['rate'] if data['rate'] != '' else 1

        bill = CustomerBill(bill_at=bill_date, deadline_at=bill_deadline, partner=partner, reference=reference,
                            account_id=account, currency=currency, rate=rate)

        bill.save()

        context = {'message': "Facture créée avec succès!"}

        return Response(context, status=status.HTTP_201_CREATED)
    except BaseException as error:

        return Response({'message': _("Quelque chose s'est mal passé avec la création de la facture")},
                        status=status.HTTP_400_BAD_REQUEST)
