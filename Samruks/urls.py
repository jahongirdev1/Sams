from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from main import views as main_views

router = DefaultRouter()
router.register(r'home/carousel', main_views.CarouselViewSet, basename='carousel')
router.register(r'catalog/categories', main_views.CategoryViewSet, basename='category')
router.register(r'catalog/products', main_views.ProductViewSet, basename='product')
router.register(r'about/advantages', main_views.AdvantageViewSet, basename='advantage')
router.register(r'about/metrics', main_views.MetricViewSet, basename='metric')
router.register(r'about/team', main_views.TeamMemberViewSet, basename='team')
router.register(r'about/values', main_views.ValueViewSet, basename='value')
router.register(r'about/company', main_views.CompanyInfoViewSet, basename='company')

urlpatterns = [
    # HTML pages
    path('', main_views.index, name='index'),
    path('catalog/', main_views.catalog, name='catalog'),
    path('product/<slug:slug>/', main_views.product_detail, name='product_detail'),
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact_view, name='contact'),

    path('admin/', admin.site.urls),

    # API schema and docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
