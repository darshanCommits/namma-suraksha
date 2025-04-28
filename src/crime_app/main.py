# Import settings for Django standalone script
import os
import django
from datetime import datetime
import random
import json
from mixer.backend.django import mixer
from django.db import transaction

# Import our models
from .models import (
    Person, PropertyDetail, ChildDetail, 
    CriminalCase, CriminalCaseSubtype, BailStatus, InvestigationStatus,
    CriminalMurderHomicide, CriminalTheft, CriminalAssault, CriminalFraud,
    CriminalCharge, CriminalEvidence,
    CivilCase, CivilCaseSubtype, CivilContractDispute, CivilPropertyDispute,
    CivilMoneyRecovery, CivilTortClaim, CivilPropertyDisputeDetail,
    FamilyLawCase, FamilyLawSubtype, FamilyDivorce, FamilyDivorceGround,
    FamilyMaintenance, FamilyChildCustody, FamilyChildCustodyDetail,
    FamilyDomesticViolence, FamilyDomesticViolenceType, ViolenceType,
    PropertyLawCase, PropertyLawSubtype, PropertyTitleDispute, PropertyEvictionSuit,
    PropertyPartitionSuit, PropertyPartitionCoOwner, PropertyLawCaseProperty,
    ConsumerDisputeCase, ConsumerDisputeSubtype, ConsumerProductDefect,
    ConsumerServiceDeficiency, ConsumerUnfairTradePractice,
    LabourDisputeCase, LabourDisputeSubtype, LabourWrongfulTermination,
    LabourWageDispute, LabourWorkplaceDiscrimination, LabourDiscriminationGround,
    IntellectualPropertyCase, IPCaseSubtype, IPPatent, IPTrademark, IPCopyright,
    PublicLawCase, PublicLawSubtype, PublicConstitutional, PublicConstitutionalRight,
    PublicTaxation, PublicEnvironmental, AppealStage,
    CaseTypeEnum
)


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crime-django.settings')
django.setup()


# Custom generator functions
def generate_fir_number():
    return f"FIR-{random.randint(1000, 9999)}/{datetime.now().year}"

def generate_random_charges(case):
    charges_list = ["Theft", "Assault", "Fraud", "Property Damage", "Disorderly Conduct"]
    for _ in range(random.randint(1, 3)):
        charge = random.choice(charges_list)
        CriminalCharge.objects.create(case=case, charge_name=charge)

def generate_random_evidence_types(case):
    evidence_list = ["Documentary", "Physical", "Digital", "Testimonial"]
    for _ in range(random.randint(1, 3)):
        evidence = random.choice(evidence_list)
        CriminalEvidence.objects.create(case=case, evidence_type=evidence)

def generate_random_property_details(dispute):
    for _ in range(random.randint(1, 3)):
        property_detail = mixer.blend(PropertyDetail)
        CivilPropertyDisputeDetail.objects.create(
            dispute=dispute,
            property_detail=property_detail
        )

def generate_random_child_details(custody):
    for _ in range(random.randint(1, 4)):
        child_detail = mixer.blend(ChildDetail)
        FamilyChildCustodyDetail.objects.create(
            custody=custody,
            child_detail=child_detail
        )

def generate_random_co_owners(partition_suit):
    for _ in range(random.randint(2, 5)):
        person = mixer.blend(Person)
        PropertyPartitionCoOwner.objects.create(
            partition_suit=partition_suit,
            person=person
        )

def generate_random_violence_types(domestic_violence):
    violence_types = list(ViolenceType.choices)
    for _ in range(random.randint(1, 3)):
        violence_type_choice = random.choice(violence_types)
        FamilyDomesticViolenceType.objects.create(
            domestic_violence=domestic_violence,
            violence_type=violence_type_choice[0]
        )

def generate_random_discrimination_grounds(discrimination):
    grounds = ["Gender", "Caste", "Religion", "Disability"]
    for _ in range(random.randint(1, 2)):
        ground = random.choice(grounds)
        LabourDiscriminationGround.objects.create(
            discrimination=discrimination,
            ground=ground
        )

def generate_random_fundamental_rights(constitutional):
    rights = ["Equality", "Freedom of Speech", "Life and Liberty"]
    for _ in range(random.randint(1, 2)):
        right = random.choice(rights)
        PublicConstitutionalRight.objects.create(
            constitutional=constitutional,
            right=right
        )

