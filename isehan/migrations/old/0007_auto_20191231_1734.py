# Generated by Django 2.1.1 on 2019-12-31 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isehan', '0006_auto_20191231_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description1',
            new_name='description',
        ),
    ]