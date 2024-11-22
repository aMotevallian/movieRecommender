# Generated by Django 5.1.1 on 2024-10-21 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_movietfidf'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieSimilarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity_score', models.FloatField()),
                ('movie_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similarities_from', to='base.movie')),
                ('movie_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similarities_to', to='base.movie')),
            ],
        ),
    ]
