from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_wpscanapikkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTXAlienVaultAPIKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='LeakCheckAPIKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=500)),
            ],
        ),
    ]
