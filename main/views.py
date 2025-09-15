from __future__ import annotations
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters

from .models import (
    CarouselItem,
    Category,
    Product,
    ProductImage,
    Advantage,
    Metric,
    TeamMember,
    Value,
    CompanyInfo,
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
    return render(request, "index.html", {"carousel": carousel})


def catalog(request):
    qs = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")
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
    context = {
        "categories": categories,
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "active_category": active_category,
    }
    return render(request, "catalog.html", context)


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )
    images = product.images.all().order_by("-is_primary", "ordering", "id")
    return render(
        request,
        "product_detail.html",
        {"product": product, "images": images},
    )


def about(request):
    advantages = Advantage.objects.filter(is_active=True).order_by("ordering")
    metrics = Metric.objects.filter(is_active=True).order_by("ordering")
    team = TeamMember.objects.filter(is_active=True).order_by("ordering")
    values = Value.objects.filter(is_active=True).order_by("ordering")
    company = CompanyInfo.objects.first()
    context = {
        "advantages": advantages,
        "metrics": metrics,
        "team": team,
        "values": values,
        "company": company,
    }
    return render(request, "about.html", context)


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
