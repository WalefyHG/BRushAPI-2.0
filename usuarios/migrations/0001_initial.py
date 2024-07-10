# Generated by Django 5.0.4 on 2024-07-10 01:24

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('user_email', models.CharField(max_length=50, unique=True)),
                ('user_image', models.ImageField(blank=True, default='', null=True, upload_to='image/')),
                ('user_birthday', models.DateField(blank=True, null=True)),
                ('user_firstName', models.CharField(max_length=50)),
                ('user_lastName', models.CharField(max_length=50)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('user_idioma', models.CharField(max_length=20)),
                ('user_games', models.CharField(max_length=50)),
                ('user_pais', models.CharField(max_length=20)),
                ('user_banner', models.ImageField(blank=True, default='', null=True, upload_to='banner/')),
                ('user_youtube', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user_twitch', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user_instagram', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user_twitter', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('admin', 'Admin'), ('atleta', 'Atleta'), ('team', 'Team')], default='atleta', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_title', models.CharField(max_length=100)),
                ('notice_content', models.TextField()),
                ('notice_date', models.DateTimeField(auto_now_add=True)),
                ('notice_image', models.ImageField(blank=True, null=True, upload_to='newsImage/')),
                ('notice_writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice_writer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_code', models.CharField(max_length=6, unique=True)),
                ('verification_code_expires', models.DateTimeField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
