# Generated by Django 3.2.4 on 2021-12-06 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='meals-pics')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('tags', models.CharField(choices=[('foods', 'foods'), ('beverages', 'beverages')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderstatus', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('ordercode', models.CharField(max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderitemID', models.PositiveSmallIntegerField(auto_created=True, null=True)),
                ('ordertype', models.CharField(choices=[('reserve', 'reserve'), ('takeaway', 'takeaway')], max_length=20)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Regent.order')),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Regent.meal')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Regent.profile'),
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField()),
                ('ordertype', models.CharField(choices=[('reserve', 'reserve'), ('takeaway', 'takeaway')], max_length=20)),
                ('table', models.IntegerField(null=True)),
                ('time', models.TimeField()),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Regent.order')),
            ],
        ),
    ]
