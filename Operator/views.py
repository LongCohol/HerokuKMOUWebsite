import xlwt
from PIL import Image
from django.conf import settings
from django.contrib import messages

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django_user_agents.utils import get_user_agent

from django.core import serializers
from django.core.serializers import json
import json

from Shipment.views import shipmentRegisterView, shipmentFilterView, warehouseFilterView, shipmentModifyView
from User.models import Account
from Shipment.models import ShipmentFilter, Shipment
# from Operator.models import Operator
# from Supplier.models import Supplier
# from Company.models import Company
from account_forms import OperatorForm, SupplierForm, CompanyForm, OperatorLogin, CustomerLogin
from shipment_forms import ShipmentRegistration, ShipmentModification, WarehouseFilter

from datetime import datetime


CONTEXT = {}

UNIT_LIST = ['Select', 'CT', 'PL', 'WC', 'PKG']
WAREHOUSE_LIST = ['Select', 'SL', 'KIM-IGS', 'ICN-IGS']
BY_LIST = ['Select', 'DHL', 'FDX', 'TNT', 'AIR', 'SEA', 'SFX']

RESULT_PER_PAGE = 100
VESSEL_KEY = {}
# accounts = Account.objects.all()
# shipments = Shipment.objects.all()
COMP_LIST = []
VESS_LIST = []
# for account in accounts:
#     if account.vesselList is not "":
#         vesselowned = []
#         companyOwner = account.companyName
#         COMP_LIST.append(companyOwner)
#         vesselOwned = account.vesselList.split(',')
#         for vessel in vesselOwned:
#             vesselowned.append(vessel)
#             VESS_LIST.append(vessel)
#             VESSEL_KEY[vessel] = companyOwner
#             CONTEXT[vessel] = companyOwner

# CONTEXT["allCompanies"] = COMP_LIST
# CONTEXT["allVessels"] = VESS_LIST
# CONTEXT["allBys"] = BY_LIST
# CONTEXT["allUnits"] = UNIT_LIST
# CONTEXT["allWarehouses"] = WAREHOUSE_LIST
# CONTEXT["totalShipments"] = len(shipments)
VESSEL_KEY_JS = json.dumps(CONTEXT)
# CONTEXT["vessel_key"] = VESSEL_KEY_JS


