from __future__ import annotations
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.utils.html import escape

from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters

from utils.telegram import send_telegram_message

from .models import (
    CarouselItem,
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
    carousel = CarouselItem.objects.filter(is_active=True).order_by("ordering")
    images_prefetch = Prefetch(
        "images",
        queryset=ProductImage.objects.order_by("-is_primary", "ordering", "id"),
    )
    main_products = (
        Product.objects.filter(is_active=True, is_main=True)
        .select_related("category")
        .prefetch_related(images_prefetch)
        .order_by("-created_at")[:8]
    )
    metrics = Metric.objects.filter(is_active=True).order_by("ordering")[:3]
    home_video = (
        Video.objects.filter(page=Video.Page.HOME, is_active=True)
        .order_by("order", "-created_at")
        .first()
    )
    company = CompanyInfo.objects.first()
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


def catalog(request):
    images_prefetch = Prefetch(
        "images",
        queryset=ProductImage.objects.order_by("-is_primary", "ordering", "id"),
    )
    qs = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(images_prefetch)
        .order_by("-created_at")
    )
    categories = Category.objects.all()
    category_slug = request.GET.get("category")
    q = request.GET.get("q")
    active_category = None
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
        active_category = categories.filter(slug=category_slug).first()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()
    contacts = CompanyInfo.objects.first()
    context = {
        "categories": categories,
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "active_category": active_category,
        "active_page": "catalog",
        "q": q,
        "query_string": query_string,
        "category_slug": category_slug,
        "contacts": contacts,
    }
    return render(request, "catalog.html", context)


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )
    images = product.images.all().order_by("-is_primary", "ordering", "id")
    contacts = CompanyInfo.objects.first()
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
    advantages = Advantage.objects.filter(is_active=True).order_by("ordering")
    metrics = Metric.objects.filter(is_active=True).order_by("ordering")
    team = TeamMember.objects.filter(is_active=True).order_by("ordering")
    values = Value.objects.filter(is_active=True).order_by("ordering")
    about_video = (
        Video.objects.filter(page=Video.Page.ABOUT, is_active=True)
        .order_by("order", "-created_at")
        .first()
    )
    company = CompanyInfo.objects.first()
    contacts = company
    context = {
        "advantages": advantages,
        "metrics": metrics,
        "team": team,
        "values": values,
        "about_video": about_video,
        "company": company,
        "contacts": contacts,
        "active_page": "about",
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
        .order_by("order", "id")
        .only("title", "city", "address", "order", "is_active")
    )
    phones = (
        ContactPhone.objects.filter(is_active=True)
        .order_by("order", "id")
        .only("label", "phone", "order", "is_active")
    )
    emails = (
        ContactEmail.objects.filter(is_active=True)
        .order_by("order", "id")
        .only("label", "email", "order", "is_active")
    )
    hours = (
        ContactWorkingHours.objects.filter(is_active=True)
        .only("weekdays", "saturday", "sunday", "note", "is_active")
        .first()
    )
    topics = ContactTopic.objects.all().order_by("name").only("name", "slug")
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
            form_errors.append("Укажите имя.")
        if not phone:
            form_errors.append("Укажите телефон.")
        if not message_text:
            form_errors.append("Введите сообщение.")
        if not consent_value:
            form_errors.append("Необходимо согласие на обработку данных.")

        topic = None
        if topic_value:
            topic = ContactTopic.objects.filter(slug=topic_value).only("id", "name", "slug").first()
            if topic is None:
                topic = ContactTopic.objects.filter(pk=topic_value).only("id", "name", "slug").first()

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
            topic_name = topic.name if topic else "Не выбрана"
            email_display = email or "—"
            telegram_text = "\n".join(
                [
                    "<b>Новая заявка</b>",
                    f"Имя: {escape(name)}",
                    f"Телефон: {escape(phone)}",
                    f"Email: {escape(email_display)}",
                    f"Тема: {escape(topic_name)}",
                    f"Сообщение: {escape(message_text)}",
                    f"Время: {timestamp}",
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

    contacts = CompanyInfo.objects.first()
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
    }
    status = 200 if not form_errors else 400
    return render(request, "contact.html", context, status=status)

# ----------------- API ViewSets -----------------


@method_decorator(cache_page(60 * 5), name="list")
class CarouselViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CarouselItemSerializer
    queryset = CarouselItem.objects.filter(is_active=True).order_by("ordering")


@method_decorator(cache_page(60 * 5), name="list")
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().annotate(
        products_count=Count("products", filter=Q(products__is_active=True))
    )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("images")
        )


class AdvantageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdvantageSerializer
    queryset = Advantage.objects.filter(is_active=True).order_by("ordering")


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    queryset = Metric.objects.filter(is_active=True).order_by("ordering")


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.filter(is_active=True).order_by("ordering")


class ValueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValueSerializer
    queryset = Value.objects.filter(is_active=True).order_by("ordering")


class CompanyInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanyInfoSerializer
    queryset = CompanyInfo.objects.all()
