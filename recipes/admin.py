from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (Category, CookingTechnology, Allergens,
                     BaseIngredients, BaseIngredientNutrition,
                     Recipe, Rating, RatingStar, Review, RecipeImages)


class RecipeAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description = forms.CharField(label="Description", widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category"""
    list_display = ("name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class RecipeImagesInline(admin.TabularInline):
    model = RecipeImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Image"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipes"""
    list_display = ("name", "category", "url", "draft")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    # inlines = [RecipeImagesInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = RecipeAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("name", "category"),)
        }),
        (None, {
            "fields": (("time_cooking", "portions", 'difficulty', 'technology'),)
        }),
        (None, {
            "fields": ("description", ("image", "get_image"))
        }),
        ("Ingredients", {
            "fields": ("ingredients", )
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("name", "email", "parent", "recipe", "id")
    readonly_fields = ("name", "email")


@admin.register(CookingTechnology)
class CookingTechnologyAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "recipe", "ip")


@admin.register(RecipeImages)
class RecipeImagesAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "recipe", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Images"


admin.site.register(RatingStar)

admin.site.site_title = "What in ya Fridge"
admin.site.site_header = "What in ya Fridge"