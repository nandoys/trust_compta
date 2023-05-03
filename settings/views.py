from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from settings.models import Journal
from settings.serializers import JournalSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_journal(request):
    journal_type = request.GET.get('type')
    journals = Journal.objects.filter(type_journal__label__iexact=journal_type)

    journal_root = None
    for journal in journals:
        if journal.is_root():
            journal_root = JournalSerializer(journal)

    return Response(journal_root.data)
