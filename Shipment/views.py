from django.core.paginator import Paginator

from Shipment.models import Shipment, ShipmentFilter
from shipment_forms import ShipmentRegistration, ShipmentModification, WarehouseFilter


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
    warehouseFilter = request.GET.get('wh')

    paginator = Paginator(formShipmentFilter.qs, RESULT_PER_PAGE)
    page = request.GET.get('page')
    pagination = paginator.get_page(page)
    result = {
        "shipmentFilter": formShipmentFilter,
        "shipmentDisplay": pagination,
        "shipmentResults": formShipmentFilter.qs,
    }
    return result


def warehouseFilterView(request):
    # IF this is POST request:
    if request.method == "POST":
        warehouseFilter = WarehouseFilter(request.POST)
    # ELSE when this is GET request:
    else:
        warehouseFilter = WarehouseFilter(request.GET)

    result = {
        "warehouseFilter": warehouseFilter,
    }
    return result


def shipmentModifyView(request):
    # IF this is POST request:
    if request.method == "POST":
        formShipmentModify = ShipmentModification(request.POST)
    # ELSE when this is GET request:
    else:
        formShipmentModify = ShipmentModification()

    result = {
        "shipmentModify": formShipmentModify,
    }
    return result
