# Generated migration to remove hero_image field from Cohort model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fellowships', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cohort',
            name='hero_image',
        ),
    ]