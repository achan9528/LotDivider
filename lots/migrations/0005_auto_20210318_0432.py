# Generated by Django 2.2.4 on 2021-03-18 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0004_remove_taxlot_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxlot',
            name='acquisitionDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
