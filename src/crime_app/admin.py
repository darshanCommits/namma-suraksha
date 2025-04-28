from django.contrib import admin
from .models import (
    Person, PropertyDetail, ChildDetail,
    CriminalCase, CriminalMurderHomicide, CriminalTheft, CriminalAssault, CriminalFraud,
    CriminalCharge, CriminalEvidence,
    CivilCase, CivilContractDispute, CivilPropertyDispute, CivilMoneyRecovery, CivilTortClaim,
    FamilyLawCase, FamilyDivorce, FamilyMaintenance, FamilyChildCustody, FamilyDomesticViolence,
    PropertyLawCase, PropertyTitleDispute, PropertyEvictionSuit, PropertyPartitionSuit,
    ConsumerDisputeCase, ConsumerProductDefect, ConsumerServiceDeficiency, ConsumerUnfairTradePractice,
    LabourDisputeCase, LabourWrongfulTermination, LabourWageDispute, LabourWorkplaceDiscrimination,
    IntellectualPropertyCase, IPPatent, IPTrademark, IPCopyright,
    PublicLawCase, PublicConstitutional, PublicTaxation, PublicEnvironmental
)


# Register basic models
admin.site.register(Person)
admin.site.register(PropertyDetail)
admin.site.register(ChildDetail)

# Register Criminal Case models
class CriminalChargeInline(admin.TabularInline):
    model = CriminalCharge
    extra = 1

class CriminalEvidenceInline(admin.TabularInline):
    model = CriminalEvidence
    extra = 1

@admin.register(CriminalCase)
class CriminalCaseAdmin(admin.ModelAdmin):
    inlines = [CriminalChargeInline, CriminalEvidenceInline]
    list_display = ('fir_number', 'subtype', 'investigation_status', 'chargesheet_filed')
    list_filter = ('subtype', 'investigation_status', 'bail_status')
    search_fields = ('fir_number', 'police_station')

admin.site.register(CriminalMurderHomicide)
admin.site.register(CriminalTheft)
admin.site.register(CriminalAssault)
admin.site.register(CriminalFraud)

# Register Civil Case models
@admin.register(CivilCase)
class CivilCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype', 'claim_amount', 'settlement_attempts')
    list_filter = ('subtype', 'settlement_attempts')
    search_fields = ('relief_sought',)

admin.site.register(CivilContractDispute)
admin.site.register(CivilPropertyDispute)
admin.site.register(CivilMoneyRecovery)
admin.site.register(CivilTortClaim)

# Register Family Law Case models
@admin.register(FamilyLawCase)
class FamilyLawCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype', 'marriage_date', 'children_involved')
    list_filter = ('subtype', 'children_involved')
    search_fields = ('marriage_date',)

admin.site.register(FamilyDivorce)
admin.site.register(FamilyMaintenance)
admin.site.register(FamilyChildCustody)
admin.site.register(FamilyDomesticViolence)

# Register Property Law Case models
@admin.register(PropertyLawCase)
class PropertyLawCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype')
    list_filter = ('subtype',)

admin.site.register(PropertyTitleDispute)
admin.site.register(PropertyEvictionSuit)
admin.site.register(PropertyPartitionSuit)

# Register Consumer Dispute Case models
@admin.register(ConsumerDisputeCase)
class ConsumerDisputeCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype', 'purchase_date', 'compensation_claimed')
    list_filter = ('subtype',)
    search_fields = ('product_service_details',)

admin.site.register(ConsumerProductDefect)
admin.site.register(ConsumerServiceDeficiency)
admin.site.register(ConsumerUnfairTradePractice)

# Register Labour Dispute Case models
@admin.register(LabourDisputeCase)
class LabourDisputeCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype', 'employee', 'employer_details')
    list_filter = ('subtype',)
    search_fields = ('employer_details',)

admin.site.register(LabourWrongfulTermination)
admin.site.register(LabourWageDispute)
admin.site.register(LabourWorkplaceDiscrimination)

# Register Intellectual Property Case models
@admin.register(IntellectualPropertyCase)
class IntellectualPropertyCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype', 'ip_owner_details')
    list_filter = ('subtype',)
    search_fields = ('ip_owner_details',)

admin.site.register(IPPatent)
admin.site.register(IPTrademark)
admin.site.register(IPCopyright)

# Register Public Law Case models
@admin.register(PublicLawCase)
class PublicLawCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtype')
    list_filter = ('subtype',)

admin.site.register(PublicConstitutional)
admin.site.register(PublicTaxation)
admin.site.register(PublicEnvironmental)
