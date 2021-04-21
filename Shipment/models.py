from django.db import models
from override_existing import OverrideExisting

# For barcode-printer
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# For filter form
import django_filters


IMAGE_PATH = "imageShipment/"
PDF_PATH = "pdfShipment/"
BARCODE_PATH = "barcodeShipment/"


def image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return IMAGE_PATH + '/{0}/{1}'.format(instance.odr, filename)


def pdf_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return PDF_PATH + '/{0}/{1}'.format(instance.odr, filename)


def barcode_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return BARCODE_PATH + '/{0}/{1}'.format(instance.odr, filename)


class Shipment(models.Model):
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

    number = models.BigAutoField(primary_key=True, db_column="no")
    barcode = models.ImageField(upload_to=barcode_path, db_column="barcode", blank=True, verbose_name="Barcode Shipment",
                                storage=OverrideExisting())

    kantor_id = models.CharField(blank=True, db_column="kantor_id", max_length=40)
    insert_org = models.CharField(blank=True, db_column="insert_org", max_length=100)
    correct_org = models.CharField(blank=True, db_column="correct_org", max_length=100)
    reg_date = models.DateTimeField(auto_now=True, db_column="regdate", max_length=6)
    company = models.CharField(null=False, db_column="company", choices=COMPANY, max_length=100, verbose_name="COMPANY")
    vessel = models.CharField(blank=True, db_column="vessel", max_length=100, verbose_name="VESSEL")
    by = models.CharField(blank=True, db_column="by1", choices=BY, max_length=50, verbose_name="BY")
    BLno = models.CharField(blank=True, db_column="blno", max_length=50, verbose_name="BLNO")
    docs = models.TextField(blank=True, db_column="doc", max_length=500, verbose_name="DOC")
    odr = models.TextField(blank=False, db_column="odr", max_length=100, verbose_name="ODR")
    supplier = models.TextField(blank=True, db_column="supplier", max_length=100, verbose_name="SUPPLIER")
    quanty = models.CharField(blank=True, db_column="qty", max_length=10, verbose_name="QTY")
    unit = models.CharField(blank=True, db_column="unit", max_length=10, verbose_name="UNIT")
    size = models.TextField(blank=True, db_column="size", max_length=100, verbose_name="SIZE")
    weight = models.CharField(blank=True, db_column="weight", max_length=10, verbose_name="WEIGHT")
    in_date = models.DateField(blank=True, null=True, db_column="in1", max_length=10, verbose_name="IN")
    warehouse = models.CharField(blank=True, db_column="whouse", choices=WAREHOUSE, max_length=100, verbose_name="W/H")
    port = models.CharField(blank=True, db_column="port", max_length=100, verbose_name="PORT")
    out_date = models.DateField(blank=True, null=True, db_column="out1", max_length=10, verbose_name="OUT")
    remark = models.TextField(blank=True, db_column="remark", max_length=500, verbose_name="REMARK")
    image = models.ImageField(upload_to=image_path, db_column="img", blank=True, verbose_name="IMG",
                              storage=OverrideExisting())
    image1 = models.ImageField(upload_to=image_path, db_column="img1", blank=True,
                               storage=OverrideExisting())
    image2 = models.ImageField(upload_to=image_path, db_column="img2", blank=True,
                               storage=OverrideExisting())
    pdf_file = models.FileField(upload_to=pdf_path, db_column="pdf", blank=True, verbose_name="PDF",
                                storage=OverrideExisting())
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
        code_type = barcode.get_barcode_class('code128')
        byte = BytesIO()
        if self.odr is None:
            code = code_type('{0}'.format(0000000000), writer=ImageWriter()).write(byte)
        else:
            code = code_type('{0}'.format(self.odr), writer=ImageWriter()).write(byte)

        self.barcode.save(f'{self.odr}.png', File(byte), save=False)
        return super().save(*args, **kwargs)


class ShipmentFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(lookup_expr='iexact')
    odr = django_filters.CharFilter(lookup_expr="icontains")
    in_date = django_filters.DateFilter(label="In Date (yyyy-mm-dd)", input_formats=['%Y-%m-%d'])
    out_date = django_filters.DateFilter(label="Out Date (yyyy-mm-dd)", input_formats=['%Y-%m-%d'])

    class Meta:
        model = Shipment
        fields = ['company', 'odr', 'in_date', 'out_date']

    def __init__(self, *args, **kwargs):
        # Set up dimension for fields with CSS style
        super(ShipmentFilter, self).__init__(*args, **kwargs)
        self.form.fields['company'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['odr'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['in_date'].widget.attrs['style'] = 'width: 5cm'
        self.form.fields['out_date'].widget.attrs['style'] = 'width: 5cm'
