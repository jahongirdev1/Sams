from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
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
    path("i18n/", include("django.conf.urls.i18n")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(router.urls)),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
