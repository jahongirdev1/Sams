from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html
from django.db import models as django_models

from . import models

admin.site.site_header = "Samruks — Панель управления"
admin.site.site_title = "Админка Samruks"
admin.site.index_title = "Управление сайтом"


@admin.action(description="Включить выбранные")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Выключить выбранные")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1
    fields = ("preview", "image", "alt_text", "ordering", "is_primary")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.image.url)
        return ""

    preview.short_description = "Превью"


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_display = ("name", "slug")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_display = ("name", "category", "price", "is_active", "is_main", "created_at")
    list_filter = ("is_active", "is_main", "category")
    list_editable = ("is_main",)
    actions = [make_active, make_inactive]
    inlines = [ProductImageInline]


@admin.register(models.CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ("title", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "ordering", "is_primary")
    list_filter = ("is_primary",)


@admin.register(models.Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ("title", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ("title", "ordering", "is_active")
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "page", "is_active", "order", "created_at")
    list_filter = ("page", "is_active")
    search_fields = ("title", "youtube_url")
    ordering = ("order", "-created_at")


@admin.register(models.CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
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
class ContactAddressAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    actions = [make_active, make_inactive]


@admin.register(models.ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    actions = [make_active, make_inactive]


@admin.register(models.ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order", "id")
    actions = [make_active, make_inactive]


@admin.register(models.ContactWorkingHours)
class ContactWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ("weekdays", "saturday", "sunday", "is_active")
    list_filter = ("is_active",)

    def has_add_permission(self, request):
        if models.ContactWorkingHours.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.ContactTopic)
class ContactTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    ordering = ("name",)


@admin.register(models.ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "topic", "created_at")
    readonly_fields = ("created_at", "ip", "user_agent")
    list_filter = ("topic", "created_at")
    search_fields = ("name", "phone", "email")
