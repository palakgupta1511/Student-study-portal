# Generated by Django 3.1.2 on 2024-04-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboad', '0008_usercategoryattempts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
