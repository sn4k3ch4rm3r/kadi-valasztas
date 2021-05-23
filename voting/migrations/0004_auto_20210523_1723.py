# Generated by Django 3.2.3 on 2021-05-23 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20210523_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('refresh_token', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='kadicandidate',
            name='id',
        ),
        migrations.AlterField(
            model_name='kadicandidate',
            name='classname',
            field=models.CharField(max_length=1, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='voting.kadicandidate')),
            ],
        ),
    ]
