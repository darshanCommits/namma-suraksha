from django.db import models
from datetime import datetime, date
import json
from mixer.backend.django import mixer
from enum import Enum
import random
from typing import List

# Common Enums
class AppealStage(models.TextChoices):
    FIRST_APPEAL = "FirstAppeal", "First Appeal"
    TRIBUNAL = "Tribunal", "Tribunal"
    HIGH_COURT = "HighCourt", "High Court"
    SUPREME_COURT = "SupremeCourt", "Supreme Court"

class ViolenceType(models.TextChoices):
    PHYSICAL = "Physical", "Physical"
    EMOTIONAL = "Emotional", "Emotional"
    SEXUAL = "Sexual", "Sexual"
    FINANCIAL = "Financial", "Financial"
    VERBAL = "Verbal", "Verbal"
    OTHER = "Other", "Other"

# Main Case Type Enum
class CaseTypeEnum(models.TextChoices):
    CRIMINAL = "Criminal", "Criminal"
    CIVIL = "Civil", "Civil"
    FAMILY_LAW = "FamilyLaw", "Family Law"
    PROPERTY_LAW = "PropertyLaw", "Property Law"
    CONSUMER_DISPUTE = "ConsumerDispute", "Consumer Dispute"
    LABOUR_DISPUTE = "LabourDispute", "Labour Dispute"
    INTELLECTUAL_PROPERTY = "IntellectualProperty", "Intellectual Property"
    PUBLIC_LAW = "PublicLaw", "Public Law"

