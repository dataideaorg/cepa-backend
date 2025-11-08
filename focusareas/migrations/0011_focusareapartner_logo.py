# Generated migration for adding logo field to FocusAreaPartner

from django.db import migrations, models
import focusareas.models


class Migration(migrations.Migration):

    dependencies = [
        ('focusareas', '0010_alter_focusareabasicinformation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='focusareapartner',
            name='logo',
            field=models.ImageField(blank=True, help_text='Partner organization logo', null=True, upload_to=focusareas.models.upload_to_partner_logos),
        ),
    ]
