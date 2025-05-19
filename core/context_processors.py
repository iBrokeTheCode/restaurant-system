from core.models import BusinessInfo


def business_info(request):
    try:
        info = BusinessInfo.objects.all().first()
    except BusinessInfo.DoesNotExist:
        info = None

    return {'business_info': info}
