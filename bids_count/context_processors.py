from bids_count.models import DjangoAdminLog


def bids_count(request):
    return {'bids_count': DjangoAdminLog.created_in_current_month().count()}
