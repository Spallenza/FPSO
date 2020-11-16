
from rest_framework import viewsets
from rest_framework.decorators import action

from api.models.Vessel import Vessel
from api.models.User import User
from api.models.Equipment import Equipment
from api.serializers import UserSerializer, EquipmentSerializer, VesselSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (IsAuthenticated,)

    
    @action(
        methods=['post'],
        detail=False,
        url_name='inactivate',
    )
    def inactivate(self, request, *args, **kwargs):
    
        result = False
        if request is not None and 'code_list' in request.data:
            if len(request.data['code_list'])>0:
                serializer = self.serializer_class()    
                result = serializer.inactivate(request.data['code_list'])

        if result:
            content = {'data': 'Equipment(s) Successfully Inactivated'}
            return Response(content, status=status.HTTP_200_OK)

        content = {'data': 'Bad Request'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    
    @action(
        methods=['post'],
        detail=False,
        url_name='activate',
    )
    def activate(self, request, *args, **kwargs):
    
        result = False
        if request is not None and 'code_list' in request.data:
            if len(request.data['code_list'])>0:
                serializer = self.serializer_class()    
                result = serializer.activate(request.data['code_list'])

        if result:
            content = {'data': 'Equipment(s) Successfully Activated'}
            return Response(content, status=status.HTTP_200_OK)

        content = {'data': 'Bad Request'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class VesselViewSet(viewsets.ModelViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
    permission_classes = (IsAuthenticated,)


    @action(detail=True)
    def equipments(self, request, pk):
        serializer = self.serializer_class()
        result = serializer.equipments(pk)
        content = {'data': result}
        return Response(content, status=status.HTTP_200_OK)        
        