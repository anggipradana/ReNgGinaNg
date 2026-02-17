from django.contrib import admin

from threatIntel.models import (
	OTXThreatData,
	LeakCheckData,
	ThreatIntelScanStatus,
	ManualIndicator,
	ThreatIntelReportSetting,
)

admin.site.register(OTXThreatData)
admin.site.register(LeakCheckData)
admin.site.register(ThreatIntelScanStatus)
admin.site.register(ManualIndicator)
admin.site.register(ThreatIntelReportSetting)
