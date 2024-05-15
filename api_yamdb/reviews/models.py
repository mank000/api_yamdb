from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.const import (
    DEFAULT_LENGTH_TEXT,
    MAX_SCORE_VALUE,
    MAX_LEN_NAME_SIZE,
    MIN_SCORE_VALUE,
    TITLE_MAX_LEN_SLUG_SIZE,
)
from reviews.validators import year_validator

User = get_user_model()


class CategoryGenreModel(models.Model):
    """Абстрактный класс для категорий и жанров."""
    
    name = models.CharField(
        max_length=MAX_LEN_NAME_SIZE,
        verbose_name="Hазвание",
    )
    slug = models.SlugField(
        verbose_name="slug",
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        abstract = True
    
    def __str__(self):
        return self.name[:DEFAULT_LENGTH_TEXT]
    
class CommentReviewModel(models.Model):
    """Абстрактный класс для даты комментариев и отзывов."""

    text = models.TextField(verbose_name="текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Aвтор"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ("-pub_date",)
        abstract = True

    def __str__(self):
        return self.text


class Category(CategoryGenreModel):
    """Класс категорий."""

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Genre(CategoryGenreModel):
    """Класс жанров."""

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(max_length=TITLE_MAX_LEN_SLUG_SIZE,
                            verbose_name="Hазвание")
    year = models.SmallIntegerField(
        verbose_name="год выпуска",
        validators=[
            MaxValueValidator(
                year_validator,
                message="Значение года не может быть больше текущего",
            ),
        ],
    )
    description = models.TextField(verbose_name="описание", blank=True)
    genre = models.ManyToManyField(
        Genre, through="GenreTitle", related_name="titles", verbose_name="жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="категория",
        null=True,
    )

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "Произведения"
        ordering = ("-year", "name")

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательный класс, для связи жанра и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="жанр"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="произведение"
    )

    class Meta:
        verbose_name = "cоответствие жанра и произведения"
        verbose_name_plural = "Таблица соответствия жанров и произведений"

    def __str__(self):
        return f"{self.title} соответствует жанру {self.genre}"


class Review(CommentReviewModel):
    """Класс рецензий."""

    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(
                MIN_SCORE_VALUE,
                message="Оценка ниже допустимой"
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                message="Оценка выше допустимой"
            ),
        ],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="произведение",
        null=True,
    )

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_author_title"
            ),
        )

    def __str__(self):
        return self.text


class Comment(CommentReviewModel):
    """Класс комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="oтзыв",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
