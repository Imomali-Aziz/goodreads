# Generated by Django 4.1.3 on 2022-11-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
