from django.core import serializers
from django.core.paginator import Paginator

from Shipment.models import Shipment, ShipmentFilter
from shipment_forms import ShipmentRegistration


RESULT_PER_PAGE = 100


def shipmentRegisterView(request):
    # IF this is POST request:
    if request.method == "POST":
        formShipmentRegister = ShipmentRegistration(request.POST, request.FILES)
    # ELSE when this is GET request:
    else:
        formShipmentRegister = ShipmentRegistration()

    result = {
        "shipmentRegister": formShipmentRegister,
    }
    return result


def shipmentFilterView(request):
    shipmentList = Shipment.objects.all().order_by("-number")
    formShipmentFilter = ShipmentFilter(request.GET, queryset=shipmentList)
    paginator = Paginator(formShipmentFilter.qs, RESULT_PER_PAGE)
    page = request.GET.get('page')
    pagination = paginator.get_page(page)
    result = {
        "shipmentFilter": formShipmentFilter,
        "shipmentDisplay": pagination,
    }
    return result