# Generated by Django 3.0.4 on 2020-03-11 09:53

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Static',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.PositiveIntegerField(default=1)),
                ('start', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('final', models.DateTimeField(auto_now=True)),
                ('alias', models.CharField(max_length=256)),
                ('title_tag', models.TextField(default='')),
                ('keywords', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('template', models.TextField(default='')),
                ('title', models.TextField(verbose_name='Название')),
                ('icon', models.ImageField(blank=True, default='', max_length=500, upload_to='uploads', verbose_name='Картинка')),
                ('short', models.TextField(blank=True, default='', verbose_name='Анонс')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Подробнее')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'db_table': 'static',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StaticCategories',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('usestart', models.PositiveIntegerField()),
                ('usefinal', models.PositiveIntegerField()),
                ('parent', models.PositiveSmallIntegerField()),
                ('type', models.PositiveIntegerField()),
                ('usepic', models.IntegerField()),
                ('picwidth', models.SmallIntegerField()),
                ('picheight', models.SmallIntegerField()),
                ('matlimit', models.PositiveIntegerField()),
                ('ordering', models.PositiveIntegerField()),
                ('main_material', models.PositiveIntegerField()),
                ('alias', models.CharField(max_length=256)),
                ('name', models.TextField()),
                ('keywords', models.TextField()),
                ('description', models.TextField()),
                ('my_template', models.TextField()),
                ('template', models.TextField()),
            ],
            options={
                'db_table': 'static_categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StaticContentAttachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Вложения')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appl.Static')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
                'db_table': 'static_content_attachments',
            },
        ),
    ]