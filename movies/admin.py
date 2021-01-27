from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Отзывы в фильме"""
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.StackedInline):
    """Кадры из фильмов в фильме"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="250" height="200">')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('id', 'title', 'category', 'url', 'draft')
    list_display_links = ('title',)
    list_filter = ('category', 'draft', 'year', 'directors', 'actors')
    search_fields = ('title', 'category__name')
    list_editable = ('draft',)
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    actions = ['publish', 'unpublish']
    readonly_fields = ('get_image',)
    fieldsets = (
        ('Основное', {
            'fields': (('title', 'tagline'),'description')
        }),
        ('Изображение', {
            'fields': (('poster', 'get_image'),)
        }),
        ('Даты и страна', {
            'fields': (('year', 'country', 'world_premiere'),)
        }),
        ('Актеры и жанры', {
            'classes': ('collapse ',),
            'fields': (('directors', 'actors'), 'genres', 'category')
        }),
        ('Бюджет', {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Дополнительно', {
            'fields': (('url', 'draft'),)
        }),
    )


    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')


    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="200" height="250">')

    get_image.short_description = 'Изображение'


@admin.register((Reviews))
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('id', 'name', 'age', 'get_image')
    list_display_links = ('name',)
    search_fields = ['name']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'



@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('id', 'title', 'movie', 'get_image')
    list_display_links = ('title',)
    readonly_fields = ('get_image',)
    list_filter = ('movie',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг фильма"""
    list_display = ('star', 'movie', 'ip')
    list_display_links = ('star',)
    list_filter = ('movie', )


admin.site.site_title = 'Django Movie'
admin.site.site_header = 'Django Movie'

#admin.site.register(Actor)
admin.site.register(Genre)
# admin.site.register(Movie)
#admin.site.register(MovieShots)
admin.site.register(RatingStar)
#admin.site.register(Rating)
# admin.site.register(Reviews)
