# Generated by Django 3.2.3 on 2021-05-22 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KadiCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=10)),
                ('lastname', models.CharField(max_length=40)),
                ('nickname', models.CharField(max_length=20)),
                ('classname', models.CharField(max_length=1)),
                ('logo', models.ImageField(upload_to='')),
            ],
        ),
    ]