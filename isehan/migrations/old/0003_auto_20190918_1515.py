# Generated by Django 2.1.1 on 2019-09-18 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isehan', '0002_auto_20190918_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '子カテゴリー', 'verbose_name_plural': '子カテゴリー'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='parent_category',
            new_name='p_category',
        ),
    ]