def generate_random_divorce_grounds(divorce):
    grounds = ["Cruelty", "Desertion", "Adultery", "Mutual Consent"]
    for _ in range(random.randint(1, 2)):
        ground = random.choice(grounds)
        FamilyDivorceGround.objects.create(
            divorce=divorce,
            ground=ground
        )

def generate_property_for_case(case):
    for _ in range(random.randint(1, 3)):
        property_detail = mixer.blend(PropertyDetail)
        PropertyLawCaseProperty.objects.create(
            case=case,
            property_detail=property_detail
        )

# Function to generate a criminal case
@transaction.atomic
def generate_criminal_case():
    subtype = random.choice(list(CriminalCaseSubtype.choices))[0]
    
    # Create base criminal case
    case = mixer.blend(
        CriminalCase,
        case_type=CaseTypeEnum.CRIMINAL,
        subtype=subtype,
        fir_number=generate_fir_number(),
        investigation_status=random.choice(list(InvestigationStatus.choices))[0],
        bail_status=random.choice(list(BailStatus.choices))[0]
    )
    
    # Generate charges and evidence
    generate_random_charges(case)
    generate_random_evidence_types(case)
    
    # Create subtype-specific details
    if subtype == CriminalCaseSubtype.MURDER_HOMICIDE:
        victim = mixer.blend(Person)
        murder_homicide = mixer.blend(CriminalMurderHomicide, victim=victim)
        case.murder_homicide = murder_homicide
    elif subtype == CriminalCaseSubtype.THEFT:
        case.theft = mixer.blend(CriminalTheft)
    elif subtype == CriminalCaseSubtype.ASSAULT:
        case.assault = mixer.blend(CriminalAssault)
    elif subtype == CriminalCaseSubtype.FRAUD:
        case.fraud = mixer.blend(CriminalFraud)
    
    case.save()
    return case

# Function to generate a civil case
@transaction.atomic
def generate_civil_case():
    subtype = random.choice(list(CivilCaseSubtype.choices))[0]
    
    # Create base civil case
    case = mixer.blend(
        CivilCase,
        case_type=CaseTypeEnum.CIVIL,
        subtype=subtype,
        relief_sought=mixer.faker.sentence(),
        claim_amount=round(random.uniform(10000, 1000000), 2) if random.choice([True, False]) else None,
        settlement_attempts=random.choice([True, False])
    )
    
    # Create subtype-specific details
    if subtype == CivilCaseSubtype.CONTRACT_DISPUTE:
        case.contract_dispute = mixer.blend(CivilContractDispute)
    elif subtype == CivilCaseSubtype.PROPERTY_DISPUTE:
        property_dispute = mixer.blend(CivilPropertyDispute)
        generate_random_property_details(property_dispute)
        case.property_dispute = property_dispute
    elif subtype == CivilCaseSubtype.MONEY_RECOVERY:
        case.money_recovery = mixer.blend(CivilMoneyRecovery)
    elif subtype == CivilCaseSubtype.TORT_CLAIM:
        case.tort_claim = mixer.blend(CivilTortClaim)
    
    case.save()
    return case

# Function to generate a family law case
@transaction.atomic
def generate_family_law_case():
    subtype = random.choice(list(FamilyLawSubtype.choices))[0]
    
    # Create base family law case
    case = mixer.blend(
        FamilyLawCase,
        case_type=CaseTypeEnum.FAMILY_LAW,
        subtype=subtype,
        marriage_date=mixer.faker.date_between(start_date='-30y', end_date='-1y') if random.choice([True, False]) else None,
        children_involved=random.choice([True, False])
    )
    
    # Create subtype-specific details
    if subtype == FamilyLawSubtype.DIVORCE:
        divorce = mixer.blend(FamilyDivorce)
        generate_random_divorce_grounds(divorce)
        case.divorce = divorce
    elif subtype == FamilyLawSubtype.MAINTENANCE:
        case.maintenance = mixer.blend(FamilyMaintenance)
    elif subtype == FamilyLawSubtype.CHILD_CUSTODY:
        child_custody = mixer.blend(FamilyChildCustody)
        generate_random_child_details(child_custody)
        case.child_custody = child_custody
    elif subtype == FamilyLawSubtype.DOMESTIC_VIOLENCE:
        domestic_violence = mixer.blend(FamilyDomesticViolence)
        generate_random_violence_types(domestic_violence)
        case.domestic_violence = domestic_violence
    
    case.save()
    return case

