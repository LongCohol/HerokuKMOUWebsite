# Generated by Django 3.2 on 2021-04-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shipment', '0007_auto_20210426_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='by',
            field=models.CharField(blank=True, choices=[('FDX', 'FDX'), ('DHL', 'DHL'), ('AIR', 'AIR'), ('TNT', 'TNT'), ('SFX', 'SFX'), ('SEA', 'SEA')], db_column='by1', max_length=50, verbose_name='BY'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='company',
            field=models.CharField(choices=[('CMSHIP', 'CMSHIP'), ('GOWIN', 'GOWIN'), ('KLCSM', 'KLCSM'), ('MAN', 'MAN'), ('SAEHAN', 'SAEHAN'), ('MARUBISHI', 'MARUBISHI'), ('CENTRA', 'CENTRA'), ('FORTUNE WILL', 'FORTUNE WILL'), ('DORVAL', 'DORVAL'), ('GOLTENS', 'GOLTENS'), ('POSSM', 'POSSM'), ('SEOYANG', 'SEOYANG'), ('KSS', 'KSS'), ('EUCO', 'EUCO'), ('SUNAMI', 'SUNAMI'), ('SUNRIO', 'SUNRIO'), ('INTERGIS', 'INTERGIS'), ('이강공사', '이강공사'), ('STX', 'STX'), ('보성상사', '보성상사'), ('DAN MO', 'DAN MO'), ('KNK', 'KNK'), ('GLOVIS', 'GLOVIS'), ('오션마린', '오션마린'), ('SHI OCEAN', 'SHI OCEAN')], db_column='company', max_length=100, verbose_name='COMPANY'),
        ),
    ]
