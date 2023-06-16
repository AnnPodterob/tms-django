# Generated by Django 4.2 on 2023-06-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('INITIAL', 'Initial'), ('COMPLETED', 'Completed'), ('DELIVERED', 'Delivered')], default='INITIAL', max_length=25),
        ),
    ]
