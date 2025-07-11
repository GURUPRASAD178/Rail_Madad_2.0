# Generated by Django 5.0.7 on 2025-06-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RailApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='category',
            field=models.CharField(default='Uncategorized', max_length=100),
        ),
        migrations.AddField(
            model_name='complaint',
            name='phone',
            field=models.CharField(default=22062025, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='subject',
            field=models.CharField(default=22062025, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='complaint',
            name='complaint_image',
            field=models.ImageField(blank=True, null=True, upload_to='complaint_images/'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]
