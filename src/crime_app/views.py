# File: legal_app/views.py
from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.http import JsonResponse
from .models import (
    CriminalCase,
    CivilCase,
    FamilyLawCase,
    PropertyLawCase,
    ConsumerDisputeCase,
    LabourDisputeCase,
    IntellectualPropertyCase,
    PublicLawCase,
)


def home(request):
    """Home view with basic statistics for all case types"""

    # Count cases by type
    case_counts = {
        "Criminal": CriminalCase.objects.count(),
        "Civil": CivilCase.objects.count(),
        "Family Law": FamilyLawCase.objects.count(),
        "Property Law": PropertyLawCase.objects.count(),
        "Consumer Dispute": ConsumerDisputeCase.objects.count(),
        "Labour Dispute": LabourDisputeCase.objects.count(),
        "Intellectual Property": IntellectualPropertyCase.objects.count(),
        "Public Law": PublicLawCase.objects.count(),
    }

    # Total cases
    total_cases = sum(case_counts.values())

    # Recent cases (last 10)
    # We would need a common timestamp field to properly implement this
    # Here's a conceptual implementation
    recent_criminal_cases = CriminalCase.objects.all().order_by("-created_at")[:5]

    context = {
        "case_counts": case_counts,
        "total_cases": total_cases,
        "recent_criminal_cases": recent_criminal_cases,
    }

    return render(request, "legal_app/home.html", context)


def criminal_dashboard(request):
    """Dashboard for criminal cases"""

    # Count cases by subtype
    subtype_counts = CriminalCase.objects.values("subtype").annotate(count=Count("id"))

    # Count cases by investigation status
    investigation_status_counts = CriminalCase.objects.values(
        "investigation_status"
    ).annotate(count=Count("id"))

    # Count cases by bail status
    bail_status_counts = CriminalCase.objects.values("bail_status").annotate(
        count=Count("id")
    )

    # Chargesheet filed vs not filed
    chargesheet_counts = {
        "Filed": CriminalCase.objects.filter(chargesheet_filed=True).count(),
        "Not Filed": CriminalCase.objects.filter(chargesheet_filed=False).count(),
    }

    context = {
        "subtype_counts": subtype_counts,
        "investigation_status_counts": investigation_status_counts,
        "bail_status_counts": bail_status_counts,
        "chargesheet_counts": chargesheet_counts,
        "total_cases": CriminalCase.objects.count(),
    }

    return render(request, "legal_app/criminal_dashboard.html", context)


def civil_dashboard(request):
    """Dashboard for civil cases"""

    # Count cases by subtype
    subtype_counts = CivilCase.objects.values("subtype").annotate(count=Count("id"))

    # Average claim amount
    avg_claim = CivilCase.objects.filter(claim_amount__isnull=False).aggregate(
        Avg("claim_amount")
    )

    # Settlement attempts
    settlement_counts = {
        "Attempted": CivilCase.objects.filter(settlement_attempts=True).count(),
        "Not Attempted": CivilCase.objects.filter(settlement_attempts=False).count(),
    }

    context = {
        "subtype_counts": subtype_counts,
        "avg_claim": avg_claim,
        "settlement_counts": settlement_counts,
        "total_cases": CivilCase.objects.count(),
    }

    return render(request, "legal_app/civil_dashboard.html", context)


def family_law_dashboard(request):
    """Dashboard for family law cases"""

    # Count cases by subtype
    subtype_counts = FamilyLawCase.objects.values("subtype").annotate(count=Count("id"))

    # Children involved
    children_involved_counts = {
        "Involved": FamilyLawCase.objects.filter(children_involved=True).count(),
        "Not Involved": FamilyLawCase.objects.filter(children_involved=False).count(),
    }

    context = {
        "subtype_counts": subtype_counts,
        "children_involved_counts": children_involved_counts,
        "total_cases": FamilyLawCase.objects.count(),
    }

    return render(request, "legal_app/family_law_dashboard.html", context)


def property_law_dashboard(request):
    """Dashboard for property law cases"""

    # Count cases by subtype
    subtype_counts = PropertyLawCase.objects.values("subtype").annotate(
        count=Count("id")
    )

    # Total properties involved
    property_count = PropertyLawCase.objects.aggregate(
        total_properties=Count("properties")
    )

    context = {
        "subtype_counts": subtype_counts,
        "property_count": property_count,
        "total_cases": PropertyLawCase.objects.count(),
    }

    return render(request, "legal_app/property_law_dashboard.html", context)


def consumer_dashboard(request):
    """Dashboard for consumer dispute cases"""

    # Count cases by subtype
    subtype_counts = ConsumerDisputeCase.objects.values("subtype").annotate(
        count=Count("id")
    )

    # Total compensation claimed
    total_compensation = ConsumerDisputeCase.objects.filter(
        compensation_claimed__isnull=False
    ).aggregate(Sum("compensation_claimed"))

    context = {
        "subtype_counts": subtype_counts,
        "total_compensation": total_compensation,
        "total_cases": ConsumerDisputeCase.objects.count(),
    }

    return render(request, "legal_app/consumer_dashboard.html", context)


def labour_dashboard(request):
    """Dashboard for labour dispute cases"""

    # Count cases by subtype
    subtype_counts = LabourDisputeCase.objects.values("subtype").annotate(
        count=Count("id")
    )

    context = {
        "subtype_counts": subtype_counts,
        "total_cases": LabourDisputeCase.objects.count(),
    }

    return render(request, "legal_app/labour_dashboard.html", context)


def ip_dashboard(request):
    """Dashboard for intellectual property cases"""

    # Count cases by subtype
    subtype_counts = IntellectualPropertyCase.objects.values("subtype").annotate(
        count=Count("id")
    )

    context = {
        "subtype_counts": subtype_counts,
        "total_cases": IntellectualPropertyCase.objects.count(),
    }

    return render(request, "legal_app/ip_dashboard.html", context)


def public_law_dashboard(request):
    """Dashboard for public law cases"""

    # Count cases by subtype
    subtype_counts = PublicLawCase.objects.values("subtype").annotate(count=Count("id"))

    context = {
        "subtype_counts": subtype_counts,
        "total_cases": PublicLawCase.objects.count(),
    }

    return render(request, "legal_app/public_law_dashboard.html", context)


# API endpoints for charts
def case_type_distribution_api(request):
    """API endpoint for case type distribution chart"""
    case_counts = {
        "Criminal": CriminalCase.objects.count(),
        "Civil": CivilCase.objects.count(),
        "Family Law": FamilyLawCase.objects.count(),
        "Property Law": PropertyLawCase.objects.count(),
        "Consumer Dispute": ConsumerDisputeCase.objects.count(),
        "Labour Dispute": LabourDisputeCase.objects.count(),
        "Intellectual Property": IntellectualPropertyCase.objects.count(),
        "Public Law": PublicLawCase.objects.count(),
    }

    # Format for chart.js
    data = {
        "labels": list(case_counts.keys()),
        "datasets": [
            {
                "label": "Number of Cases",
                "data": list(case_counts.values()),
                "backgroundColor": [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF",
                    "#FF9F40",
                    "#8D6E63",
                    "#607D8B",
                ],
            }
        ],
    }

    return JsonResponse(data)
