from django import forms
from Shipment.models import Shipment


COMPANY = {
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
    ("D", "D"),
    ("B", "B"),
    ("L", "L"),
}
FLAG = {
    ("BLANK", "BLANK"),
    ("STAY", "STAY"),
    ("START", "START"),
    ("COMPLETED", "COMPLETED"),
}


class ShipmentRegistration(forms.ModelForm):
    in_date = forms.DateField(required=False, input_formats=['%Y%m%d'], widget=forms.DateInput(format='%Y%m%d'), label="IN")
    out_date = forms.DateField(required=False, input_formats=['%Y%m%d'], widget=forms.DateInput(format='%Y%m%d'), label="OUT")

    class Meta:
        model = Shipment
        fields = ('company', 'vessel', 'docs', 'odr', 'supplier', 'quanty', 'unit', 'size', 'weight', 'in_date',
                  'warehouse', 'by', 'BLno', 'port', 'out_date', 'remark', 'job_number', 'image', 'image1', 'image2',
                  'pdf_file', 'division')

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentRegistration, self).__init__(*args, **kwargs)
        self.fields['docs'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'
        self.fields['odr'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'
        self.fields['supplier'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'
        self.fields['size'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'
        self.fields['remark'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'

        self.fields['company'].widget.attrs['style'] = 'width: 5cm'
        self.fields['vessel'].widget.attrs['style'] = 'width: 5cm'
        self.fields['quanty'].widget.attrs['style'] = 'width: 5cm'
        self.fields['unit'].widget.attrs['style'] = 'width: 5cm'
        self.fields['weight'].widget.attrs['style'] = 'width: 5cm'
        self.fields['in_date'].widget.attrs['style'] = 'width: 5cm'
        self.fields['BLno'].widget.attrs['style'] = 'width: 5cm'
        self.fields['port'].widget.attrs['style'] = 'width: 5cm'
        self.fields['out_date'].widget.attrs['style'] = 'width: 5cm'
        self.fields['job_number'].widget.attrs['style'] = 'width: 5cm'
        self.fields['warehouse'].widget.attrs['style'] = 'width: 2cm'
        self.fields['by'].widget.attrs['style'] = 'width: 2cm'
        self.fields['division'].widget.attrs['style'] = 'width: 2cm'


class ShipmentModification(forms.ModelForm):
    in_dateM = forms.DateField(required=False, input_formats=['%Y%m%d'], widget=forms.DateInput(format='%Y%m%d'), label="Date In")
    out_dateM = forms.DateField(required=False, input_formats=['%Y%m%d'], widget=forms.DateInput(format='%Y%m%d'), label="Date Out")

    supplier = forms.CharField(required=False, max_length=100, label="SUPPLIER")
    # remark = forms.CharField(required=False, max_length=500, label="REMARK")
    # vessel = forms.CharField(max_length=100, label="VESSEL")

    class Meta:
        model = Shipment
        fields = ['company', 'vessel', 'supplier', 'warehouse', 'division', 'flag_status',
                  'in_dateM', 'out_dateM', 'job_number', 'port', 'remark']

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentModification, self).__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['vessel'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['supplier'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['warehouse'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['job_number'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['division'].widget.attrs['style'] = 'width: 2cm; height: 0.8cm'
        self.fields['flag_status'].widget.attrs['style'] = 'width: 2cm; height: 0.8cm'
        self.fields['in_dateM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['out_dateM'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['port'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
        self.fields['remark'].widget.attrs['style'] = 'width: 5cm; height:1.5cm;'
        self.fields['port'].widget.attrs['style'] = 'width: 5cm; height: 0.8cm'
