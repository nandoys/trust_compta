from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from treasury.models import AccountingEntry
from .models import Partner, CustomerBill


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
    context = []
    bills = CustomerBill.objects.filter(is_lettered=False).all()

    for bill in bills:
        payments = bill.customerbillpayment_set.all()
        context.append({
            'bill': {'id': bill.id, 'account': {'id': bill.account.serializable_value('id'),
                                                'account_number': bill.account.serializable_value('account_number'),
                                                'account_name': bill.account.serializable_value('account_name')},
                     'partner': bill.partner, 'label': bill.label, 'reference': bill.reference,
                     # 'currency': {'id':  bill.currency, 'symbol': bill.currency, 'name': bill},
                     'bill_at': bill.bill_at, 'amountForeignCurrency': bill.amount_foreign_currency,
                     'amount': bill.amount}
        })

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_customer_bill_accounting_entries(request, bill_id):
    context = []
    entries = None
    try:
        entries = AccountingEntry.objects.filter(ref_billing_customer_id=bill_id).all()
    except AccountingEntry.DoesNotExist:
        pass

    return Response(entries.values())
