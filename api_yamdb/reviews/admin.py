from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
    )


class CategoryAdmin(admin.ModelAdmin):
    """Класс Admin Category."""
    
    list_display = ("pk", "name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "пусто"


class GenreAdmin(admin.ModelAdmin):
    """Класс Admin Genre."""
    
    list_display = ("pk", "name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "пусто"


class TitleAdmin(admin.ModelAdmin):
    """Класс Admin Title."""

    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
        "get_genre",
        "count_reviews",
        "get_rating"
    )
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "пусто"

    def get_genre(self, obj):
        # реализация вашего метода для получения жанра
        pass
    
    def count_reviews(self, obj):
        # реализация вашего метода для подсчета отзывов
        pass
    
    def get_rating(self, obj):
        # реализация вашего метода для получения рейтинга
        pass


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
    list_filter = ("author", "pub_date")
    search_fields = ("author",)



class CommentAdmin(admin.ModelAdmin):
    """Класс Admin Comment."""

    list_display = (
        "pk",
        "author",
        "text",
        "pub_date",
        "review"
    )
    list_filter = ("author", "pub_date")
    search_fields = ("author",)
    empty_value_display = "пусто"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle)
