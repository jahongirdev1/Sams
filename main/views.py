from __future__ import annotations
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import gettext as _, get_language

from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters

from utils.telegram import send_telegram_message

from .models import (
    CarouselItem,
    SectionHeader,
    Category,
    Product,
    ProductImage,
    Advantage,
    Metric,
    TeamMember,
    Value,
    Video,
    CompanyInfo,
    SocialMap,
    ContactAddress,
    ContactPhone,
    ContactEmail,
    ContactWorkingHours,
    ContactTopic,
    ContactRequest,
)


# ----------------- Serializers -----------------


class CarouselItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselItem
        fields = ["id", "title", "subtitle", "image", "link_url", "ordering"]


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "products_count"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text", "ordering", "is_primary"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "images",
            "created_at",
        ]


class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = "__all__"


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = "__all__"


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"


# ----------------- Filters -----------------


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    price__gte = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "price__gte", "price__lte"]


# ----------------- HTML Views -----------------


def index(request):
    carousel = (
        CarouselItem.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )
    images_prefetch = Prefetch(
        "images",
        queryset=ProductImage.objects.prefetch_related("translations").order_by(
            "-is_primary", "ordering", "id"
        ),
    )
    main_products = (
        Product.objects.filter(is_active=True, is_main=True)
        .select_related("category")
        .prefetch_related("translations", "category__translations", images_prefetch)
        .order_by("-created_at")[:8]
    )
    metrics = (
        Metric.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")[:3]
    )
    home_video = (
        Video.objects.filter(page=Video.Page.HOME, is_active=True)
        .prefetch_related("translations")
        .order_by("order", "-created_at")
        .first()
    )
    company = CompanyInfo.objects.prefetch_related("translations").first()
    contacts = company
    context = {
        "carousel": carousel,
        "main_products": main_products,
        "metrics": metrics,
        "home_video": home_video,
        "company": company,
        "contacts": contacts,
        "active_page": "home",
    }
    return render(request, "index.html", context)


def catalog_view(request):
    cat_slug = request.GET.get("category")
    search_query = request.GET.get("q")
    language_code = getattr(request, "LANGUAGE_CODE", None) or get_language()

    images_prefetch = Prefetch(
        "images",
        queryset=ProductImage.objects.prefetch_related("translations").order_by(
            "-is_primary", "ordering", "id"
        ),
    )
    qs = Product.objects.filter(is_active=True)
    if cat_slug and cat_slug != "all":
        qs = qs.filter(category__slug=cat_slug)
    if search_query:
        translation_q = Q(translations__name__icontains=search_query) | Q(
            translations__description__icontains=search_query
        )
        if language_code:
            translation_q = translation_q & Q(translations__language_code=language_code)
        qs = qs.filter(translation_q).distinct()

    qs = (
        qs.select_related("category")
        .prefetch_related("translations", "category__translations", images_prefetch)
        .order_by("-created_at")
    )

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.GET.get("partial") == "1":
        return render(request, "partials/_products_grid.html", {"products": page_obj.object_list})

    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()

    categories = Category.objects.all().prefetch_related("translations")
    contacts = CompanyInfo.objects.prefetch_related("translations").first()
    header = (
        SectionHeader.objects.filter(slug="catalog", is_active=True)
        .prefetch_related("translations")
        .first()
    )
    active_cat = cat_slug or "all"

    context = {
        "categories": categories,
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "active_page": "catalog",
        "active_cat": active_cat,
        "q": search_query,
        "query_string": query_string,
        "contacts": contacts,
        "header": header,
    }
    return render(request, "catalog.html", context)


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.select_related("category")
        .prefetch_related("translations", "category__translations", "images__translations"),
        slug=slug,
        is_active=True,
    )
    images = (
        product.images.all()
        .prefetch_related("translations")
        .order_by("-is_primary", "ordering", "id")
    )
    contacts = CompanyInfo.objects.prefetch_related("translations").first()
    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "images": images,
            "active_page": "catalog",
            "contacts": contacts,
        },
    )


def about(request):
    advantages = (
        Advantage.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )
    metrics = (
        Metric.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )
    team = (
        TeamMember.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )
    values = (
        Value.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )
    about_video = (
        Video.objects.filter(page=Video.Page.ABOUT, is_active=True)
        .prefetch_related("translations")
        .order_by("order", "-created_at")
        .first()
    )
    company = CompanyInfo.objects.prefetch_related("translations").first()
    contacts = company
    header = (
        SectionHeader.objects.filter(slug="about", is_active=True)
        .prefetch_related("translations")
        .first()
    )
    context = {
        "advantages": advantages,
        "metrics": metrics,
        "team": team,
        "values": values,
        "about_video": about_video,
        "company": company,
        "contacts": contacts,
        "active_page": "about",
        "header": header,
    }
    return render(request, "about.html", context)


