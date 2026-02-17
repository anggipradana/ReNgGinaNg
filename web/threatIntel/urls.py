from django.urls import path

from threatIntel import views

urlpatterns = [
	path(
		'<slug:slug>/threat-intel/',
		views.index,
		name='threat_intel_index'),
	path(
		'<slug:slug>/threat-intel/refresh_all',
		views.refresh_all,
		name='threat_intel_refresh_all'),
	path(
		'<slug:slug>/threat-intel/refresh_domain/<int:id>',
		views.refresh_domain,
		name='threat_intel_refresh_domain'),
	path(
		'<slug:slug>/threat-intel/scan_status',
		views.scan_status,
		name='threat_intel_scan_status'),
	path(
		'<slug:slug>/threat-intel/domain_detail/<int:id>',
		views.domain_detail,
		name='threat_intel_domain_detail'),
	path(
		'<slug:slug>/threat-intel/toggle_checked/<int:id>',
		views.toggle_checked_credential,
		name='threat_intel_toggle_checked'),
	path(
		'<slug:slug>/threat-intel/add_indicator',
		views.add_indicator,
		name='threat_intel_add_indicator'),
	path(
		'<slug:slug>/threat-intel/delete_indicator/<int:id>',
		views.delete_indicator,
		name='threat_intel_delete_indicator'),
	path(
		'<slug:slug>/threat-intel/refresh_indicator/<int:id>',
		views.refresh_indicator,
		name='threat_intel_refresh_indicator'),
	path(
		'<slug:slug>/threat-intel/indicator_detail/<int:id>',
		views.indicator_detail,
		name='threat_intel_indicator_detail'),
	path(
		'<slug:slug>/threat-intel/generate_report',
		views.generate_threat_report,
		name='threat_intel_generate_report'),
	path(
		'<slug:slug>/threat-intel/report_settings',
		views.threat_report_settings,
		name='threat_report_settings'),
]
