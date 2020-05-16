# Generated by Django 2.2 on 2020-05-15 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0011_feed_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_comment', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='CommentLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('like_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
