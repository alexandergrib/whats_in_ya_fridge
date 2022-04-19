from rest_framework import permissions
from django.db import models
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe
from .serializers import RecipeListSerializer, RecipeDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer
from .service import get_client_ip


@permission_classes((permissions.AllowAny,))
class RecipeListView(APIView):
    """Display Recipe List"""
    def get(self, request):
        recipes = Recipe.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class RecipeDetailView(APIView):
    """Display Recipe Detail"""

    def get(self, request, pk):
        recipe = Recipe.objects.get(id=pk, draft=False)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ReviewCreateView(APIView):
    """Add review to the Recipe"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


@permission_classes((permissions.AllowAny,))
class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)