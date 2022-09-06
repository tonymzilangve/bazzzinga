# Generated by Django 4.0.4 on 2022-06-13 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0002_alter_amigos_options_alter_friendrequest_options'),
        ('social', '0006_alter_profile_amigos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='amigos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amigos', to='friend.amigos', verbose_name='Друзья'),
        ),
    ]