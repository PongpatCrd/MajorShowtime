# Generated by Django 2.1 on 2020-02-27 07:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('major_showtime', '0003_auto_20200226_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchesBestTimeDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch_nickname', models.CharField(max_length=5)),
                ('best_time', models.CharField(max_length=5)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'branches_best_time_detail',
            },
        ),
        migrations.AlterIndexTogether(
            name='branchesbesttimedetail',
            index_together={('branch_nickname', 'created_at'), ('branch_nickname', 'is_active', 'created_at')},
        ),
    ]