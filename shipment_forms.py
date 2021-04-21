from django import forms
from Shipment.models import Shipment


class ShipmentRegistration(forms.ModelForm):
    in_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d'), label="IN")
    out_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d'), label="OUT")

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
