# Generated by Django 3.1 on 2023-06-27 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230627_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default/default-user.jpeg', upload_to='userprofile'),
        ),
    ]
