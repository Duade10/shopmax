# Generated by Django 4.2.4 on 2023-08-07 07:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0004_rename_quantity_cartitem_total_quantity_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitemvariation",
            old_name="total_quantity",
            new_name="quantity",
        ),
    ]
