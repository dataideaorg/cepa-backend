import resources.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_publication_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.CharField(default=resources.models.generate_uuid, max_length=255, primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=255)),
                ('author_email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='resources.blogpost')),
            ],
            options={
                'verbose_name': 'Blog Comment',
                'verbose_name_plural': 'Blog Comments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.CharField(default=resources.models.generate_uuid, max_length=255, primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=255)),
                ('author_email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='resources.newsarticle')),
            ],
            options={
                'verbose_name': 'News Comment',
                'verbose_name_plural': 'News Comments',
                'ordering': ['-created_at'],
            },
        ),
    ]
