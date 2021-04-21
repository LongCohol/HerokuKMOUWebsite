from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
# from django_user_agents.utils import get_user_agent

from django.core import serializers

from Shipment.views import shipmentRegisterView, shipmentFilterView
from User.models import Account
# from Operator.models import Operator
# from Supplier.models import Supplier
# from Company.models import Company
from account_forms import OperatorForm, SupplierForm, CompanyForm, OperatorLogin
from shipment_forms import ShipmentRegistration

CONTEXT = {}
RESULT_PER_PAGE = 100


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
                spl = Account.objects.get(splID__exact=splID)
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


def frontView(request):
    staffloginview_result = staffLoginView(request)
    CONTEXT.update(staffloginview_result)

    if request.method == "POST":
        # check the button of staffLogin.html
        if "staffloginform" in request.POST:
            # if there exists an account with the authentication
            account = CONTEXT["staffExist"]
            if account is not None:
                login(request, account)
                return redirect('staff_redirect')

    return render(request, "frontpage.html", CONTEXT)


def staffLoginView(request):
    # IF this is POST request:
    if request.method == "POST":
        account = None
        formOperatorLogin = OperatorLogin(request.POST)

        if formOperatorLogin.is_valid():
            username = formOperatorLogin.cleaned_data.get('userID')
            password = formOperatorLogin.cleaned_data.get('password')
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


def mainView(request):
    shipmentregisterview_result = shipmentRegisterView(request)
    CONTEXT.update(shipmentregisterview_result)

    if request.method == "POST":
        # check the button of shipmentRegister.html
        if "addShipment" in request.POST:
            # load the form from the CONTEXT
            shipmentregisterform = CONTEXT["shipmentRegister"]
            if shipmentregisterform.is_valid():
                shipmentregisterform.save()
                CONTEXT["shipmentRegister"] = ShipmentRegistration()
                return redirect('mainPage')
    else:
        CONTEXT["shipmentRegister"] = ShipmentRegistration()

    shipmentfilterview_result = shipmentFilterView(request)
    CONTEXT.update(shipmentfilterview_result)
    return render(request, "mainPage.html", CONTEXT)
