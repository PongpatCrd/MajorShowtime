# Generated by Django 2.1 on 2020-02-26 10:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('major_showtime', '0002_auto_20200225_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchesTimeSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branch_nickname', models.CharField(max_length=5)),
                ('first_showtime', models.CharField(max_length=4)),
                ('last_showtime', models.CharField(max_length=4)),
                ('advertisement_time', models.PositiveSmallIntegerField(default=0)),
                ('clean_up_time', models.PositiveSmallIntegerField(default=0)),
                ('break_time', models.PositiveSmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'branches_time_setting',
            },
        ),
        migrations.AlterIndexTogether(
            name='branchestimesetting',
            index_together={('branch_nickname', 'created_at', 'is_active'), ('branch_nickname', 'updated_at', 'is_active'), ('branch_nickname', 'created_at'), ('branch_nickname', 'updated_at'), ('branch_nickname', 'is_active')},
        ),
    ]