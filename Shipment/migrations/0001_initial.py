# Generated by Django 3.2 on 2021-05-12 12:43

import Shipment.models
from django.db import migrations, models
import django.utils.timezone
import override_existing


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('number', models.BigAutoField(db_column='no', primary_key=True, serialize=False)),
                ('barcode', models.ImageField(blank=True, db_column='barcode', storage=override_existing.OverrideExisting(), upload_to=Shipment.models.barcode_path, verbose_name='Barcode Shipment')),
                ('kantor_id', models.CharField(blank=True, db_column='kantor_id', max_length=40)),
                ('insert_org', models.CharField(blank=True, db_column='insert_org', max_length=100)),
                ('correct_org', models.CharField(blank=True, db_column='correct_org', max_length=100)),
                ('reg_date', models.DateTimeField(auto_now=True, db_column='regdate', max_length=20)),
                ('company', models.CharField(blank=True, choices=[('CENTRA', 'CENTRA'), ('이강공사', '이강공사'), ('DAN MO', 'DAN MO'), ('SUNAMI', 'SUNAMI'), ('KLCSM', 'KLCSM'), ('오션마린', '오션마린'), ('EUCO', 'EUCO'), ('SAEHAN', 'SAEHAN'), ('JW', 'JW'), ('SHI OCEAN', 'SHI OCEAN'), ('GOWIN', 'GOWIN'), ('KNK', 'KNK'), ('SUNRIO', 'SUNRIO'), ('FORTUNE WILL', 'FORTUNE WILL'), ('CMSHIP', 'CMSHIP'), ('GLOVIS', 'GLOVIS'), ('보성상사', '보성상사'), ('MAN', 'MAN'), ('MARUBISHI', 'MARUBISHI'), ('SEOYANG', 'SEOYANG'), ('STX', 'STX'), ('GOLTENS', 'GOLTENS'), ('INTERGIS', 'INTERGIS'), ('DORVAL', 'DORVAL'), ('POSSM', 'POSSM'), ('KSS', 'KSS')], db_column='company', max_length=100, verbose_name='COMPANY')),
                ('vessel', models.CharField(blank=True, db_column='vessel', max_length=100, verbose_name='VESSEL')),
                ('by', models.CharField(blank=True, db_column='by1', max_length=50, verbose_name='BY')),
                ('BLno', models.CharField(blank=True, db_column='blno', max_length=50, verbose_name='BLNO')),
                ('docs', models.TextField(blank=True, db_column='doc', max_length=500, verbose_name='DOC')),
                ('odr', models.TextField(blank=True, db_column='odr', max_length=100, verbose_name='ODR')),
                ('supplier', models.TextField(blank=True, db_column='supplier', max_length=100, verbose_name='SUPPLIER')),
                ('quanty', models.CharField(blank=True, db_column='qty', max_length=10, verbose_name='QTY')),
                ('unit', models.CharField(blank=True, db_column='unit', max_length=10, verbose_name='UNIT')),
                ('size', models.TextField(blank=True, db_column='size', max_length=100, verbose_name='SIZE')),
                ('weight', models.CharField(blank=True, db_column='weight', max_length=10, verbose_name='WEIGHT')),
                ('in_date', models.DateField(blank=True, db_column='in1', default=django.utils.timezone.now, max_length=10, null=True, verbose_name='IN')),
                ('warehouse', models.CharField(blank=True, db_column='whouse', max_length=100, verbose_name='W/H1')),
                ('warehouse2', models.CharField(blank=True, db_column='whouse2', max_length=100, verbose_name='W/H2')),
                ('port', models.CharField(blank=True, db_column='port', max_length=100, verbose_name='PORT')),
                ('out_date', models.DateField(blank=True, db_column='out1', max_length=10, null=True, verbose_name='OUT')),
                ('remark', models.TextField(blank=True, db_column='remark', max_length=500, verbose_name='REMARK')),
                ('memo', models.TextField(blank=True, db_column='memo', max_length=1000, verbose_name='MEMO')),
                ('image', models.ImageField(blank=True, db_column='img', default='', max_length=500, null=True, storage=override_existing.OverrideExisting(), upload_to=Shipment.models.image_path, verbose_name='IMG')),
                ('image1', models.ImageField(blank=True, db_column='img1', default='', max_length=500, null=True, storage=override_existing.OverrideExisting(), upload_to=Shipment.models.image_path)),
                ('image2', models.ImageField(blank=True, db_column='img2', default='', max_length=500, null=True, storage=override_existing.OverrideExisting(), upload_to=Shipment.models.image_path)),
                ('pdf_file', models.FileField(blank=True, db_column='pdf', default='', max_length=500, null=True, storage=override_existing.OverrideExisting(), upload_to=Shipment.models.pdf_path, verbose_name='PDF')),
                ('division', models.CharField(blank=True, choices=[('B', 'B'), ('L', 'L'), ('D', 'D')], db_column='division', max_length=10, verbose_name='DIVISION')),
                ('flag_status', models.CharField(blank=True, choices=[('START', 'START'), ('STAY2', 'STAY2'), ('BLANK', 'BLANK'), ('STAY1', 'STAY1'), ('COMPLETED', 'COMPLETED')], db_column='flg', max_length=10, verbose_name='STATE')),
                ('job_number', models.CharField(blank=True, db_column='jobno', max_length=50, verbose_name='JOB.NO')),
                ('work', models.CharField(blank=True, db_column='work', max_length=10)),
                ('work_regdate', models.DateTimeField(blank=True, db_column='work_regdate', max_length=20, null=True)),
            ],
            options={
                'db_table': 'pla_databoard',
            },
        ),
    ]
