# Generated by Django 5.0.6 on 2024-06-02 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
