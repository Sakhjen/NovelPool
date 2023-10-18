# Generated by Django 4.2.5 on 2023-09-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novelpoolapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='novel',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='novel',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='novel',
            name='status',
            field=models.IntegerField(verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='page',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='selection',
            name='text',
            field=models.CharField(max_length=500, verbose_name='Ответ'),
        ),
    ]
