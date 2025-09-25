from django.contrib import admin
from django.db import models as django_models
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableTabularInline

from . import models

admin.site.site_header = _("Samruks — Панель управления")
admin.site.site_title = _("Админка Samruks")
admin.site.index_title = _("Управление сайтом")


@admin.action(description=_("Включить выбранные"))
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description=_("Выключить выбранные"))
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class ProductImageInline(TranslatableTabularInline):
    model = models.ProductImage
    extra = 1
    fields = ("preview", "image", "alt_text", "ordering", "is_primary")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.image.url)
        return ""

    preview.short_description = _("Превью")


@admin.register(models.Category)
class CategoryAdmin(TranslatableAdmin):
    search_fields = ("translations__name", "slug")
    list_display = ("__str__", "slug")


@admin.register(models.Product)
class ProductAdmin(TranslatableAdmin):
    search_fields = ("translations__name", "slug", "translations__description")
    list_display = ("__str__", "category", "price", "is_active", "is_main", "created_at")
    list_filter = ("is_active", "is_main", "category")
    list_editable = ("is_main",)
    actions = [make_active, make_inactive]
    inlines = [ProductImageInline]


@admin.register(models.CarouselItem)
class CarouselItemAdmin(TranslatableAdmin):
    list_display = ("__str__", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.SectionHeader)
class SectionHeaderAdmin(TranslatableAdmin):
    list_display = ("__str__", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("translations__title", "slug")
    actions = [make_active, make_inactive]


@admin.register(models.ProductImage)
class ProductImageAdmin(TranslatableAdmin):
    list_display = ("product", "ordering", "is_primary")
    list_filter = ("is_primary",)


@admin.register(models.Advantage)
class AdvantageAdmin(TranslatableAdmin):
    list_display = ("__str__", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.Metric)
class MetricAdmin(TranslatableAdmin):
    list_display = ("__str__", "value", "ordering", "is_active")
    list_filter = ("is_active",)
    search_fields = ("translations__name", "translations__value")
    actions = [make_active, make_inactive]


@admin.register(models.TeamMember)
class TeamMemberAdmin(TranslatableAdmin):
    list_display = ("__str__", "role", "ordering", "is_active")
    list_filter = ("is_active",)
    search_fields = ("translations__full_name", "translations__role")
    actions = [make_active, make_inactive]


@admin.register(models.Value)
class ValueAdmin(TranslatableAdmin):
    list_display = ("__str__", "ordering", "is_active")
    list_filter = ("is_active",)
    search_fields = ("translations__title",)
    actions = [make_active, make_inactive]


@admin.register(models.Video)
class VideoAdmin(TranslatableAdmin):
    list_display = ("id", "__str__", "page", "is_active", "order", "created_at")
    list_filter = ("page", "is_active")
    search_fields = ("translations__title", "youtube_url")
    ordering = ("order", "-created_at")


@admin.register(models.CompanyInfo)
class CompanyInfoAdmin(TranslatableAdmin):
    def has_add_permission(self, request):
        if models.CompanyInfo.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.SocialMap)
class SocialMapAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "updated_at")
    list_editable = ("is_active",)
    formfield_overrides = {
        django_models.TextField: {"widget": Textarea(attrs={"rows": 8})},
    }

    def has_add_permission(self, request):
        if models.SocialMap.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.ContactAddress)
class ContactAddressAdmin(TranslatableAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    search_fields = ("translations__title", "translations__city", "translations__address")
    actions = [make_active, make_inactive]


@admin.register(models.ContactPhone)
class ContactPhoneAdmin(TranslatableAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    search_fields = ("translations__label", "phone")
    actions = [make_active, make_inactive]


@admin.register(models.ContactEmail)
class ContactEmailAdmin(TranslatableAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    search_fields = ("translations__label", "email")
    actions = [make_active, make_inactive]


@admin.register(models.ContactWorkingHours)
class ContactWorkingHoursAdmin(TranslatableAdmin):
    list_display = ("weekdays", "saturday", "sunday", "is_active")
    list_filter = ("is_active",)
    search_fields = ("translations__weekdays", "translations__saturday", "translations__sunday")

    def has_add_permission(self, request):
        if models.ContactWorkingHours.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.ContactTopic)
class ContactTopicAdmin(TranslatableAdmin):
    search_fields = ("translations__name", "slug")
    ordering = ("slug",)


@admin.register(models.ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "topic", "created_at")
    readonly_fields = ("created_at", "ip", "user_agent")
    list_filter = ("topic", "created_at")
    search_fields = ("name", "phone", "email")
