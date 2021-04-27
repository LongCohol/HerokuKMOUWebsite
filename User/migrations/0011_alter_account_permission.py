# Generated by Django 3.2 on 2021-04-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_alter_account_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='permission',
            field=models.CharField(choices=[('Read + Modify', 'Read + Modify'), ('Read Only', 'Read Only')], default='Read + Modify', max_length=30, verbose_name='Permission'),
        ),
    ]
