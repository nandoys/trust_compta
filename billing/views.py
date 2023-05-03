import datetime

from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from accounting.models import Plan
from settings.models import Journal
from treasury.models import AccountingEntry, Currency
from treasury.serializers import AccountingEntrySerializer
from utils.token import set_auth_token
from .models import Partner, CustomerBill, BillLine, BillLineTax
from .serializers import BillLineSerializer, CustomerBillSerializer


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

        serializer = CustomerBillSerializer(bills, many=True)

        return Response(serializer.data)
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

    serializer = AccountingEntrySerializer(entries, many=True)

    response = Response(serializer.data)
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_customer_bill_lines(request):
    bill_id = request.GET.get('billId')
    lines = BillLine.objects.filter(customer_bill__id=bill_id).all()
    lineSerialize = BillLineSerializer(lines, many=True)
    return Response(lineSerialize.data)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_bill(request):
    try:
        data = request.data
        user = request.user
        bill = CustomerBill.objects.get(id=1)
        bill.bill_date = data['dateBill']
        bill.deadline = data['dateDeadline']
        bill.partner = Partner.objects.get(id=data['partner']) if data['partner'] != '' else None
        bill.reference = data['reference']
        bill.account = data['account']
        bill.currency = Currency.objects.get(id=data['currency'])
        bill.rate = data['rate'] if data['rate'] != '' else 1
        bill.amount = data['amount']

        print(bill.amount)

        # bill.save()

        context = {'message': "Facture créée avec succès!"}

        return Response(context, status=status.HTTP_201_CREATED)
    except BaseException as error:

        return Response({'message': _("Quelque chose s'est mal passé avec la création de la facture")},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_customer_bill_entry(request):
    user = request.user
    entries = request.data
    for entry in entries:
        ref_billing_customer = CustomerBill.objects.get(id=entry['ref_billing_customer'])
        account = Plan.objects.get(id=entry['account'])
        partner = None
        rate = entry['rate']
        currency = Currency.objects.get(id=entry['currency'])
        ref_bill_line = entry['ref_bill_line']
        date_at = datetime.datetime.strptime(entry['date_at'], "%d/%m/%Y").date()
        label = entry['label']
        amount_foreign = entry['amount_foreign']
        debit = entry['debit']
        credit = entry['credit']

        if entry['is_customer_account']:
            ref_billing_customer.amount = entry['debit']
            ref_billing_customer.amount_foreign = entry['amount_foreign']
            ref_billing_customer.save()

        if entry['partner'] is not None:
            partner = Partner.objects.get(id=entry['partner'])

        if ref_bill_line is not None:
            label_line = ref_bill_line['label']
            account_line = ref_bill_line['account']

            bill_line = BillLine(customer_bill=ref_billing_customer, label=label_line, account_id=account_line,
                                 quantity=ref_bill_line['quantity'], price=ref_bill_line['price'],
                                 price_with_tax=ref_bill_line['priceWithTax'])

            bill_line.save()

            # save every taxes in billLiineTax
            if len(ref_bill_line['taxes']) > 0:
                taxes = ref_bill_line['taxes']

                for tax in taxes:
                    tax_id = tax['tax_ref']
                    tax_amount = tax['calculated']

                    BillLineTax(tax_id=tax_id, tax_amount=tax_amount, bill_line=bill_line).save()

            AccountingEntry(account=account, currency=currency, rate=rate, ref_billing_customer=ref_billing_customer,
                            ref_bill_line=bill_line, label=label_line, partner=partner, date_at=date_at,
                            amount_foreign=amount_foreign, debit=debit, credit=credit, done_by=user).save()
        else:
            AccountingEntry(account=account, currency=currency, rate=rate, ref_billing_customer=ref_billing_customer,
                            label=label, partner=partner, date_at=date_at, amount_foreign=amount_foreign, debit=debit,
                            credit=credit,
                            done_by=user).save()

    response = Response({'message': _("Écriture comptable enregistrée avec succès")})
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_delete_customer_bill_entry(request):
    line_id = request.data['id']
    BillLine.objects.get(id=line_id).delete()
    response = Response({'message': _("Écriture comptable supprimée avec succès")})
    return response
