from rest_framework import serializers

from api.models import Ads, Category
from users.models import User
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Ads
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        author = representation['author']
        if author.get('location'):
            representation['location'] = author['location'][0]['name']
        else:
            representation['location'] = None
        representation['author'] = author['first_name']
        representation['category'] = representation['category']['name']
        return representation


class AdCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Ads
        fields = '__all__'

    def create(self, validated_data):
        # Check if User and Category objects exist
        author_id = validated_data.pop('author').id
        category_id = validated_data.pop('category').id
        try:
            user = User.objects.get(id=author_id)
            category = Category.objects.get(id=category_id)
        except (User.DoesNotExist, Category.DoesNotExist):
            raise serializers.ValidationError('User and/or Category does not exist')

        # Create the Ad object
        ad = Ads.objects.create(author=user, category=category, **validated_data)
        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['id', 'name', 'price', 'description', 'is_published', 'image']

    def update(self, instance, validated_data):
        # Update the Ad object
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.is_published = validated_data.get('is_published', instance.is_published)

        # If a new image file was sent in the request, update the image field
        image = self.context['request'].FILES.get('image')
        if image:
            instance.image = image
        instance.save()

        return instance
