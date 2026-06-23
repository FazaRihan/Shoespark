from rest_framework import serializers
from .models import Product, Variation
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug']


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id', 'variation_category', 'variation_value', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variations = VariationSerializer(
        many=True,
        read_only=True,
        source='variation_set'
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'is_available',
            'is_new',
            'image_url',
            'category',
            'variations',
            'created_at',
            'updated_at',
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None