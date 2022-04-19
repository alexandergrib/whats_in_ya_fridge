from django.db import models
from datetime import date

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Category"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CookingTechnology(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cooking Technology"
        verbose_name_plural = "Cooking Technology"


class Allergens(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField("Description")


class BaseIngredients(models.Model):
    """Single Ingredient"""
    name = models.CharField(max_length=150)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="ingredients/")
    origin = models.CharField("Place of origin", max_length=500, blank=True)
    vegan_friendly = models.BooleanField(default=False)
    vegetarian_friendly = models.BooleanField(default=False)
    weight = models.PositiveSmallIntegerField(default=1)
    allergens = models.ForeignKey(Allergens, on_delete=models.SET_NULL,
                                  null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Base Ingredient"
        verbose_name_plural = "Base Ingredients"


class Recipe(models.Model):
    """Recipes"""
    DIFFICULTY_CHOICES = (
        ('1', 'Super Easy'),
        ('2', 'Easy'),
        ('3', 'Medium'),
        ('4', 'Hard'),
        ('5', 'professional'),
    )

    name = models.CharField("Name", max_length=100)
    time_cooking = models.DurationField(default=None)
    portions = models.PositiveSmallIntegerField("Portions", default=1)
    ingredients = models.ManyToManyField(BaseIngredients)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="recipes/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    technology = models.ForeignKey(CookingTechnology,
                                   on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    weight = models.PositiveSmallIntegerField(default=1)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={"slug": self.name})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"


class BaseIngredientNutrition(models.Model):
    """Ingredients Nutritional Values"""
    base_ingredient_name = models.ForeignKey(BaseIngredients,
                                             on_delete=models.CASCADE)
    energy = models.PositiveSmallIntegerField(help_text="set in kcal")
    fat = models.PositiveSmallIntegerField(help_text="set in grams")
    sugars = models.PositiveSmallIntegerField(help_text="set in grams")
    salt = models.PositiveSmallIntegerField(help_text="set in grams")
    saturates = models.PositiveSmallIntegerField(help_text="set in grams")
    carbohydrates = models.PositiveSmallIntegerField(help_text="set in grams")
    fibre = models.PositiveSmallIntegerField(help_text="set in grams")
    protein = models.PositiveSmallIntegerField(help_text="set in grams")

    def __str__(self):
        return self.base_ingredient_name.name

    def get_absolute_url(self):
        return reverse('recipe_detail',
                       kwargs={"slug": self.base_ingredient_name.name})

    class Meta:
        verbose_name = "Ingredient Nutrition"
        verbose_name_plural = "Ingredients Nutrition"


class RatingStar(models.Model):
    """Rating Stars"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE,
                             verbose_name="star")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name="recipe", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.recipe}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Review Text", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True,
        null=True, related_name="children"
    )
    recipe = models.ForeignKey(Recipe, verbose_name="recipe",
                               on_delete=models.CASCADE,
                               related_name='reviews')

    def __str__(self):
        return f"{self.name} - {self.recipe}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class RecipeImages(models.Model):
    """Recipe images"""
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="recipe_images/")
    recipe = models.ForeignKey(Recipe, verbose_name="Recipe",
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Recipe Image"
        verbose_name_plural = "Recipe Images"
