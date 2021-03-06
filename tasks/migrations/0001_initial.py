# Generated by Django 3.1.6 on 2021-07-05 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='general', max_length=40)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True)),
                ('created_date', models.DateField(default='2021-07-05')),
                ('finish_date', models.DateField(default='2021-07-05')),
                ('complete', models.BooleanField(default=False)),
                ('category', models.ForeignKey(default='general', on_delete=django.db.models.deletion.PROTECT, to='tasks.category')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