# Function to generate a property law case
@transaction.atomic
def generate_property_law_case():
    subtype = random.choice(list(PropertyLawSubtype.choices))[0]
    
    # Create base property law case
    case = mixer.blend(
        PropertyLawCase,
        case_type=CaseTypeEnum.PROPERTY_LAW,
        subtype=subtype,
    )
    
    # Generate property details
    generate_property_for_case(case)
    
    # Create subtype-specific details
    if subtype == PropertyLawSubtype.TITLE_DISPUTE:
        case.title_dispute = mixer.blend(PropertyTitleDispute)
    elif subtype == PropertyLawSubtype.EVICTION_SUIT:
        case.eviction_suit = mixer.blend(PropertyEvictionSuit)
    elif subtype == PropertyLawSubtype.PARTITION_SUIT:
        partition_suit = mixer.blend(PropertyPartitionSuit)
        generate_random_co_owners(partition_suit)
        case.partition_suit = partition_suit
    
    case.save()
    return case

# Function to generate a consumer dispute case
@transaction.atomic
def generate_consumer_dispute_case():
    subtype = random.choice(list(ConsumerDisputeSubtype.choices))[0]
    
    # Create base consumer dispute case
    case = mixer.blend(
        ConsumerDisputeCase,
        case_type=CaseTypeEnum.CONSUMER_DISPUTE,
        subtype=subtype,
        product_service_details=mixer.faker.sentence(),
        purchase_date=mixer.faker.date_between(start_date='-5y', end_date='today') if random.choice([True, False]) else None,
        compensation_claimed=round(random.uniform(1000, 500000), 2) if random.choice([True, False]) else None
    )
    
    # Create subtype-specific details
    if subtype == ConsumerDisputeSubtype.PRODUCT_DEFECT:
        case.product_defect = mixer.blend(ConsumerProductDefect)
    elif subtype == ConsumerDisputeSubtype.SERVICE_DEFICIENCY:
        case.service_deficiency = mixer.blend(ConsumerServiceDeficiency)
    elif subtype == ConsumerDisputeSubtype.UNFAIR_TRADE_PRACTICE:
        case.unfair_trade_practice = mixer.blend(ConsumerUnfairTradePractice)
    
    case.save()
    return case

# Function to generate a labour dispute case
@transaction.atomic
def generate_labour_dispute_case():
    subtype = random.choice(list(LabourDisputeSubtype.choices))[0]
    
    # Create base labour dispute case
    employee = mixer.blend(Person)
    case = mixer.blend(
        LabourDisputeCase,
        case_type=CaseTypeEnum.LABOUR_DISPUTE,
        subtype=subtype,
        employee=employee,
        employer_details=mixer.faker.company(),
        employment_start_date=mixer.faker.date_between(start_date='-20y', end_date='-1m') if random.choice([True, False]) else None
    )
    
    # Create subtype-specific details
    if subtype == LabourDisputeSubtype.WRONGFUL_TERMINATION:
        case.wrongful_termination = mixer.blend(LabourWrongfulTermination)
    elif subtype == LabourDisputeSubtype.WAGE_DISPUTE:
        case.wage_dispute = mixer.blend(LabourWageDispute)
    elif subtype == LabourDisputeSubtype.WORKPLACE_DISCRIMINATION:
        workplace_discrimination = mixer.blend(LabourWorkplaceDiscrimination)
        generate_random_discrimination_grounds(workplace_discrimination)
        case.workplace_discrimination = workplace_discrimination
    
    case.save()
    return case

# Function to generate an intellectual property case
@transaction.atomic
def generate_intellectual_property_case():
    subtype = random.choice(list(IPCaseSubtype.choices))[0]
    
    # Create base IP case
    case = mixer.blend(
        IntellectualPropertyCase,
        case_type=CaseTypeEnum.INTELLECTUAL_PROPERTY,
        subtype=subtype,
        ip_owner_details=mixer.faker.company() if random.choice([True, False]) else None
    )
    
    # Create subtype-specific details
    if subtype == IPCaseSubtype.PATENT:
        case.patent = mixer.blend(IPPatent)
    elif subtype == IPCaseSubtype.TRADEMARK:
        case.trademark = mixer.blend(IPTrademark)
    elif subtype == IPCaseSubtype.COPYRIGHT:
        case.copyright = mixer.blend(IPCopyright)
    
    case.save()
    return case

