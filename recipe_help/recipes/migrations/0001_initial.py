# Generated by Django 4.2.1 on 2023-05-24 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RecipesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('link_video', models.URLField(blank=True, max_length=255)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.categoriesmodel')),
            ],
        ),
    ]
