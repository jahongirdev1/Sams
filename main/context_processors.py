from .models import (
    Category,
    ContactAddress,
    ContactEmail,
    ContactPhone,
    ContactWorkingHours,
    SocialMap,
)


def categories(request):
    return {
        "menu_categories": Category.objects.all().prefetch_related("translations"),
    }


def global_contacts(request):
    return {
        "footer_addresses": ContactAddress.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order")[:3],
        "footer_phones": ContactPhone.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order")[:3],
        "footer_emails": ContactEmail.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order")[:2],
        "footer_hours": ContactWorkingHours.objects.filter(is_active=True)
        .prefetch_related("translations")
        .first(),
        "footer_social": SocialMap.objects.filter(is_active=True).first(),
    }
