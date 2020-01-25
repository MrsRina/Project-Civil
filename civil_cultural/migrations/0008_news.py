# Generated by Django 2.1.4 on 2019-07-14 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('civil_cultural', '0007_rule_portal_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('votes', models.IntegerField(default=0)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('portal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='civil_cultural.Portal')),
            ],
        ),
    ]