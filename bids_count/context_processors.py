from bids_count.models import DjangoAdminLog


def bids_count(request):
    return {'bids_count': DjangoAdminLog.objects.count()}
