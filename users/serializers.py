from rest_framework import serializers

from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        user = User.objects.create(**validated_data)
        if location_data:
            for location in location_data:
                location_obj, _ = Location.objects.get_or_create(**location)
                user.location.add(location_obj)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Update user data

        About Location:
        Trying to get the old location name (if it exists) and compare with
        the new location name (if we got it from validated_data).
        If they are the same or both do not exist, nothing changes.
        If the new name is different - the old location is deleted and the new one is recorded!
        """
        try:
            old_location = instance.location.first().name
        except Exception:
            old_location = None

        location_data = validated_data.pop('location', None)
        if location_data:
            new_location = location_data[0]['name']

            if new_location != old_location:
                instance.location.clear()
                for location in location_data:
                    location_obj, _ = Location.objects.get_or_create(**location)
                    instance.location.add(location_obj)

        instance = super().update(instance, validated_data)
        return instance