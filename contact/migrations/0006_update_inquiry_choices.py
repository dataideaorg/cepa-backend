# Generated manually for inquiry choices cleanup

from django.db import migrations


def update_inquiry_types(apps, schema_editor):
    """
    Update existing records with old inquiry types to 'general'
    """
    Contact = apps.get_model('contact', 'Contact')
    
    # Map old inquiry types to 'general'
    old_types = ['training', 'consultancy', 'partnership', 'other']
    
    for old_type in old_types:
        Contact.objects.filter(inquiry_type=old_type).update(inquiry_type='general')


def reverse_update_inquiry_types(apps, schema_editor):
    """
    Reverse migration - this is not easily reversible
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_alter_contact_id_alter_newsletter_id'),
    ]

    operations = [
        # Update existing records with old inquiry types to 'general'
        migrations.RunPython(
            code=update_inquiry_types,
            reverse_code=reverse_update_inquiry_types,
        ),
    ]