# Function to generate a public law case
@transaction.atomic
def generate_public_law_case():
    subtype = random.choice(list(PublicLawSubtype.choices))[0]
    
    # Create base public law case
    case = mixer.blend(
        PublicLawCase,
        case_type=CaseTypeEnum.PUBLIC_LAW,
        subtype=subtype,
    )
    
    # Create subtype-specific details
    if subtype == PublicLawSubtype.CONSTITUTIONAL:
        constitutional = mixer.blend(PublicConstitutional)
        generate_random_fundamental_rights(constitutional)
        case.constitutional = constitutional
    elif subtype == PublicLawSubtype.TAXATION:
        case.taxation = mixer.blend(
            PublicTaxation, 
            appeal_stage=random.choice(list(AppealStage.choices))[0]
        )
    elif subtype == PublicLawSubtype.ENVIRONMENTAL:
        case.environmental = mixer.blend(PublicEnvironmental)
    
    case.save()
    return case

# Function to generate a case based on the top-level enum
def generate_legal_case():
    case_type_enum = random.choice(list(CaseTypeEnum.choices))[0]

    if case_type_enum == CaseTypeEnum.CRIMINAL:
        return generate_criminal_case()
    elif case_type_enum == CaseTypeEnum.CIVIL:
        return generate_civil_case()
    elif case_type_enum == CaseTypeEnum.FAMILY_LAW:
        return generate_family_law_case()
    elif case_type_enum == CaseTypeEnum.PROPERTY_LAW:
        return generate_property_law_case()
    elif case_type_enum == CaseTypeEnum.CONSUMER_DISPUTE:
        return generate_consumer_dispute_case()
    elif case_type_enum == CaseTypeEnum.LABOUR_DISPUTE:
        return generate_labour_dispute_case()
    elif case_type_enum == CaseTypeEnum.INTELLECTUAL_PROPERTY:
        return generate_intellectual_property_case()
    elif case_type_enum == CaseTypeEnum.PUBLIC_LAW:
        return generate_public_law_case()

# Create a test dataset
def create_test_dataset(num_cases=10):
    print(f"Generating {num_cases} random legal cases...")
    cases = []
    
    for _ in range(num_cases):
        try:
            case = generate_legal_case()
            cases.append(case)
            print(f"Created {case.case_type} case")
        except Exception as e:
            print(f"Error creating case: {e}")
    
    print(f"Generated {len(cases)} cases successfully.")
    return cases

# Helper function to serialize a case to dictionary
def case_to_dict(case):
    if case.case_type == CaseTypeEnum.CRIMINAL:
        result = {
            'case_type': case.case_type,
            'subtype': case.subtype,
            'fir_number': case.fir_number,
            'police_station': case.police_station,
            'arrest_date': str(case.arrest_date) if case.arrest_date else None,
            'bail_status': case.bail_status,
            'investigation_status': case.investigation_status,
            'chargesheet_filed': case.chargesheet_filed,
            'chargesheet_date': str(case.chargesheet_date) if case.chargesheet_date else None,
            'witness_count': case.witness_count,
            'charges': [charge.charge_name for charge in case.charges.all()],
            'evidence_types': [evidence.evidence_type for evidence in case.evidence_types.all()],
            'other_details': case.other_details,
        }
        
        # Add subtype-specific details
        if case.murder_homicide:
            result['murder_homicide'] = {
                'victim_details': {
                    'name': case.murder_homicide.victim.name,
                    'contact_info': case.murder_homicide.victim.contact_info
                },
                'weapon_used': case.murder_homicide.weapon_used
            }
        elif case.theft:
            result['theft'] = {
                'property_type': case.theft.property_type,
                'estimated_value': case.theft.estimated_value
            }
        elif case.assault:
            result['assault'] = {
                'injury_severity': case.assault.injury_severity,
                'weapon_used': case.assault.weapon_used
            }
        elif case.fraud:
            result['fraud'] = {
                'amount_involved': case.fraud.amount_involved,
                'fraud_type': case.fraud.fraud_type
            }
        
        return result
    
    # Add similar serialization logic for other case types...
    # For brevity, I'm just returning a basic object for other case types
    return {
        'case_type': case.case_type,
        'id': case.id
    }

# Main function to run the script
def main():
    cases = create_test_dataset(5)
    
    # Convert to dictionaries for JSON serialization
    case_dicts = [case_to_dict(case) for case in cases]
    
    # Print or save the output
    print(json.dumps(case_dicts, indent=2))
    
    # Optionally save to file
    with open('legal_cases.json', 'w') as f:
        json.dump(case_dicts, f, indent=2)
    
    print("Data saved to legal_cases.json")

if __name__ == "__main__":
    main()
