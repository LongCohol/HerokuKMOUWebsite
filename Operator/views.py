from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django_user_agents.utils import get_user_agent

from django.core import serializers
from django.core.serializers import json
import json

from Shipment.views import shipmentRegisterView, shipmentFilterView, shipmentModifyView
from User.models import Account
from Shipment.models import ShipmentFilter, Shipment
# from Operator.models import Operator
# from Supplier.models import Supplier
# from Company.models import Company
from account_forms import OperatorForm, SupplierForm, CompanyForm, OperatorLogin, CustomerLogin
from shipment_forms import ShipmentRegistration, ShipmentModification

CONTEXT = {}
RESULT_PER_PAGE = 100
VESSEL_KEY = {}
accounts = Account.objects.all()
COMP_LIST = []
VESS_LIST = []
for account in accounts:
    if account.vesselList is not "":
        vesselowned = []
        companyOwner = account.companyName
        COMP_LIST.append(companyOwner)
        vesselOwned = account.vesselList.split(',')
        for vessel in vesselOwned:
            vesselowned.append(vessel)
            VESS_LIST.append(vessel)
            VESSEL_KEY[vessel] = companyOwner
            CONTEXT[vessel] = companyOwner

CONTEXT["allCompanies"] = COMP_LIST
CONTEXT["allVessels"] = VESS_LIST


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
    return render(request, "redirect1.html", CONTEXT)
def customer_in(request):
    return render(request, "redirect2.html", CONTEXT)


def frontView(request):
    staffloginview_result = staffLoginView(request)
    customerloginview_result = customerLoginView(request)
    CONTEXT.update(staffloginview_result)
    CONTEXT.update(customerloginview_result)

    if request.method == "POST":
        # check the button of staffLogin.html
        if "staffloginform" in request.POST:
            # if there exists an account with the authentication
            accountstaff = CONTEXT["staffExist"]
            if accountstaff is not None:
                # CONTEXT.pop("customerExist")
                login(request, accountstaff)
                return redirect('staff_redirect')

        if "customerloginform" in request.POST:
            # if there exists an account with the authentication
            accountcustomer = CONTEXT["customerExist"]
            if accountcustomer is not None:
                # CONTEXT.pop("staffExist")
                login(request, accountcustomer)
                return redirect('customer_redirect')

    return render(request, "frontpage.html", CONTEXT)


def staffLoginView(request):
    # IF this is POST request:
    if request.method == "POST":
        account = None
        formOperatorLogin = OperatorLogin(request.POST)

        if formOperatorLogin.is_valid():
            username = formOperatorLogin.cleaned_data.get('userIDstaff')
            password = formOperatorLogin.cleaned_data.get('passwordstaff')
            account = authenticate(request, userID=username, password=password)
    # ELSE when this is GET request:
    else:
        account = None
        formOperatorLogin = OperatorLogin()

    result = {
        "staffLogin": formOperatorLogin,
        "staffExist": account,
    }
    return result


def customerLoginView(request):
    # IF this is POST request:
    if request.method == "POST":
        accountcustomer = None
        formCustomerLogin = CustomerLogin(request.POST)

        if formCustomerLogin.is_valid():
            username = formCustomerLogin.cleaned_data.get('userIDcustomer')
            password = formCustomerLogin.cleaned_data.get('passwordcustomer')
            accountcustomer = authenticate(request, userID=username, password=password)
    # ELSE when this is GET request:
    else:
        accountcustomer = None
        formCustomerLogin = CustomerLogin()

    result = {
        "customerLogin": formCustomerLogin,
        "customerExist": accountcustomer,
    }
    return result


