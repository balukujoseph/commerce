from .models import Category
def category_list(request):
    return{
         "all_categories": Category.objects.all()
    }
   