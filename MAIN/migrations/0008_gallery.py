# Generated by Django 5.1.4 on 2025-06-16 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIN', '0007_alter_contact_delivery_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery_images/')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]
