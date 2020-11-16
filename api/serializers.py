from rest_framework import serializers
from api.models.Equipment import Equipment
from api.models.Vessel import Vessel
from api.models.User import User




class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'code', 'location', 'vessel')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['status'] = instance.status
        return ret    

    def create(self, validated_data):
        equipment = Equipment(**validated_data)
        equipment.status = 'active'
        equipment.save()
        return equipment

    def inactivate(self, code_list):
        try:
            equipments = Equipment.objects.filter(code__in=code_list)
            for equipment in equipments:
                equipment.status = 'inactive'
                equipment.save()
            return True
        except:
            return False

    def activate(self, code_list):
        try:
            equipments = Equipment.objects.filter(code__in=code_list)
            for equipment in equipments:
                equipment.status = 'active'
                equipment.save()
            return True
        except:
            return False
        


class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = ('id', 'code')
    
    def equipments(self, pk):
        equipments = Equipment.objects.filter(vessel_id=pk, status='active')

        data = [{'id': equipment.id, 'name': equipment.name, 'code': equipment.code, 'location':equipment.location} for equipment in equipments]
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
