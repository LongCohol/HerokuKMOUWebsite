from datetime import date
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from Shipment.models import Shipment


COMPANY = {
    ('',          '------------'),
    ('CENTRA',          'CENTRA'),
    ('CMSHIP',          'CMSHIP'),
    ('DAN MO',          'DAN MO'),
    ('DORVAL',          'DORVAL'),
    ('EUCO',            'EUCO'),
    ('FORTUNE WILL',    'FORTUNE WILL'),
    ('GLOVIS',          'GLOVIS'),
    ('GOLTENS',         'GOLTENS'),
    ('GOWIN',           'GOWIN'),
    ('INTERGIS',        'INTERGIS'),
    ('KLCSM',           'KLCSM'),
    ('KNK',             'KNK'),
    ('KSS',             'KSS'),
    ('MAN',             'MAN'),
    ('MARUBISHI',       'MARUBISHI'),
    ('POSSM',           'POSSM'),
    ('SAEHAN',          'SAEHAN'),
    ('SEOYANG',         'SEOYANG'),
    ('SHI OCEAN',       'SHI OCEAN'),
    ('STX',             'STX'),
    ('SUNAMI',          'SUNAMI'),
    ('SUNRIO',          'SUNRIO'),
    ('보성상사',        '보성상사'),
    ('오션마린',        '오션마린'),
    ('이강공사',        '이강공사'),
}
WAREHOUSE = {
    ('SL', 'SL'),
    ('KIM-IGS', 'KIM-IGS'),
    ('ICN-IGS', 'ICN-IGS'),
}

BY = {
    ('DHL', 'DHL'),
    ('FDX', 'FDX'),
    ('TNT', 'TNT'),
    ('AIR', 'AIR'),
    ('SEA', 'SEA'),
    ('SFX', 'SFX'),
}
DIVISION = {
    ('', '---------'),
    ("D", "D"),
    ("B", "B"),
    ("L", "L"),
}
FLAG = {
    ("BLANK", "BLANK"),
    ("STAY", "STAY1"),
    ("STAY2", "STAY2"),
    ("START", "START"),
    ("COMPLETED", "COMPLETED"),
}

DATE_ERRORS = {
    'invalid': "Wrong date format. Please check (YYYYMMDD)",
}
BRIEF_DATE_ERRORS = {
    'invalid': "Must be YYYYMMDD",
}