# Person model
class Person(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

# Property Detail model
class PropertyDetail(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.address or "Unnamed Property"

# Child Detail model
class ChildDetail(models.Model):
    age = models.IntegerField()

    def __str__(self):
        return f"Child (Age: {self.age})"

# Base Case model
class Case(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    case_type = models.CharField(
        max_length=30,
        choices=CaseTypeEnum.choices,
    )
    
    class Meta:
        abstract = True

# Criminal Case Models
class CriminalCaseSubtype(models.TextChoices):
    MURDER_HOMICIDE = "MurderHomicide", "Murder/Homicide"
    THEFT = "Theft", "Theft"
    ASSAULT = "Assault", "Assault"
    FRAUD = "Fraud", "Fraud"
    OTHER = "Other", "Other"

class BailStatus(models.TextChoices):
    NOT_APPLIED = "NotApplied", "Not Applied"
    APPLIED = "Applied", "Applied"
    GRANTED = "Granted", "Granted"
    REJECTED = "Rejected", "Rejected"

class InvestigationStatus(models.TextChoices):
    ONGOING = "Ongoing", "Ongoing"
    COMPLETED = "Completed", "Completed"
    CLOSED = "Closed", "Closed"

class CriminalMurderHomicide(models.Model):
    victim = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="murder_victim")
    weapon_used = models.CharField(max_length=100, null=True, blank=True)

class CriminalTheft(models.Model):
    property_type = models.CharField(max_length=100, null=True, blank=True)
    estimated_value = models.FloatField(null=True, blank=True)

class CriminalAssault(models.Model):
    injury_severity = models.CharField(max_length=100, null=True, blank=True)
    weapon_used = models.CharField(max_length=100, null=True, blank=True)

class CriminalFraud(models.Model):
    amount_involved = models.FloatField(null=True, blank=True)
    fraud_type = models.CharField(max_length=100, null=True, blank=True)

class CriminalCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=CriminalCaseSubtype.choices,
    )
    fir_number = models.CharField(max_length=20)
    police_station = models.CharField(max_length=100, null=True, blank=True)
    arrest_date = models.DateField(null=True, blank=True)
    bail_status = models.CharField(
        max_length=20,
        choices=BailStatus.choices,
        null=True,
        blank=True
    )
    investigation_status = models.CharField(
        max_length=20,
        choices=InvestigationStatus.choices,
    )
    chargesheet_filed = models.BooleanField(default=False)
    chargesheet_date = models.DateField(null=True, blank=True)
    witness_count = models.IntegerField(default=0)
    
    # Foreign key relationships to subtype-specific details
    murder_homicide = models.OneToOneField(
        CriminalMurderHomicide, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    theft = models.OneToOneField(
        CriminalTheft, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    assault = models.OneToOneField(
        CriminalAssault, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    fraud = models.OneToOneField(
        CriminalFraud, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

class CriminalCharge(models.Model):
    case = models.ForeignKey(CriminalCase, on_delete=models.CASCADE, related_name="charges")
    charge_name = models.CharField(max_length=100)

class CriminalEvidence(models.Model):
    case = models.ForeignKey(CriminalCase, on_delete=models.CASCADE, related_name="evidence_types")
    evidence_type = models.CharField(max_length=100)

# Civil Case Models
class CivilCaseSubtype(models.TextChoices):
    CONTRACT_DISPUTE = "ContractDispute", "Contract Dispute"
    PROPERTY_DISPUTE = "PropertyDispute", "Property Dispute"
    MONEY_RECOVERY = "MoneyRecovery", "Money Recovery"
    TORT_CLAIM = "TortClaim", "Tort Claim"
    OTHER = "Other", "Other"

class CivilContractDispute(models.Model):
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    breach_details = models.TextField(null=True, blank=True)

class CivilPropertyDispute(models.Model):
    def __str__(self):
        return f"Property Dispute ({self.id})"

class CivilPropertyDisputeDetail(models.Model):
    dispute = models.ForeignKey(CivilPropertyDispute, on_delete=models.CASCADE, related_name="properties")
    property_detail = models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)

class CivilMoneyRecovery(models.Model):
    principal_amount = models.FloatField(null=True, blank=True)
    debt_documentation = models.CharField(max_length=255, null=True, blank=True)

class CivilTortClaim(models.Model):
    tort_type = models.CharField(max_length=100, null=True, blank=True)
    damages_claimed = models.FloatField(null=True, blank=True)

class CivilCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=CivilCaseSubtype.choices,
    )
    relief_sought = models.TextField()
    claim_amount = models.FloatField(null=True, blank=True)
    settlement_attempts = models.BooleanField(default=False)
    
    # Foreign key relationships to subtype-specific details
    contract_dispute = models.OneToOneField(
        CivilContractDispute, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    property_dispute = models.OneToOneField(
        CivilPropertyDispute, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    money_recovery = models.OneToOneField(
        CivilMoneyRecovery, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    tort_claim = models.OneToOneField(
        CivilTortClaim, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

# Family Law Case Models
class FamilyLawSubtype(models.TextChoices):
    DIVORCE = "Divorce", "Divorce"
    MAINTENANCE = "Maintenance", "Maintenance"
    CHILD_CUSTODY = "ChildCustody", "Child Custody"
    DOMESTIC_VIOLENCE = "DomesticViolence", "Domestic Violence"
    OTHER = "Other", "Other"

class FamilyDivorce(models.Model):
    divorce_type = models.CharField(max_length=100, null=True, blank=True)

class FamilyDivorceGround(models.Model):
    divorce = models.ForeignKey(FamilyDivorce, on_delete=models.CASCADE, related_name="grounds")
    ground = models.CharField(max_length=100)

class FamilyMaintenance(models.Model):
    maintenance_for = models.CharField(max_length=100, null=True, blank=True)
    amount_claimed = models.FloatField(null=True, blank=True)

class FamilyChildCustody(models.Model):
    visitation_rights_proposed = models.TextField(null=True, blank=True)

class FamilyChildCustodyDetail(models.Model):
    custody = models.ForeignKey(FamilyChildCustody, on_delete=models.CASCADE, related_name="children")
    child_detail = models.ForeignKey(ChildDetail, on_delete=models.CASCADE)

class FamilyDomesticViolence(models.Model):
    protection_order_sought = models.BooleanField(default=False)

class FamilyDomesticViolenceType(models.Model):
    domestic_violence = models.ForeignKey(FamilyDomesticViolence, on_delete=models.CASCADE, related_name="violence_types")
    violence_type = models.CharField(
        max_length=20, 
        choices=ViolenceType.choices
    )

class FamilyLawCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=FamilyLawSubtype.choices,
    )
    marriage_date = models.DateField(null=True, blank=True)
    children_involved = models.BooleanField(default=False)
    
    # Foreign key relationships to subtype-specific details
    divorce = models.OneToOneField(
        FamilyDivorce, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    maintenance = models.OneToOneField(
        FamilyMaintenance, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    child_custody = models.OneToOneField(
        FamilyChildCustody, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    domestic_violence = models.OneToOneField(
        FamilyDomesticViolence, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

# Property Law Case Models
class PropertyLawSubtype(models.TextChoices):
    TITLE_DISPUTE = "TitleDispute", "Title Dispute"
    EVICTION_SUIT = "EvictionSuit", "Eviction Suit"
    PARTITION_SUIT = "PartitionSuit", "Partition Suit"
    OTHER = "Other", "Other"

class PropertyTitleDispute(models.Model):
    claim_basis = models.CharField(max_length=100, null=True, blank=True)
    possession_status = models.CharField(max_length=100, null=True, blank=True)

class PropertyEvictionSuit(models.Model):
    eviction_grounds = models.CharField(max_length=100, null=True, blank=True)
    arrears_amount = models.FloatField(null=True, blank=True)

class PropertyPartitionSuit(models.Model):
    share_claimed = models.CharField(max_length=100, null=True, blank=True)

class PropertyPartitionCoOwner(models.Model):
    partition_suit = models.ForeignKey(PropertyPartitionSuit, on_delete=models.CASCADE, related_name="co_owners")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class PropertyLawCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=PropertyLawSubtype.choices,
    )
    
    # Foreign key relationships to subtype-specific details
    title_dispute = models.OneToOneField(
        PropertyTitleDispute, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    eviction_suit = models.OneToOneField(
        PropertyEvictionSuit, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    partition_suit = models.OneToOneField(
        PropertyPartitionSuit, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

class PropertyLawCaseProperty(models.Model):
    case = models.ForeignKey(PropertyLawCase, on_delete=models.CASCADE, related_name="properties")
    property_detail = models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)

# Consumer Dispute Case Models
class ConsumerDisputeSubtype(models.TextChoices):
    PRODUCT_DEFECT = "ProductDefect", "Product Defect"
    SERVICE_DEFICIENCY = "ServiceDeficiency", "Service Deficiency"
    UNFAIR_TRADE_PRACTICE = "UnfairTradePractice", "Unfair Trade Practice"
    OTHER = "Other", "Other"

class ConsumerProductDefect(models.Model):
    product_type = models.CharField(max_length=100, null=True, blank=True)
    defect_nature = models.CharField(max_length=100, null=True, blank=True)

class ConsumerServiceDeficiency(models.Model):
    service_type = models.CharField(max_length=100, null=True, blank=True)
    deficiency_nature = models.CharField(max_length=100, null=True, blank=True)

class ConsumerUnfairTradePractice(models.Model):
    practice_type = models.CharField(max_length=100, null=True, blank=True)
    misleading_aspect = models.CharField(max_length=100, null=True, blank=True)

class ConsumerDisputeCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=ConsumerDisputeSubtype.choices,
    )
    product_service_details = models.TextField()
    purchase_date = models.DateField(null=True, blank=True)
    compensation_claimed = models.FloatField(null=True, blank=True)
    
    # Foreign key relationships to subtype-specific details
    product_defect = models.OneToOneField(
        ConsumerProductDefect, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    service_deficiency = models.OneToOneField(
        ConsumerServiceDeficiency, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    unfair_trade_practice = models.OneToOneField(
        ConsumerUnfairTradePractice, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

# Labour Dispute Case Models
class LabourDisputeSubtype(models.TextChoices):
    WRONGFUL_TERMINATION = "WrongfulTermination", "Wrongful Termination"
    WAGE_DISPUTE = "WageDispute", "Wage Dispute"
    WORKPLACE_DISCRIMINATION = "WorkplaceDiscrimination", "Workplace Discrimination"
    OTHER = "Other", "Other"

class LabourWrongfulTermination(models.Model):
    termination_date = models.DateField(null=True, blank=True)
    termination_reason_stated = models.CharField(max_length=255, null=True, blank=True)

class LabourWageDispute(models.Model):
    disputed_amount = models.FloatField(null=True, blank=True)
    wage_dispute_type = models.CharField(max_length=100, null=True, blank=True)

class LabourWorkplaceDiscrimination(models.Model):
    incident_details = models.TextField(null=True, blank=True)

class LabourDiscriminationGround(models.Model):
    discrimination = models.ForeignKey(LabourWorkplaceDiscrimination, on_delete=models.CASCADE, related_name="grounds")
    ground = models.CharField(max_length=100)

class LabourDisputeCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=LabourDisputeSubtype.choices,
    )
    employee = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name="labour_cases_as_employee")
    employer_details = models.CharField(max_length=255, null=True, blank=True)
    employment_start_date = models.DateField(null=True, blank=True)
    
    # Foreign key relationships to subtype-specific details
    wrongful_termination = models.OneToOneField(
        LabourWrongfulTermination, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    wage_dispute = models.OneToOneField(
        LabourWageDispute, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    workplace_discrimination = models.OneToOneField(
        LabourWorkplaceDiscrimination, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

# Intellectual Property Case Models
class IPCaseSubtype(models.TextChoices):
    PATENT = "Patent", "Patent"
    TRADEMARK = "Trademark", "Trademark"
    COPYRIGHT = "Copyright", "Copyright"
    OTHER = "Other", "Other"

class IPPatent(models.Model):
    invention_details = models.TextField(null=True, blank=True)
    dispute_type = models.CharField(max_length=100, null=True, blank=True)

class IPTrademark(models.Model):
    trademark_description = models.TextField(null=True, blank=True)
    dispute_type = models.CharField(max_length=100, null=True, blank=True)

class IPCopyright(models.Model):
    work_type = models.CharField(max_length=100, null=True, blank=True)
    infringing_work_details = models.TextField(null=True, blank=True)

class IntellectualPropertyCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=IPCaseSubtype.choices,
    )
    ip_owner_details = models.CharField(max_length=255, null=True, blank=True)
    
    # Foreign key relationships to subtype-specific details
    patent = models.OneToOneField(
        IPPatent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    trademark = models.OneToOneField(
        IPTrademark, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    copyright = models.OneToOneField(
        IPCopyright, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)

# Public Law Case Models
class PublicLawSubtype(models.TextChoices):
    CONSTITUTIONAL = "Constitutional", "Constitutional"
    TAXATION = "Taxation", "Taxation"
    ENVIRONMENTAL = "Environmental", "Environmental"
    OTHER = "Other", "Other"

class PublicConstitutional(models.Model):
    government_action_challenged = models.TextField(null=True, blank=True)

class PublicConstitutionalRight(models.Model):
    constitutional = models.ForeignKey(PublicConstitutional, on_delete=models.CASCADE, related_name="fundamental_rights")
    right = models.CharField(max_length=100)

class PublicTaxation(models.Model):
    assessment_year = models.CharField(max_length=20, null=True, blank=True)
    disputed_amount = models.FloatField(null=True, blank=True)
    tax_authority = models.CharField(max_length=100, null=True, blank=True)
    appeal_stage = models.CharField(
        max_length=20,
        choices=AppealStage.choices,
        null=True,
        blank=True
    )

class PublicEnvironmental(models.Model):
    pollution_type = models.CharField(max_length=100, null=True, blank=True)
    regulatory_authority = models.CharField(max_length=100, null=True, blank=True)
    penalty_imposed = models.FloatField(null=True, blank=True)

class PublicLawCase(Case):
    subtype = models.CharField(
        max_length=30,
        choices=PublicLawSubtype.choices,
    )
    
    # Foreign key relationships to subtype-specific details
    constitutional = models.OneToOneField(
        PublicConstitutional, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    taxation = models.OneToOneField(
        PublicTaxation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    environmental = models.OneToOneField(
        PublicEnvironmental, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    other_details = models.TextField(null=True, blank=True)
