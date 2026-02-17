from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0004_otxalienvaultapikey_leakcheckapikey'),
        ('targetApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTXThreatData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pulse_count', models.IntegerField(default=0)),
                ('reputation', models.IntegerField(default=0)),
                ('pulses', models.JSONField(blank=True, default=list)),
                ('malware_samples', models.JSONField(blank=True, default=list)),
                ('passive_dns', models.JSONField(blank=True, default=list)),
                ('analyzed_urls', models.JSONField(blank=True, default=list)),
                ('malware_count', models.IntegerField(default=0)),
                ('passive_dns_count', models.IntegerField(default=0)),
                ('url_count', models.IntegerField(default=0)),
                ('whois_data', models.JSONField(blank=True, default=dict)),
                ('fetched_at', models.DateTimeField(auto_now=True)),
                ('fetch_error', models.TextField(blank=True, null=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='targetApp.domain')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.project')),
            ],
            options={
                'unique_together': {('domain', 'project')},
            },
        ),
        migrations.CreateModel(
            name='LeakCheckData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_found', models.IntegerField(default=0)),
                ('leaked_credentials', models.JSONField(blank=True, default=list)),
                ('fetched_at', models.DateTimeField(auto_now=True)),
                ('fetch_error', models.TextField(blank=True, null=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='targetApp.domain')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.project')),
            ],
            options={
                'unique_together': {('domain', 'project')},
            },
        ),
        migrations.CreateModel(
            name='ThreatIntelScanStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_scanning', models.BooleanField(default=False)),
                ('last_scan_at', models.DateTimeField(blank=True, null=True)),
                ('domains_scanned', models.IntegerField(default=0)),
                ('domains_total', models.IntegerField(default=0)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.project')),
            ],
        ),
    ]
