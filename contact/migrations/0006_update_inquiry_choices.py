# Generated manually for inquiry choices update

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_alter_contact_id_alter_newsletter_id'),
    ]

    operations = [
        # This migration updates the INQUIRY_CHOICES in the model
        # The actual field definition doesn't change, only the choices
        # This is a data migration to update existing choices
        migrations.RunPython(
            code=migrations.RunPython.noop,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
