# Generated by Django 5.1.4 on 2025-02-06 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIN', '0006_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='number_of_prints',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
