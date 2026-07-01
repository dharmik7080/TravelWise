from rest_framework import serializers
from destinations.models import Destination
from attractions.models import Attraction
from packages.models import Package
from trips.models import Trip, ItineraryTemplate, ItineraryDay
from seasons.models import BestSeason

class DestinationSerializer(serializers.ModelSerializer):
    """
    Serializer representing travel destinations and associated rating/cost fields.
    """
    class Meta:
        model = Destination
        fields = '__all__'


class AttractionSerializer(serializers.ModelSerializer):
    """
    Serializer representing tourist attractions, mapping foreign key to read-only name.
    """
    destination_name = serializers.ReadOnlyField(source='destination.destination_name')

    class Meta:
        model = Attraction
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    """
    Serializer representing package items, mapping parent destination properties.
    """
    destination_name = serializers.ReadOnlyField(source='destination.destination_name')

    class Meta:
        model = Package
        fields = '__all__'


class ItineraryTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer representing predefined day-by-day travel template curations.
    """
    destination_name = serializers.ReadOnlyField(source='destination.destination_name')

    class Meta:
        model = ItineraryTemplate
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer representing user-specific trips, keeping owner references read-only.
    """
    destination_name = serializers.ReadOnlyField(source='destination.destination_name')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('user',)


class ItineraryDaySerializer(serializers.ModelSerializer):
    """
    Serializer representing active day-by-day trip itinerary details.
    """
    class Meta:
        model = ItineraryDay
        fields = '__all__'


class BestSeasonSerializer(serializers.ModelSerializer):
    """
    Serializer representing destination seasonal parameters and peak travel months.
    """
    destination_name = serializers.ReadOnlyField(source='destination.destination_name')

    class Meta:
        model = BestSeason
        fields = '__all__'
