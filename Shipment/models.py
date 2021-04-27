from django import forms
from django.db import models


from override_existing import OverrideExisting

# For barcode-printer
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# For filter form
import django_filters
from django_filters.widgets import RangeWidget


IMAGE_PATH = "imageShipment/"
PDF_PATH = "pdfShipment/"
BARCODE_PATH = "barcodeShipment/"

COMPANY = {
    ('CENTRA',          'CENTRA'),
    ('CMSHIP',          'CMSHIP'),
    ('DAN MO',          'DAN MO'),
    ('DORVAL',          'DORVAL'),
    ('JW',              'JW'),
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


def image_path(instance, filename):
    return IMAGE_PATH + '/{0}_{1}_{2}/{3}'.format(instance.company, instance.vessel, instance.in_date, filename)


def pdf_path(instance, filename):
    return PDF_PATH + '/{0}_{1}_{2}/{3}'.format(instance.company, instance.vessel, instance.in_date, filename)


def barcode_path(instance, filename):
    return BARCODE_PATH + '/{0}_{1}_{2}/{3}'.format(instance.company, instance.vessel, instance.in_date, filename)


class Shipment(models.Model):
    number = models.BigAutoField(primary_key=True, db_column="no")
    barcode = models.ImageField(upload_to=barcode_path, db_column="barcode", blank=True, verbose_name="Barcode Shipment",
                                storage=OverrideExisting())

    kantor_id = models.CharField(blank=True, db_column="kantor_id", max_length=40)
    insert_org = models.CharField(blank=True, db_column="insert_org", max_length=100)
    correct_org = models.CharField(blank=True, db_column="correct_org", max_length=100)
    reg_date = models.DateTimeField(auto_now=True, db_column="regdate", max_length=20)
    company = models.CharField(blank=True, db_column="company", choices=COMPANY, max_length=100, verbose_name="COMPANY")
    vessel = models.CharField(blank=True, db_column="vessel", max_length=100, verbose_name="VESSEL")
    by = models.CharField(blank=True, db_column="by1", choices=BY, max_length=50, verbose_name="BY")
    BLno = models.CharField(blank=True, db_column="blno", max_length=50, verbose_name="BLNO")
    docs = models.TextField(blank=True, db_column="doc", max_length=500, verbose_name="DOC")
    odr = models.TextField(blank=True, db_column="odr", max_length=100, verbose_name="ODR")
    supplier = models.TextField(blank=True, db_column="supplier", max_length=100, verbose_name="SUPPLIER")
    quanty = models.CharField(blank=True, db_column="qty", max_length=10, verbose_name="QTY")
    unit = models.CharField(blank=True, db_column="unit", max_length=10, verbose_name="UNIT")
    size = models.TextField(blank=True, db_column="size", max_length=100, verbose_name="SIZE")
    weight = models.CharField(blank=True, db_column="weight", max_length=10, verbose_name="WEIGHT")
    in_date = models.DateField(blank=True, null=True, db_column="in1", max_length=10, verbose_name="IN")
    warehouse = models.CharField(blank=True, db_column="whouse", max_length=100, verbose_name="W/H")
    port = models.CharField(blank=True, db_column="port", max_length=100, verbose_name="PORT")
    out_date = models.DateField(blank=True, null=True, db_column="out1", max_length=10, verbose_name="OUT")
    remark = models.TextField(blank=True, db_column="remark", max_length=500, verbose_name="REMARK")
    image = models.ImageField(upload_to=image_path, db_column="img", blank=True, null=True, verbose_name="IMG",
                              storage=OverrideExisting(), default='')
    image1 = models.ImageField(upload_to=image_path, db_column="img1", blank=True, null=True,
                               storage=OverrideExisting(), default='')
    image2 = models.ImageField(upload_to=image_path, db_column="img2", blank=True, null=True,
                               storage=OverrideExisting(), default='')
    pdf_file = models.FileField(upload_to=pdf_path, db_column="pdf", blank=True, null=True, verbose_name="PDF",
                                storage=OverrideExisting(), default='')
    division = models.CharField(blank=True, db_column="division", max_length=10, choices=DIVISION, verbose_name="DIVISION")
    flag_status = models.CharField(blank=True, db_column="flg", max_length=10, choices=FLAG, verbose_name="STATE")
    job_number = models.CharField(blank=True, db_column="jobno", max_length=50, verbose_name="JOB.NO")
    work = models.CharField(blank=True, db_column="work", max_length=10)
    work_regdate = models.DateTimeField(blank=True, null=True, db_column="work_regdate", max_length=6)

    def __str__(self):
        return self.number

    class Meta:
        db_table = "pla_databoard"

    def save(self, *args, **kwargs):  # overriding save()
        # code_type = barcode.get_barcode_class('code128')
        # byte = BytesIO()
        # if self.odr is None:
        #     code = code_type('{0}'.format(0000000000), writer=ImageWriter()).write(byte)
        # else:
        #     code = code_type('{0}'.format(self.odr), writer=ImageWriter()).write(byte)
        #
        # self.barcode.save(f'{self.odr}.png', File(byte), save=False)
        return super().save(*args, **kwargs)


class ShipmentFilter(django_filters.FilterSet):
    # companyF = django_filters.CharFilter(label="Company", lookup_expr="icontains")
    # supplierF = django_filters.CharFilter(label="Supplier", lookup_expr="icontains")
    # vesselF = django_filters.CharFilter(label="Vessel", lookup_expr="icontains")
    # warehouseF = django_filters.CharFilter(label="Warehouse", lookup_expr="icontains")
    # job_numberF = django_filters.CharFilter(label="JOB.NO", lookup_expr="icontains")
    company = django_filters.CharFilter(label="Company", lookup_expr="icontains")
    supplier = django_filters.CharFilter(label="Supplier", lookup_expr="icontains")
    vessel = django_filters.CharFilter(label="Vessel", lookup_expr="icontains")
    warehouse = django_filters.CharFilter(label="Warehouse", lookup_expr="icontains")
    job_number = django_filters.CharFilter(label="JOB.NO", lookup_expr="icontains")
    in_date_range = django_filters.DateFromToRangeFilter(field_name='in_date', widget=RangeWidget(attrs={'placeholder': 'YYYYMMDD'}))

    class Meta:
        model = Shipment
        # fields = ['companyF', 'supplierF', 'vesselF', 'warehouseF', 'job_numberF', 'in_date_range']
        fields = ['company', 'supplier', 'vessel', 'warehouse', 'job_number', 'in_date_range', 'flag_status']

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentFilter, self).__init__(*args, **kwargs)
        self.form.fields['in_date_range'].fields[0].input_formats = ['%Y%m%d']
        self.form.fields['in_date_range'].fields[1].input_formats = ['%Y%m%d']
        self.form.fields['in_date_range'].widget.attrs['style'] = 'width: 2.5cm'
        # self.form.fields['companyF'].widget.attrs['style'] = 'width: 5cm'
        # self.form.fields['supplierF'].widget.attrs['style'] = 'width: 5cm'
        # self.form.fields['vesselF'].widget.attrs['style'] = 'width: 5cm'
        # self.form.fields['warehouseF'].widget.attrs['style'] = 'width: 5cm'
        # self.form.fields['job_numberF'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['company'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['supplier'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['vessel'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['warehouse'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['job_number'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['flag_status'].widget.attrs['style'] = 'width: 5cm'

