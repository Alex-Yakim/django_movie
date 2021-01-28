from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Все категории фильмов"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/lust_movie.html')
def get_lust_movie():
    """Последние добавленные фильмы"""
    movies = Movie.objects.filter(draft=False).order_by('-id')[:5]
    return {'lust_movies': movies}
