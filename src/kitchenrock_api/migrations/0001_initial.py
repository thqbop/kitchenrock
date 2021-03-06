# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-10-02 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import kitchenrock_api.models.user
import kitchenrock_api.models.usertypes


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, max_length=30, verbose_name='middle name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Required. 245 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=254, null=True, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_disabled', models.BooleanField(default=False)),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'abstract': False,
                'db_table': 'auth_user',
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', kitchenrock_api.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Api',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired_at', models.DateTimeField(default='2000-10-10 00:00:00')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField()),
                ('token', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=40)),
                ('type', kitchenrock_api.models.usertypes.PositiveTinyIntegerField(default=0)),
                ('app_id', models.CharField(default='', max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_apis',
            },
        ),
        migrations.CreateModel(
            name='AppKey',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('activated_at', models.DateTimeField(null=True, verbose_name='Actived at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_app_keys',
            },
        ),
        migrations.CreateModel(
            name='AppMeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(default='v0.0.1', max_length=10)),
                ('installed_at', models.DateTimeField(default=None, null=True)),
                ('last_updated', models.DateTimeField(default=None, null=True)),
                ('is_active', kitchenrock_api.models.usertypes.TinyIntegerField(default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_app_meta',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'kitchenrock_cart',
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', kitchenrock_api.models.usertypes.NormalTextField()),
                ('answer', kitchenrock_api.models.usertypes.NormalTextField()),
            ],
            options={
                'db_table': 'kitchenrock_faq',
            },
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
            ],
            options={
                'db_table': 'kitchenrock_category',
            },
        ),
        migrations.CreateModel(
            name='FoodMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'kitchenrock_food_materials',
            },
        ),
        migrations.CreateModel(
            name='FoodNutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'kitchenrock_food_nutritions',
            },
        ),
        migrations.CreateModel(
            name='FoodRecipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=250)),
                ('picture', models.FileField(default='', max_length=200, null=True, upload_to='')),
                ('level', kitchenrock_api.models.usertypes.TinyIntegerField(choices=[(1, 'Easy'), (2, 'Normal'), (3, 'Hard')], default=1)),
                ('prepare_time', models.CharField(default='', max_length=50)),
                ('cook_time', models.CharField(default='', max_length=50)),
                ('method', kitchenrock_api.models.usertypes.NormalTextField()),
                ('lovers', models.IntegerField(default=0)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('serve', models.IntegerField()),
                ('categories', models.ManyToManyField(db_table='kitchenrock_food_category', to='kitchenrock_api.FoodCategory')),
            ],
            options={
                'db_table': 'kitchenrock_foodrecipe',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api_id', models.PositiveIntegerField(default=0)),
                ('user_agent', models.CharField(max_length=256)),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_id', models.CharField(default='', max_length=256)),
                ('time_since_last_login', models.PositiveIntegerField(default=0)),
                ('time_since_last_open_app', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_logins',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'kitchenrock_materials',
            },
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='ten', max_length=100)),
            ],
            options={
                'db_table': 'kitchenrock_nutrition',
            },
        ),
        migrations.CreateModel(
            name='Pathological',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('question', kitchenrock_api.models.usertypes.NormalTextField()),
            ],
            options={
                'db_table': 'kitchenrock_pathological',
            },
        ),
        migrations.CreateModel(
            name='PinCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=40, verbose_name='Pin code')),
                ('is_active', models.BooleanField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_pin',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(default=1)),
                ('content', models.TextField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('foodrecipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.FoodRecipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_review',
            },
        ),
        migrations.CreateModel(
            name='SearchPathological',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_value', models.IntegerField(default=0)),
                ('min_value', models.IntegerField(default=0)),
                ('nutrition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.Nutrition')),
                ('pathological', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.Pathological')),
            ],
            options={
                'db_table': 'kitchenrock_search_pathological',
            },
        ),
        migrations.CreateModel(
            name='UserActivityLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('action', models.CharField(max_length=6, verbose_name='Action')),
                ('status', models.SmallIntegerField(default=200, verbose_name='Request status code')),
                ('url', models.CharField(default='', max_length=2000, verbose_name='Url')),
                ('meta', kitchenrock_api.models.usertypes.NormalTextField(default='{}', verbose_name='Meta data')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('latest_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_type', kitchenrock_api.models.usertypes.TinyIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_user_activity_logs',
                'verbose_name_plural': 'activity_logs',
                'verbose_name': 'activity_log',
            },
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('email', models.CharField(default='', max_length=255, unique=True)),
                ('is_primary', models.BooleanField(default=0)),
                ('token', models.CharField(default='', max_length=40)),
                ('verified_at', models.PositiveIntegerField(default=0)),
                ('created_at', models.PositiveIntegerField(default=1446015876)),
                ('unsubscribe_at', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'kitchenrock_emails',
            },
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pref_id', kitchenrock_api.models.usertypes.PositiveTinyIntegerField(default=0)),
                ('pref_value', models.CharField(default='', max_length=255)),
                ('extra_param', models.CharField(default='', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kitchenrock_users_prefs',
            },
        ),
        migrations.AddField(
            model_name='pathological',
            name='nutrition',
            field=models.ManyToManyField(through='kitchenrock_api.SearchPathological', to='kitchenrock_api.Nutrition'),
        ),
        migrations.AlterUniqueTogether(
            name='material',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='foodrecipe',
            name='materials',
            field=models.ManyToManyField(through='kitchenrock_api.FoodMaterial', to='kitchenrock_api.Material'),
        ),
        migrations.AddField(
            model_name='foodrecipe',
            name='nutritions',
            field=models.ManyToManyField(through='kitchenrock_api.FoodNutrition', to='kitchenrock_api.Nutrition'),
        ),
        migrations.AddField(
            model_name='foodnutrition',
            name='foodrecipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.FoodRecipe'),
        ),
        migrations.AddField(
            model_name='foodnutrition',
            name='nutrition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.Nutrition'),
        ),
        migrations.AddField(
            model_name='foodmaterial',
            name='food_recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.FoodRecipe'),
        ),
        migrations.AddField(
            model_name='foodmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.Material'),
        ),
        migrations.AddField(
            model_name='cart',
            name='foodrecipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.FoodRecipe'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='foodrecipe',
            field=models.ManyToManyField(db_table='kitchenrock_favourite_food', to='kitchenrock_api.FoodRecipe'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='pathological',
            field=models.ManyToManyField(db_table='kitchenrock_pathological_user', to='kitchenrock_api.Pathological'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('foodrecipe', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set([('user', 'foodrecipe', 'create_date')]),
        ),
    ]
