from django.conf import settings
from .models import *

def common(request):
    all_parent_category = ParentCategory.objects.all()
    other_category = Category.objects.all()
    return {'all_parent_category': all_parent_category, 'other_category': other_category}