def mainView1(request):
    useragent = get_user_agent(request)

    shipmentregisterview_result = shipmentRegisterView(request)
    shipmentmodifyview_result = shipmentModifyView(request)
    CONTEXT.update(shipmentregisterview_result)
    CONTEXT.update(shipmentmodifyview_result)

    if request.method == "POST":
        shipmentselectedlist = request.POST.get('checkedList')
        # check the button on mainPage1.html
        if "addShipment" in request.POST:
            # load the form from the CONTEXT
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                shipment = shipmentregisterform.save()
                shipment.insert_org = CONTEXT["staffExist"].userID
                shipment.save()
                CONTEXT["shipmentRegister"] = ShipmentRegistration()
                return redirect('mainPage1')

        if "changeShipment" in request.POST:
            modified_company = request.POST['company']
            modified_vessel = request.POST['vessel']
            modified_docs = request.POST['docs']
            modified_odr = request.POST['odr']
            modified_supplier = request.POST['supplier']
            modified_quanty = request.POST['quanty']
            modified_unit = request.POST['unit']
            modified_size = request.POST['size']
            modified_weight = request.POST['weight']
            modified_in_date = request.POST['in_date']
            modified_warehouse = request.POST['warehouse']
            modified_by = request.POST['by']
            modified_BLno = request.POST['BLno']
            modified_port = request.POST['port']
            modified_out_date = request.POST['out_date']
            modified_remark = request.POST['remark']
            modified_division = request.POST['division']
            modified_job_number = request.POST['job_number']
            modified_image = request.POST['image']
            modified_image1 = request.POST['image1']
            modified_image2 = request.POST['image2']
            modified_pdf_file = request.POST['pdf_file']

            # check the shipment to update
            shipment = Shipment.objects.get(company__exact=modified_company, vessel__exact=modified_vessel, supplier__exact=modified_supplier,
                                               division__exact=modified_division)
            shipment.docs = modified_docs
            shipment.odr = modified_odr
            shipment.quanty = modified_quanty
            shipment.unit = modified_unit
            shipment.size = modified_size
            shipment.weight = modified_weight
            shipment.in_date = modified_in_date
            shipment.warehouse = modified_warehouse
            shipment.by = modified_by
            shipment.BLno = modified_BLno
            shipment.port = modified_port
            shipment.out_date = modified_out_date
            shipment.remark = modified_remark
            shipment.job_number = modified_job_number
            shipment.image = modified_image
            shipment.image1 = modified_image1
            shipment.image2 = modified_image2
            shipment.pdf_file = modified_pdf_file
            shipment.correct_org = CONTEXT["staffExist"].userID

            shipment.save()

        if "addShipment_m" in request.POST:
            # load the form from the CONTEXT
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                shipment = shipmentregisterform.save()
                shipment.insert_org = CONTEXT["staffExist"].userID
                shipment.save()
                CONTEXT["shipmentRegister"] = ShipmentRegistration()
                return redirect('mainPage1')

        if "modifyShipment" in request.POST:
            shipmentchangedlist = shipmentselectedlist.split(',')

            changed_company = request.POST['company']
            changed_vessel = request.POST['vessel']
            changed_supplier = request.POST['supplier']
            changed_warehouse = request.POST['warehouse']
            changed_division = request.POST['division']
            changed_flag_status = request.POST['flag_status']
            changed_in_date = request.POST['in_dateM']
            changed_out_date = request.POST['out_dateM']
            changed_job_number = request.POST['job_number']
            changed_port = request.POST['port']
            changed_remark = request.POST['remark']

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
                    if changed_division is not "":
                        shipmentchanged.division = changed_division
                    if changed_flag_status is not "":
                        shipmentchanged.flag_status = changed_flag_status
                    if changed_in_date is not "":
                        change_in_date = changed_in_date[:4] + "-" + changed_in_date[5:6] + "-" + changed_in_date[7:8]
                        shipmentchanged.in_date = change_in_date
                    if changed_out_date is not "":
                        change_out_date = changed_out_date[:4] + "-" + changed_out_date[5:6] + "-" + changed_out_date[7:8]
                        shipmentchanged.out_date = change_out_date
                    if changed_job_number is not "":
                        shipmentchanged.job_number = changed_job_number
                    if changed_port is not "":
                        shipmentchanged.port = changed_port
                    if changed_company is not "":
                        shipmentchanged.remark = changed_remark

                    shipmentchanged.correct_org = CONTEXT["staffExist"].userID
                    shipmentchanged.save()

        if "deleteShipment" in request.POST:
            shipmentchangedlist = shipmentselectedlist.split(',')

            for id_shipmentdeleted in shipmentchangedlist:
                if id_shipmentdeleted == "":
                    pass
                else:
                    id_shipmentdeleted = int(id_shipmentdeleted)
                    Shipment.objects.filter(number__exact=id_shipmentdeleted).delete()

    else:
        CONTEXT["shipmentRegister"] = ShipmentRegistration()
        CONTEXT["shipmentModify"] = ShipmentModification()

    shipmentfilterview_result = shipmentFilterView(request)
    CONTEXT.update(shipmentfilterview_result)

    if useragent.is_pc:
        return render(request, "mainPage1.html", CONTEXT)
    else:
        return render(request, "mobilePage.html", CONTEXT)
def mainView2(request):
    shipmentfilterview_result = shipmentFilterView(request)
    return render(request, "mainPage2.html", shipmentfilterview_result)
