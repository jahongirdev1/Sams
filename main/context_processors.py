from .models import Category

def categories(request):
    return {
        'menu_categories': Category.objects.all()
    }