def adminView(request):
    oprForm = OperatorForm()
    splForm = SupplierForm()
    cpnForm = CompanyForm()

    # IF this is POST request:
    if request.method == "POST":
        oprID = request.POST.get('oprID')
        splID = request.POST.get('splID')
        cpnID = request.POST.get('cpnID')
        oprNumber = len(Account.objects.filter(userID__exact=oprID))
        splNumber = len(Account.objects.filter(userID__exact=splID))
        cpnNumber = len(Account.objects.filter(userID__exact=cpnID))

        # oprID = request.POST.get('operatorID')
        # splID = request.POST.get('supplierID')
        # cpnID = request.POST.get('companyID')

        if 'saveOperator' in request.POST:
            oprForm = OperatorForm(request.POST)

            if oprForm.is_valid() and oprNumber<1:
                oprForm.save()
            else:
                opr = Account.objects.get(userID__exact=oprID)
                # opr.userID = oprID
                opr.password = request.POST['oprPassword']
                opr.permission = request.POST['oprPermission']
                opr.isOpr = True
                opr.rawPassword = opr.password
                opr.password = make_password(opr.password)
                opr.save()
                # opr = Operator.objects.get(operatorID__exact=oprID)
                # opr.OPRpassword = request.POST['OPRpassword']
                # opr.permission = request.POST['permission']
                # opr.save()
            oprForm = OperatorForm()

        if 'saveSupplier' in request.POST:
            splForm = SupplierForm(request.POST)

            if splForm.is_valid() and splNumber<1:
                splForm.save()
            else:
                spl = Account.objects.get(userID__exact=splID)
                # spl.userID = splID
                spl.password = request.POST['splPassword']
                spl.companyName = request.POST['splName']
                spl.isSpl = True
                spl.rawPassword = spl.password
                spl.password = make_password(spl.password)
                spl.save()
                # spl = Supplier.objects.get(supplierID__exact=splID)
                # spl.supplierName = request.POST['supplierName']
                # spl.SPLpassword = request.POST['SPLpassword']
                # spl.save()
            splForm = SupplierForm()

        if 'saveCompany' in request.POST:
            cpnForm = CompanyForm(request.POST)

            if cpnForm.is_valid() and cpnNumber<1:
                cpnForm.save()
            else:
                cpn = Account.objects.get(userID__exact=cpnID)
                # cpn.userID = cpnID
                cpn.password = request.POST['cpnPassword']
                cpn.email = request.POST['cpnEmail']
                cpn.companyName = request.POST['cpnName']
                cpn.vesselList = request.POST['cpnVesselList']
                cpn.isCpn = True
                cpn.rawPassword = cpn.password
                cpn.password = make_password(cpn.password)
                cpn.save()
                # cpn = Company.objects.get(companyID__exact=cpnID)
                # cpn.companyName = request.POST['companyName']
                # cpn.companyEmail = request.POST['companyEmail']
                # cpn.CPNpassword = request.POST['CPNpassword']
                # cpn.vesselList = request.POST['vesselList']
                # cpn.save()
            cpnForm = CompanyForm()

        if 'deleteOperator' in request.POST:
            Account.objects.filter(userID__exact=oprID).delete()
        if 'deleteSupplier' in request.POST:
            Account.objects.filter(userID__exact=splID).delete()
        if 'deleteCompany' in request.POST:
            Account.objects.filter(userID__exact=cpnID).delete()

        # if 'deleteOperator' in request.POST:
        #     Operator.objects.filter(operatorID__exact=oprID).delete()
        # if 'deleteSupplier' in request.POST:
        #     Supplier.objects.filter(supplierID__exact=splID).delete()
        # if 'deleteCompany' in request.POST:
        #     Company.objects.filter(companyID__exact=cpnID).delete()
    # ELSE when this is GET request:
    else:
        oprForm = OperatorForm()
        splForm = SupplierForm()
        cpnForm = CompanyForm()

    operators = Account.objects.filter(isOpr=True)
    suppliers = Account.objects.filter(isSpl=True)
    companies = Account.objects.filter(isCpn=True)
    oprs = serializers.serialize("json", operators)
    spls = serializers.serialize("json", suppliers)
    cpns = serializers.serialize("json", companies)
    CONTEXT['operatorList'] = oprs
    CONTEXT['supplierList'] = spls
    CONTEXT['companyList'] = cpns

    # oprList = serializers.serialize("json", Operator.objects.all())
    # splList = serializers.serialize("json", Supplier.objects.all())
    # cpnList = serializers.serialize("json", Company.objects.all())
    # CONTEXT['operatorList'] = oprList
    # CONTEXT['supplierList'] = splList
    # CONTEXT['companyList'] = cpnList

    CONTEXT['operatorForm'] = oprForm
    CONTEXT['supplierForm'] = splForm
    CONTEXT['companyForm'] = cpnForm

    return render(request, "adminPage.html", CONTEXT)


def logged_out(request):
    logout(request)

    return redirect('frontpage')


def staff_in(request):
    CONTEXT["staffExist"] = request.user
    return render(request, "redirect1.html", CONTEXT)


def customer_in(request):
    CONTEXT["customerExist"] = request.user
    return render(request, "redirect2.html", CONTEXT)


def frontView(request):
    # staffloginview_result = staffLoginView(request)
    # customerloginview_result = customerLoginView(request)
    # CONTEXT.update(staffloginview_result)
    # CONTEXT.update(customerloginview_result)

    if request.method == "POST":
        # check the button of staffLogin.html
        if "staffloginform" in request.POST:
            formOperatorLogin = OperatorLogin(request.POST)
            if formOperatorLogin.is_valid():
                username = formOperatorLogin.cleaned_data.get('userIDstaff')
                password = formOperatorLogin.cleaned_data.get('passwordstaff')
                accountstaff = authenticate(request, userID=username, password=password)
            # if there exists an account with the authentication
                if accountstaff is not None:
                    login(request, accountstaff)
                    return redirect('staff_redirect')

        if "customerloginform" in request.POST:
            formCustomerLogin = CustomerLogin(request.POST)
            if formCustomerLogin.is_valid():
                username = formCustomerLogin.cleaned_data.get('userIDcustomer')
                password = formCustomerLogin.cleaned_data.get('passwordcustomer')
                accountcustomer = authenticate(request, userID=username, password=password)
            # if there exists an account with the authentication
                if accountcustomer is not None:
                    login(request, accountcustomer)
                    return redirect('customer_redirect')

    else:
        # CONTEXT["staffExist"] = request.user
        # CONTEXT["customerExist"] = request.user
        CONTEXT["staffLogin"] = OperatorLogin()
        CONTEXT["customerLogin"] = CustomerLogin()
    return render(request, "frontpage.html", CONTEXT)


