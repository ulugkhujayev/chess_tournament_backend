# Generated by Django 4.2.14 on 2024-07-18 04:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("current_round", models.IntegerField(default=1)),
            ],
        ),
    ]
