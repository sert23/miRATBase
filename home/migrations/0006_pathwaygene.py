# Generated by Django 3.1.2 on 2020-10-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_mirna_mirgenedb'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathwayGene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pathway', models.CharField(max_length=200)),
                ('gene', models.CharField(max_length=100)),
                ('db', models.CharField(max_length=100)),
                ('identifier', models.CharField(max_length=100)),
            ],
        ),
    ]