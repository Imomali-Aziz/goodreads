from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Review


def landing_page(request):
    return render(request, 'landing.html')


def home_page(request):
    reviews = Review.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(reviews, page_size)

    page_num = request.GET.get('page_num', 1)
    page_obj = paginator.get_page(page_num)

    return render(request, 'home_page.html', {'page_obj': page_obj})