class ShipmentRegistration(forms.ModelForm):
    in_date = forms.DateField(required=False, initial=date.today(), input_formats=['%Y%m%d'],
                              widget=forms.DateInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}), label="IN",
                              error_messages=DATE_ERRORS)
    out_date = forms.DateField(required=False, input_formats=['%Y%m%d'],
                               widget=forms.DateInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}), label="OUT",
                               error_messages=DATE_ERRORS)
    # division = forms.ChoiceField(required=False, choices=DIVISION, label="DIVISION", initial="")

    class Meta:
        model = Shipment
        fields = ('company', 'vessel', 'docs', 'odr', 'supplier', 'quanty', 'unit', 'size', 'weight', 'in_date',
                  'warehouse', 'warehouse2', 'by', 'BLno', 'port', 'out_date', 'remark', 'memo',
                  'job_number', 'image', 'image1', 'image2', 'pdf_file', 'division')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentRegistration, self).__init__(*args, **kwargs)
        self.fields['docs'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['odr'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['supplier'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['size'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['remark'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['memo'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; margin-top:5px; font-size:12px'
        self.fields['image'].widget.attrs['style'] = 'height:0.7cm; font-size: 12px; margin-bottom:1px; font-size:12px'
        self.fields['image1'].widget.attrs['style'] = 'height:0.7cm; font-size: 12px; margin-bottom:1px; font-size:12px'
        self.fields['image2'].widget.attrs['style'] = 'height:0.7cm; font-size: 12px; margin-bottom:1px; font-size:12px'
        self.fields['pdf_file'].widget.attrs['style'] = 'height:0.7cm; font-size: 12px; margin-bottom:1px; font-size:12px'

        self.fields['company'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align-last: center'
        self.fields['vessel'].widget.attrs['style'] = 'width: 4.7cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['quanty'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['unit'].widget.attrs['style'] = 'width: 3cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['weight'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; margin-top:5px; margin-bottom:5px; text-align: center'
        self.fields['in_date'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['BLno'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['port'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['out_date'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['job_number'].widget.attrs['style'] = 'width: 5cm; height:0.8cm; font-size:12px; text-align: center'
        self.fields['warehouse'].widget.attrs['style'] = 'width: 3cm; height:0.8cm; font-size:12px; margin-top:5px; margin-bottom:5px; text-align: center'
        self.fields['warehouse2'].widget.attrs['style'] = 'width: 3cm; height:0.8cm; font-size:12px; margin-top:5px; margin-bottom:5px; text-align: center'
        self.fields['by'].widget.attrs['style'] = 'width: 3cm; height:0.8cm; font-size:12px; margin-top:5px; margin-bottom:5px; text-align: center'
        self.fields['division'].widget.attrs['style'] = 'width: 2cm; height:0.8cm; font-size:12px; text-align-last: center'


class ShipmentModification(forms.ModelForm):
    in_dateM = forms.DateField(required=False, label="Date In", input_formats=['%Y%m%d'],
                               widget=forms.DateInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}),
                               error_messages=BRIEF_DATE_ERRORS)
    out_dateM = forms.DateField(required=False, label="Date Out", input_formats=['%Y%m%d'],
                                widget=forms.DateInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}),
                                error_messages=BRIEF_DATE_ERRORS)
    # in_dateM = forms.DateField(required=False, input_formats=['%Y%m%d'],
    #                            widget=DatePickerInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}), label="Date In",
    #                            error_messages=BRIEF_DATE_ERRORS)
    # out_dateM = forms.DateField(required=False, input_formats=['%Y%m%d'],
    #                             widget=DatePickerInput(format='%Y%m%d', attrs={'placeholder': 'YYYYMMDD'}), label="Date Out",
    #                             error_messages=BRIEF_DATE_ERRORS)

    companyM = forms.ChoiceField(required=False, choices=COMPANY, label="COMPANY", initial="")
    vesselM = forms.CharField(required=False, max_length=100, label="VESSEL")
    supplierM = forms.CharField(required=False, max_length=100, label="SUPPLIER")
    warehouseM = forms.CharField(required=False, max_length=100, label="WAREHOUSE")
    warehouse2M = forms.CharField(required=False, max_length=100, label="WAREHOUSE2")
    divisionM = forms.ChoiceField(required=False, choices=DIVISION, label="DIVISION", initial="")
    flag_statusM = forms.ChoiceField(required=False, choices=FLAG, label="STATE", initial="BLANK")
    job_numberM = forms.CharField(required=False, label="JOB.NO")
    portM = forms.CharField(required=False, label="PORT")
    remarkM = forms.CharField(required=False, label="REMARK")
    memoM = forms.CharField(required=False, label="MEMO")
    docsM = forms.CharField(required=False, label="DOC")
    odrM = forms.CharField(required=False, label="ODR")
    quantyM = forms.CharField(required=False, label="QTY")
    unitM = forms.CharField(required=False, label="UNIT")
    sizeM = forms.CharField(required=False, label="SIZE")
    weightM = forms.CharField(required=False, label="WEIGHT")
    BLnoM = forms.CharField(required=False, label="BLNO")

    class Meta:
        model = Shipment
        fields = ['companyM', 'vesselM', 'supplierM', 'warehouseM', 'divisionM', 'flag_statusM',
                  'in_dateM', 'out_dateM', 'job_numberM', 'portM', 'remarkM', 'memoM']

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentModification, self).__init__(*args, **kwargs)
        self.fields['companyM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align-last:center'
        self.fields['vesselM'].widget.attrs['style'] = 'width: 4.7cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['supplierM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['warehouseM'].widget.attrs['style'] = 'width: 2.7cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['warehouse2M'].widget.attrs['style'] = 'width: 2.7cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['job_numberM'].widget.attrs['style'] = 'width: 3cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['divisionM'].widget.attrs['style'] = 'width: 2cm; height: 0.8cm; font-size:12px; text-align-last:center'
        self.fields['flag_statusM'].widget.attrs['style'] = 'width: 3cm; height: 0.8cm; font-size:12px; text-align-last:center'
        self.fields['in_dateM'].widget.attrs['style'] = 'width: 2.5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['out_dateM'].widget.attrs['style'] = 'width: 2.5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['portM'].widget.attrs['style'] = 'width: 3.5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['remarkM'].widget.attrs['style'] = 'width: 4cm; height:0.8cm; font-size:12px; text-align:center'
        self.fields['memoM'].widget.attrs['style'] = 'width: 4.5cm; height:0.8cm; font-size:12px; text-align:center'
        self.fields['docsM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['odrM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['quantyM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['unitM'].widget.attrs['style'] = 'width: 4.7cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['sizeM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['weightM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'
        self.fields['BLnoM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm; font-size:12px; text-align:center'


class WarehouseFilter(forms.ModelForm):
    wh = forms.CharField(required=False, label="Warehouse")

    class Meta:
        model = Shipment
        # fields = ['companyF', 'supplierF', 'vesselF', 'warehouseF', 'job_numberF', 'in_date_range']
        fields = ['wh']

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(WarehouseFilter, self).__init__(*args, **kwargs)
        self.fields['wh'].widget.attrs['style'] = 'width: 3cm; height: 0.8cm; font-size: 12px; text-align : center'