from rest_framework import serializers
from .models import (
    User, Category, Product, Specification,
    Build, BuildItem, Order, OrderItem, Review
)




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'phone', 'role']
        read_only_fields = ['id', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'phone']

    def create(self, validated_data):
           password = validated_data.pop('password')
           user = User(**validated_data)
           user.set_password(password)
           user.save()
           return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'spec_key', 'spec_value']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'image', 'stock',
                  'category_name', 'specifications']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'brand', 'price', 'image',
                  'description', 'stock', 'specifications']

    def create(self, validated_data):
        specs_data = validated_data.pop('specifications', [])
        product = Product.objects.create(**validated_data)
        for spec in specs_data:
            Specification.objects.create(product=product, **spec)
        return product




class BuildItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = BuildItem
        fields = ['id', 'product', 'product_id', 'quantity']


class BuildSerializer(serializers.ModelSerializer):
    items = BuildItemSerializer(many=True, read_only=True)

    class Meta:
        model = Build
        fields = ['id', 'name', 'total_price', 'total_tdp', 'is_public',
                  'created_at', 'items']
        read_only_fields = ['total_price', 'total_tdp']



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_moment']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'address', 'payment_method',
                  'comment', 'created_at', 'items']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'product', 'rating', 'text',
                  'is_approved', 'created_at']
        read_only_fields = ['user', 'is_approved']