def _get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def contact_view(request):
    addresses = (
        ContactAddress.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order", "id")
    )
    phones = (
        ContactPhone.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order", "id")
    )
    emails = (
        ContactEmail.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("order", "id")
    )
    hours = (
        ContactWorkingHours.objects.filter(is_active=True)
        .prefetch_related("translations")
        .first()
    )
    topics = (
        ContactTopic.objects.all()
        .prefetch_related("translations")
        .order_by("slug")
    )
    social = (
        SocialMap.objects.filter(is_active=True)
        .only(
            "instagram_url",
            "facebook_url",
            "youtube_url",
            "tiktok_url",
            "telegram_url",
            "map_embed",
            "map_url",
            "is_active",
            "updated_at",
        )
        .first()
    )

    form_data = {
        "name": "",
        "phone": "",
        "email": "",
        "topic": "",
        "message": "",
        "consent": False,
    }
    form_errors = []
    form_success = False

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        topic_value = request.POST.get("topic", "").strip()
        message_text = request.POST.get("message", "").strip()
        consent_value = request.POST.get("consent")

        form_data.update(
            {
                "name": name,
                "phone": phone,
                "email": email,
                "topic": topic_value,
                "message": message_text,
                "consent": bool(consent_value),
            }
        )

        if not name:
            form_errors.append(_("Укажите имя."))
        if not phone:
            form_errors.append(_("Укажите телефон."))
        if not message_text:
            form_errors.append(_("Введите сообщение."))
        if not consent_value:
            form_errors.append(_("Необходимо согласие на обработку данных."))

        topic = None
        if topic_value:
            topic = (
                ContactTopic.objects.filter(slug=topic_value)
                .prefetch_related("translations")
                .first()
            )
            if topic is None:
                topic = (
                    ContactTopic.objects.filter(pk=topic_value)
                    .prefetch_related("translations")
                    .first()
                )

        if not form_errors:
            contact_request = ContactRequest.objects.create(
                name=name,
                phone=phone,
                email=email,
                topic=topic,
                message=message_text,
                consent=bool(consent_value),
                ip=_get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            timestamp = timezone.localtime(contact_request.created_at).strftime("%d.%m.%Y %H:%M")
            topic_name = (
                topic.safe_translation_getter("name", any_language=True) if topic else _("Не выбрана")
            )
            email_display = email or "—"
            telegram_text = "\n".join(
                [
                    _("<b>Новая заявка</b>"),
                    _("Имя: {name}").format(name=escape(name)),
                    _("Телефон: {phone}").format(phone=escape(phone)),
                    _("Email: {email}").format(email=escape(email_display)),
                    _("Тема: {topic}").format(topic=escape(topic_name)),
                    _("Сообщение: {message}").format(message=escape(message_text)),
                    _("Время: {timestamp}").format(timestamp=timestamp),
                ]
            )
            send_telegram_message(telegram_text)

            form_success = True
            form_data = {
                "name": "",
                "phone": "",
                "email": "",
                "topic": "",
                "message": "",
                "consent": False,
            }

    contacts = CompanyInfo.objects.prefetch_related("translations").first()
    header = (
        SectionHeader.objects.filter(slug="contact", is_active=True)
        .prefetch_related("translations")
        .first()
    )
    context = {
        "addresses": addresses,
        "phones": phones,
        "emails": emails,
        "hours": hours,
        "topics": topics,
        "form_data": form_data,
        "form_errors": form_errors,
        "form_success": form_success,
        "active_page": "contact",
        "social": social,
        "contacts": contacts,
        "header": header,
    }
    status = 200 if not form_errors else 400
    return render(request, "contact.html", context, status=status)

# ----------------- API ViewSets -----------------


@method_decorator(cache_page(60 * 5), name="list")
class CarouselViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CarouselItemSerializer
    queryset = (
        CarouselItem.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )


@method_decorator(cache_page(60 * 5), name="list")
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = (
        Category.objects.all()
        .prefetch_related("translations")
        .annotate(products_count=Count("products", filter=Q(products__is_active=True)))
    )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filterset_class = ProductFilter
    search_fields = ["translations__name", "slug", "translations__description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                "translations",
                "category__translations",
                "images__translations",
            )
        )


class AdvantageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdvantageSerializer
    queryset = (
        Advantage.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    queryset = (
        Metric.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = (
        TeamMember.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )


class ValueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValueSerializer
    queryset = (
        Value.objects.filter(is_active=True)
        .prefetch_related("translations")
        .order_by("ordering")
    )


class CompanyInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanyInfoSerializer
    queryset = CompanyInfo.objects.all().prefetch_related("translations")
