from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_otxalienvaultapikey_leakcheckapikey'),
        ('threatIntel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leakcheckdata',
            name='checked_credentials',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.CreateModel(
            name='ManualIndicator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('indicator_type', models.CharField(choices=[('domain', 'Domain'), ('subdomain', 'Subdomain'), ('ip', 'IP Address')], max_length=20)),
                ('value', models.CharField(max_length=500)),
                ('otx_data', models.JSONField(blank=True, default=dict)),
                ('pulse_count', models.IntegerField(default=0)),
                ('fetched_at', models.DateTimeField(null=True, blank=True)),
                ('fetch_error', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.project')),
            ],
            options={
                'unique_together': {('project', 'indicator_type', 'value')},
            },
        ),
        migrations.CreateModel(
            name='ThreatIntelReportSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('primary_color', models.CharField(blank=True, default='#1A237E', max_length=10, null=True)),
                ('secondary_color', models.CharField(blank=True, default='#0D1B2A', max_length=10, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_address', models.CharField(blank=True, max_length=200, null=True)),
                ('company_email', models.CharField(blank=True, max_length=100, null=True)),
                ('company_website', models.CharField(blank=True, max_length=100, null=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='report_logos/')),
                ('document_number', models.CharField(blank=True, max_length=100, null=True)),
                ('show_footer', models.BooleanField(default=True)),
                ('footer_text', models.CharField(blank=True, default='CONFIDENTIAL', max_length=200, null=True)),
                ('report_language', models.CharField(blank=True, default='en', max_length=5, null=True)),
                ('classification_label', models.CharField(blank=True, default='CONFIDENTIAL - FOR INTERNAL USE ONLY', max_length=100, null=True)),
                ('banking_keywords', models.TextField(blank=True, default='bank,banking,financial,swift,payment,atm,malware,trojan,phishing,credential,fraud', null=True)),
            ],
        ),
    ]