# def staffLoginView(request):
#     # IF this is POST request:
#     if request.method == "POST":
#         account = None
#         formOperatorLogin = OperatorLogin(request.POST)
#
#         if formOperatorLogin.is_valid():
#             username = formOperatorLogin.cleaned_data.get('userIDstaff')
#             password = formOperatorLogin.cleaned_data.get('passwordstaff')
#             account = authenticate(request, userID=username, password=password)
#     # ELSE when this is GET request:
#     else:
#         account = request.user
#         formOperatorLogin = OperatorLogin()
#
#     result = {
#         "staffLogin": formOperatorLogin,
#         "staffExist": account,
#     }
#     return result
#
#
# def customerLoginView(request):
#     # IF this is POST request:
#     if request.method == "POST":
#         accountcustomer = None
#         formCustomerLogin = CustomerLogin(request.POST)
#
#         if formCustomerLogin.is_valid():
#             username = formCustomerLogin.cleaned_data.get('userIDcustomer')
#             password = formCustomerLogin.cleaned_data.get('passwordcustomer')
#             accountcustomer = authenticate(request, userID=username, password=password)
#     # ELSE when this is GET request:
#     else:
#         accountcustomer = request.user
#         formCustomerLogin = CustomerLogin()
#
#     result = {
#         "customerLogin": formCustomerLogin,
#         "customerExist": accountcustomer,
#     }
#     return result


def shipment_print(request):
    context = {}
    id_tobeprinted = []
    vessel_tobeprinted = ""
    shipment_tobeprinted = []
    total_quanty = 0
    total_weight = 0

    if request.method == "POST" and "htmlShipment" in request.POST:
        shipmentselectedlist = request.POST.get('checkedList')
        shipmentprintedlist = shipmentselectedlist.split(',')
        for sh in shipmentprintedlist:
            if sh is not "":
                sh = int(sh)
                shipment = Shipment.objects.get(number__exact=sh)
                id_tobeprinted.append(sh)
                shipment_tobeprinted.append(shipment)
                if shipment.vessel not in vessel_tobeprinted:
                    vessel_tobeprinted += "/ " + shipment.vessel
                if shipment.quanty is not "":
                    total_quanty += int(shipment.quanty)
                if shipment.weight is not "":
                    total_weight += int(shipment.weight)

    vessel_tobeprinted = vessel_tobeprinted[1:]
    context['totalQuanty'] = total_quanty
    context['totalWeight'] = total_weight
    context['vesselPrinted'] = vessel_tobeprinted
    context['shipmentPrinted'] = shipment_tobeprinted
    return context


