# Generated by Django 3.2.4 on 2021-12-03 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Regent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordercode',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
