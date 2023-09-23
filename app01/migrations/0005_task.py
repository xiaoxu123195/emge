# Generated by Django 4.1.6 on 2023-03-03 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0004_admin"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "紧急"), (2, "重要"), (3, "临时")],
                        default=1,
                        verbose_name="级别",
                    ),
                ),
                ("title", models.CharField(max_length=64, verbose_name="标题")),
                ("detail", models.TextField(verbose_name="详细信息")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.admin",
                        verbose_name="负责人",
                    ),
                ),
            ],
        ),
    ]
