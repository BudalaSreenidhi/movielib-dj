# Generated by Django 5.0.6 on 2024-06-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_list_movie_poster_alter_movie_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='movies',
            field=models.ManyToManyField(to='movies.movie'),
        ),
    ]
