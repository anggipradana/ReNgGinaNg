from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0006_add_google_chat_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vulnerabilityreportsetting',
            old_name='show_rengine_banner',
            new_name='show_rengginang_banner',
        ),
    ]
