# Generated by Django 3.1.2 on 2020-10-14 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_pathway'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetGene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mirna', models.CharField(max_length=100)),
                ('gene', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Validations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mirna', models.CharField(max_length=100)),
                ('pathway', models.CharField(max_length=200)),
                ('gene', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
    ]
