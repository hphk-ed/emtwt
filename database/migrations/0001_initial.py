# Generated by Django 3.1.1 on 2020-10-27 15:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.TextField(blank=True, default='')),
                ('release_date', models.DateField()),
                ('flo_id', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.TextField(blank=True, default='')),
                ('flo_id', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lyrics', models.TextField(blank=True, default='')),
                ('flo_id', models.IntegerField(blank=True, default=0)),
                ('fake_like', models.IntegerField(default=0)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='database.album')),
                ('artists', models.ManyToManyField(related_name='musics', to='database.Artist')),
                ('featuring_artists', models.ManyToManyField(blank=True, related_name='featuring_musics', to='database.Artist')),
                ('genres', models.ManyToManyField(related_name='musics', to='database.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('score', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('hashtags', models.ManyToManyField(related_name='reviews', to='database.Hashtag')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.music')),
            ],
        ),
        migrations.AddField(
            model_name='music',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='musics', to='database.Tag'),
        ),
    ]
