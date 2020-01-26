# Generated by Django 2.2.3 on 2020-01-25 23:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_token', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.CharField(max_length=75, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party_mode.Host')),
            ],
        ),
        migrations.CreateModel(
            name='RequestedSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=50)),
                ('song_name', models.CharField(max_length=50)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party_mode.Session')),
            ],
        ),
    ]
