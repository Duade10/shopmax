from . import models


def categories(request):
    categories = models.Category.objects.all()
    return dict(categories=categories)
