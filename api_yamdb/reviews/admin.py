from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)

admin.site.empty_value_display = '(None)'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс Admin Category."""

    list_display = ("pk", "name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс Admin Genre."""

    list_display = ("pk", "name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс Admin Title."""

    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
        "get_genre"
    )
    list_filter = ("name",)
    search_fields = ("name",)
    list_editable = ("category",)

    def get_genre(self, object):
        return ', '.join((genre.name for genre in object.genre.all()))

    get_genre.short_description = 'Жанр произведения'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс Admin Review."""

    list_display = (
        "pk",
        "author",
        "text",
        "score",
        "pub_date",
        "title"
    )
    list_filter = ("author__username", "pub_date")
    search_fields = ("author__username",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс Admin Comment."""

    list_display = (
        "pk",
        "author",
        "text",
        "pub_date",
        "review"
    )
    list_filter = ("author__username", "pub_date")
    search_fields = ("author__username",)


admin.site.register(GenreTitle)