def mainView1(request):
    useragent = get_user_agent(request)

    shipmentmodifyview_result = shipmentModifyView(request)
    CONTEXT.update(shipmentmodifyview_result)
    shipmentregisterview_result = shipmentRegisterView(request)
    CONTEXT.update(shipmentregisterview_result)

    shipmentfilterview_result = shipmentFilterView(request)
    warehousefilterview_result = warehouseFilterView(request)
    CONTEXT.update(shipmentfilterview_result)
    CONTEXT.update(warehousefilterview_result)
    # shipmentresults = CONTEXT["shipmentDisplay"]
    shipmentresults = CONTEXT["shipmentResults"]
    CONTEXT["totalResults"] = len(shipmentresults)

    warehousefiltered = request.GET.get('wh')

    if request.method == "POST":
        shipmentselectedlist = request.POST.get('checkedList')
        shipmentadjustedlist = request.POST.get('changedList')

        colorpicked = request.POST.get('pickedColor')

        # check the button on mainPage1.html
        if "addShipment" in request.POST:
            # load the form from the CONTEXT
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                shipment = shipmentregisterform.save()
                if shipment.warehouse is not "":
                    shipment.wh_timestamp = datetime.now()
                if shipment.warehouse2 is not "":
                    shipment.wh_timestamp2 = datetime.now()
                shipment.insert_org = request.user.userID
                shipment.save()
                messages.success(request, 'New shipment with id ' + str(shipment.number) + ' has been added successfully')
                CONTEXT["shipmentRegister"] = ShipmentRegistration()
                return redirect('mainPage1')

        if "changeShipment" in request.POST:
            # load the form from the CONTEXT
            shipmentadjustedlist = int(shipmentadjustedlist)
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                modified_company = shipmentregisterform.cleaned_data.get('company')
                modified_vessel = shipmentregisterform.cleaned_data.get('vessel')
                modified_docs = shipmentregisterform.cleaned_data.get('docs')
                modified_odr = shipmentregisterform.cleaned_data.get('odr')
                modified_supplier = shipmentregisterform.cleaned_data.get('supplier')
                modified_quanty = shipmentregisterform.cleaned_data.get('quanty')
                modified_unit = shipmentregisterform.cleaned_data.get('unit')
                modified_size = shipmentregisterform.cleaned_data.get('size')
                modified_weight = shipmentregisterform.cleaned_data.get('weight')
                modified_in_date = shipmentregisterform.cleaned_data.get('in_date')
                modified_warehouse = shipmentregisterform.cleaned_data.get('warehouse')
                modified_warehouse2 = shipmentregisterform.cleaned_data.get('warehouse2')
                modified_by = shipmentregisterform.cleaned_data.get('by')
                modified_BLno = shipmentregisterform.cleaned_data.get('BLno')
                modified_port = shipmentregisterform.cleaned_data.get('port')
                modified_out_date = shipmentregisterform.cleaned_data.get('out_date')
                modified_remark = shipmentregisterform.cleaned_data.get('remark')
                modified_division = shipmentregisterform.cleaned_data.get('division')
                modified_job_number = shipmentregisterform.cleaned_data.get('job_number')

                # check the shipment to update
                shipment = Shipment.objects.get(number__exact=shipmentadjustedlist)
                shipment.company = modified_company
                shipment.vessel = modified_vessel
                shipment.docs = modified_docs
                shipment.odr = modified_odr
                shipment.supplier = modified_supplier
                shipment.quanty = modified_quanty
                shipment.unit = modified_unit
                shipment.size = modified_size
                shipment.weight = modified_weight
                shipment.in_date = modified_in_date
                shipment.warehouse = modified_warehouse
                shipment.warehouse2 = modified_warehouse2
                shipment.by = modified_by
                shipment.BLno = modified_BLno
                shipment.port = modified_port
                shipment.out_date = modified_out_date
                shipment.remark = modified_remark
                shipment.division = modified_division
                shipment.job_number = modified_job_number

                shipment.correct_org = request.user.userID
                shipment.save()

        if "addShipment_m" in request.POST:
            # load the form from the CONTEXT
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                shipment_m = shipmentregisterform.save()
                shipment_m.insert_org = request.user.userID
                shipment_m.save()
                messages.success(request, 'New shipment with id ' + str(shipment_m.number) + ' has been added successfully')

                CONTEXT["shipmentRegister"] = ShipmentRegistration()
                return redirect('mainPage1')

        if "modifyShipment" in request.POST:
            shipmentchangedlist = shipmentselectedlist.split(',')
            shipmentmodifyform = CONTEXT["shipmentModify"]
            if shipmentmodifyform.is_valid():
                changed_company = shipmentmodifyform.cleaned_data.get('companyM')
                changed_vessel = shipmentmodifyform.cleaned_data.get('vesselM')
                changed_supplier = shipmentmodifyform.cleaned_data.get('supplierM')
                changed_warehouse = shipmentmodifyform.cleaned_data.get('warehouseM')
                changed_warehouse2 = shipmentmodifyform.cleaned_data.get('warehouse2M')
                changed_division = shipmentmodifyform.cleaned_data.get('divisionM')
                changed_flag_status = shipmentmodifyform.cleaned_data.get('flag_statusM')
                changed_in_date = shipmentmodifyform.cleaned_data.get('in_dateM')
                changed_out_date = shipmentmodifyform.cleaned_data.get('out_dateM')
                changed_job_number = shipmentmodifyform.cleaned_data.get('job_numberM')
                changed_port = shipmentmodifyform.cleaned_data.get('portM')
                changed_remark = shipmentmodifyform.cleaned_data.get('remarkM')
                changed_memo = shipmentmodifyform.cleaned_data.get('memoM')
                changed_docs = shipmentmodifyform.cleaned_data.get('docsM')
                changed_odr = shipmentmodifyform.cleaned_data.get('odrM')
                changed_quanty = shipmentmodifyform.cleaned_data.get('quantyM')
                changed_unit = shipmentmodifyform.cleaned_data.get('unitM')
                changed_size = shipmentmodifyform.cleaned_data.get('sizeM')
                changed_weight = shipmentmodifyform.cleaned_data.get('weightM')
                changed_BLno = shipmentmodifyform.cleaned_data.get('BLnoM')
                changed_colorpick = colorpicked

                for id_shipmentchanged in shipmentchangedlist:
                    if id_shipmentchanged == "":
                        pass
                    else:
                        id_shipmentchanged = int(id_shipmentchanged)
                        shipmentchanged = Shipment.objects.get(number=id_shipmentchanged)
                        if changed_company is not "":
                            shipmentchanged.company = changed_company
                        if changed_vessel is not "":
                            shipmentchanged.vessel = changed_vessel
                        if changed_supplier is not "":
                            shipmentchanged.supplier = changed_supplier
                        if changed_warehouse is not "":
                            shipmentchanged.warehouse = changed_warehouse
                        if changed_warehouse2 is not "":
                            shipmentchanged.warehouse2 = changed_warehouse2
                        if changed_division is not "":
                            shipmentchanged.division = changed_division
                        if changed_flag_status is not "":
                            shipmentchanged.flag_status = changed_flag_status
                        if changed_in_date is not "":
                            shipmentchanged.in_date = changed_in_date
                            # change_in_date = changed_in_date[:4] + "-" + changed_in_date[4:6] + "-" + changed_in_date[6:8]
                            # shipmentchanged.in_date = change_in_date
                        if changed_out_date is not "":
                            shipmentchanged.out_date = changed_out_date
                            # change_out_date = changed_out_date[:4] + "-" + changed_out_date[4:6] + "-" + changed_out_date[6:8]
                            # shipmentchanged.out_date = change_out_date
                        if changed_job_number is not "":
                            shipmentchanged.job_number = changed_job_number
                        if changed_port is not "":
                            shipmentchanged.port = changed_port
                        if changed_remark is not "":
                            shipmentchanged.remark = changed_remark
                        if changed_memo is not "":
                            shipmentchanged.remark = changed_memo
                        if changed_docs is not "":
                            shipmentchanged.docs = changed_docs
                        if changed_odr is not "":
                            shipmentchanged.odr = changed_odr
                        if changed_quanty is not "":
                            shipmentchanged.quanty = changed_quanty
                        if changed_unit is not "":
                            shipmentchanged.unit = changed_unit
                        if changed_size is not "":
                            shipmentchanged.size = changed_size
                        if changed_weight is not "":
                            shipmentchanged.weight = changed_weight
                        if changed_BLno is not "":
                            shipmentchanged.BLno = changed_BLno
                        shipmentchanged.colorpick = changed_colorpick

                        shipmentchanged.correct_org = request.user.userID
                        shipmentchanged.save()
                CONTEXT["shipmentModify"] = ShipmentModification()

        if "deleteShipment" in request.POST:
            shipmentchangedlist = shipmentselectedlist.split(',')

            for id_shipmentdeleted in shipmentchangedlist:
                if id_shipmentdeleted == "":
                    pass
                else:
                    id_shipmentdeleted = int(id_shipmentdeleted)
                    Shipment.objects.filter(number__exact=id_shipmentdeleted).delete()

        if "printShipment" in request.POST:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="shipment_list.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Shipments')
            # Sheet header, first row
            row_num = 0
            title_style = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
            row_style = xlwt.easyxf('align: wrap on, vert centre, horiz center')

            columns = ['Company', 'Vessel', 'Doc', 'Odr', 'Supplier', 'Qty', 'Unit', 'Size', 'Weight', 'In-date', 'Out-date', 'Warehouse',
                       'By', 'BLno', 'Port', 'Remark', 'Job.No', 'Division', 'Status', 'Image', 'User-created', 'User-modified']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], title_style)
            # Sheet body, remaining rows
            ws.col(0).width = 256 * 12
            ws.col(1).width = 256 * 20
            ws.col(2).width = 256 * 20
            ws.col(3).width = 256 * 8
            ws.col(4).width = 256 * 8
            ws.col(5).width = 256 * 5
            ws.col(6).width = 256 * 5
            ws.col(7).width = 256 * 8
            ws.col(8).width = 256 * 8
            ws.col(9).width = 256 * 10
            ws.col(10).width = 256 * 10
            ws.col(11).width = 256 * 12
            ws.col(12).width = 256 * 5
            ws.col(13).width = 256 * 8
            ws.col(14).width = 256 * 8
            ws.col(15).width = 256 * 10
            ws.col(16).width = 256 * 10
            ws.col(17).width = 256 * 8
            ws.col(18).width = 256 * 8
            ws.col(19).width = 256 * 20
            ws.col(20).width = 256 * 10
            ws.col(21).width = 256 * 10

            shipmentprintedlist = shipmentselectedlist.split(',')
            for id_shipmentprinted in shipmentprintedlist:
                if id_shipmentprinted == "":
                    pass
                else:
                    id_shipmentprinted = int(id_shipmentprinted)
                    shipmentprinted = Shipment.objects.get(number=id_shipmentprinted)

                    row_num += 1
                    # for col_num in range(22):
                    ws.write(row_num, 0, shipmentprinted.company, row_style)
                    ws.write(row_num, 1, shipmentprinted.vessel, row_style)
                    ws.write(row_num, 2, shipmentprinted.docs, row_style)
                    ws.write(row_num, 3, shipmentprinted.odr, row_style)
                    ws.write(row_num, 4, shipmentprinted.supplier, row_style)
                    ws.write(row_num, 5, shipmentprinted.quanty, row_style)
                    ws.write(row_num, 6, shipmentprinted.unit, row_style)
                    ws.write(row_num, 7, shipmentprinted.size, row_style)
                    ws.write(row_num, 8, shipmentprinted.weight, row_style)
                    ws.write(row_num, 9, shipmentprinted.in_date, row_style)
                    ws.write(row_num, 10, shipmentprinted.out_date, row_style)
                    ws.write(row_num, 11, shipmentprinted.warehouse, row_style)
                    ws.write(row_num, 12, shipmentprinted.by, row_style)
                    ws.write(row_num, 13, shipmentprinted.BLno, row_style)
                    ws.write(row_num, 14, shipmentprinted.port, row_style)
                    ws.write(row_num, 15, shipmentprinted.remark, row_style)
                    ws.write(row_num, 16, shipmentprinted.job_number, row_style)
                    ws.write(row_num, 17, shipmentprinted.division, row_style)
                    ws.write(row_num, 18, shipmentprinted.flag_status, row_style)
                    if (shipmentprinted.image):
                        tall_style = xlwt.easyxf('font:height 1000;')
                        ws.row(row_num).set_style(tall_style)

                        img = Image.open(str(settings.BASE_DIR) + shipmentprinted.image.url)
                        scale = (140, 90)
                        img.thumbnail(scale)
                        r, g, b, a = img.split()
                        img = Image.merge("RGB", (r, g, b))
                        img.save('sm.bmp')
                        ws.insert_bitmap('sm.bmp', row_num, 19)
                    ws.write(row_num, 20, shipmentprinted.insert_org, row_style)
                    ws.write(row_num, 21, shipmentprinted.correct_org, row_style)

            wb.save(response)
            return response

        if "resetFilter" in request.POST:
            CONTEXT["shipmentFilter"] = ShipmentFilter()
            return redirect("mainPage1")

        if "htmlShipment" in request.POST:
            shipmentHTML = shipment_print(request)
            CONTEXT.update(shipmentHTML)
            return render(request, "shipmentPrint.html", CONTEXT)

    else:
        # CONTEXT["shipmentRegister"] = ShipmentRegistration()
        # CONTEXT["shipmentModify"] = ShipmentModification()
        if not request.user.is_authenticated:
            logout(request)
            return redirect("frontpage")

    if useragent.is_mobile:
        return render(request, "mainPage1-mobile.html", CONTEXT)
    else:
        return render(request, "mainPage1.html", CONTEXT)


def mainView2(request):
    useragent = get_user_agent(request)
    context = {}

    if not request.user.is_authenticated:
        logout(request)
        return render(request, "frontpage.html", CONTEXT)
    # elif CONTEXT.get('customerExist') == None:
    #     return render(request, "frontpage.html", CONTEXT)
    else:
        shipmentfilterview_result = shipmentFilterView(request)
        context["allVessels"] = VESS_LIST
        context["vessel_key"] = VESSEL_KEY_JS
        context.update(shipmentfilterview_result)

    if useragent.is_mobile:
        return render(request, "mainPage2-mobile.html", context)
    else:
        return render(request, "mainPage2.html", context)

