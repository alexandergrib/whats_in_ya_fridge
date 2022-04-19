from rest_framework import serializers

from .models import Recipe, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class RecipeListSerializer(serializers.ModelSerializer):
    """List of recipes"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ("id", 'name', 'category', "rating_user", "middle_star")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Display review"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Recipe Detail"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ingredients = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    # difficulty = serializers.SlugRelatedField(slug_field='choices', read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "recipe")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            recipe=validated_data.get('recipe', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating

