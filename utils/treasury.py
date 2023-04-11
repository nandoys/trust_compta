from accounting.models import Additional
from treasury.models import Income, Outcome


def outcomes_with_subaccount(subaccount: Additional, month: int, year: int, currency: str):
    return Outcome.objects.filter(accounting_additional=subaccount, out_at__month=month, out_at__year=year,
                                  currency__symbol_iso__icontains=currency)
