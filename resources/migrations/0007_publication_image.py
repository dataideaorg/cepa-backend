from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0006_alter_blogpost_content_alter_newsarticle_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=resources.models.upload_to_publication_images),
        ),
    ]

