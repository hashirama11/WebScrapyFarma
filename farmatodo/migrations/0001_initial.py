# Generated by Django 5.2 on 2025-05-01 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyWebFarmatodo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=250)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('url', models.CharField(max_length=500)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
