from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from User.models import Account
# from Operator.models import Operator
# from Company.models import Company
# from Supplier.models import Supplier


PERMISSION = {
    ("Read Only", "Read Only"),
    ("Read + Modify", "Read + Modify"),
}


class OperatorLogin(forms.ModelForm):
    userID = forms.CharField(label="Staff ID", widget=forms.TextInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('userID', 'password')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(OperatorLogin, self).__init__(*args, **kwargs)
        self.fields['userID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['password'].widget.attrs['style'] = 'width: 5cm; height: 1cm'

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data.get('userID')
            password = self.cleaned_data.get('password')

            if not authenticate(userID=username, password=password):
                raise forms.ValidationError("Invalid account. Please try again")
    ###########################################################


class OperatorForm(forms.ModelForm):
    oprID = forms.CharField()
    oprPassword = forms.CharField()
    oprPermission = forms.ChoiceField(choices=PERMISSION)

    class Meta:
        model = Account
        fields = ('oprID', 'oprPassword', 'oprPermission')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(OperatorForm, self).__init__(*args, **kwargs)
        self.fields['oprID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['oprPassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['oprPermission'].widget.attrs['style'] = 'width: 5cm; height: 1cm'

    def save(self, commit=True):
        super().save(commit=False)
        userID = self.cleaned_data.get('oprID')
        password = self.cleaned_data.get('oprPassword')
        permission = self.cleaned_data.get('oprPermission')
        isOpr = True
        account = Account.objects.create(userID=userID, password=password, rawPassword=password, permission=permission,
                                         companyName="", email="", isOpr=isOpr, vesselList="")

        if commit:
            account.password = make_password(password)
            account.save()
        return account
    ###########################################################


class SupplierForm(forms.ModelForm):
    splID = forms.CharField()
    splName = forms.CharField()
    splPassword = forms.CharField()

    class Meta:
        model = Account
        fields = ('splID', 'splName', 'splPassword')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields['splID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['splName'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['splPassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'

    def save(self, commit=True):
        super().save(commit=False)
        userID = self.cleaned_data.get('splID')
        password = self.cleaned_data.get('splPassword')
        companyName = self.cleaned_data.get('splName')
        isSpl = True
        account = Account.objects.create(userID=userID, password=password, rawPassword=password, permission="Read Only",
                                         companyName=companyName, email="", isSpl=isSpl, vesselList="")

        if commit:
            account.password = make_password(password)
            account.save()
        return account
    ###########################################################


class CompanyForm(forms.ModelForm):
    cpnID = forms.CharField()
    cpnName = forms.CharField()
    cpnEmail = forms.EmailField()
    cpnPassword = forms.CharField()
    cpnVesselList = forms.CharField()

    class Meta:
        model = Account
        fields = ('cpnID', 'cpnName', 'cpnEmail', 'cpnPassword', 'cpnVesselList')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['cpnID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['cpnName'].widget.attrs['style'] = 'width: 4cm; height: 1cm'
        self.fields['cpnEmail'].widget.attrs['style'] = 'width: 7cm; height: 1cm'
        self.fields['cpnPassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
        self.fields['cpnVesselList'].widget.attrs['style'] = 'width: 21cm; height: 2cm'

    def save(self, commit=True):
        super().save(commit=False)
        userID = self.cleaned_data.get('cpnID')
        password = self.cleaned_data.get('cpnPassword')
        email = self.cleaned_data.get('cpnEmail')
        companyName = self.cleaned_data.get('cpnName')
        vesselList = self.cleaned_data.get('cpnVesselList')
        isCpn = True
        account = Account.objects.create(userID=userID, password=password, rawPassword=password, permission="Read Only",
                                         companyName=companyName, email=email, isCpn=isCpn, vesselList=vesselList)

        if commit:
            account.password = make_password(password)
            account.save()
        return account
    ###########################################################

# class OperatorForm(forms.ModelForm):
#     class Meta:
#         model = Operator
#         fields = ('operatorID', 'OPRpassword', 'permission')
#
#     def __init__(self, *args, **kwargs):
#         # Set up dimension for fields with CSS style
#         super(OperatorForm, self).__init__(*args, **kwargs)
#         self.fields['operatorID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['OPRpassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['permission'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#
#     def save(self, commit=True):
#         super().save(commit=False)
#         oprID = self.cleaned_data.get('operatorID')
#         password = self.cleaned_data.get('OPRpassword')
#         permission = self.cleaned_data.get('permission')
#         operator = Operator.objects.create(operatorID=oprID, OPRpassword=password, permission=permission)
#
#         if commit:
#             operator.save()
#         return operator
#     ###########################################################
#
#
# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ('supplierID', 'supplierName', 'SPLpassword')
#
#     def __init__(self, *args, **kwargs):
#         # Set up dimension for fields with CSS style
#         super(SupplierForm, self).__init__(*args, **kwargs)
#         self.fields['supplierID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['supplierName'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['SPLpassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#
#     def save(self, commit=True):
#         super().save(commit=False)
#         splID = self.cleaned_data.get('supplierID')
#         splName = self.cleaned_data.get('supplierName')
#         password = self.cleaned_data.get('SPLpassword')
#         supplier = Supplier.objects.create(supplierID=splID, supplierName=splName, SPLpassword=password)
#
#         if commit:
#             supplier.save()
#         return supplier
#     ###########################################################
#
#
# class CompanyForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ('companyID', 'companyName', 'companyEmail', 'CPNpassword', 'vesselList')
#
#     def __init__(self, *args, **kwargs):
#         # Set up dimension for fields with CSS style
#         super(CompanyForm, self).__init__(*args, **kwargs)
#         self.fields['companyID'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['companyName'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['companyEmail'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['CPNpassword'].widget.attrs['style'] = 'width: 5cm; height: 1cm'
#         self.fields['vesselList'].widget.attrs['style'] = 'width: 20cm; height: 3cm'
#
#     def save(self, commit=True):
#         super().save(commit=False)
#         cpnID = self.cleaned_data.get('companyID')
#         cpnName = self.cleaned_data.get('companyName')
#         cpnEmail = self.cleaned_data.get('companyEmail')
#         password = self.cleaned_data.get('CPNpassword')
#         vesselList = self.cleaned_data.get('vesselList')
#
#         company = Company.objects.create(companyID=cpnID, companyName=cpnName, companyEmail=cpnEmail, CPNpassword=password,
#                                          vesselList=vesselList)
#         if commit:
#             company.save()
#         return company
#     ###########################################################