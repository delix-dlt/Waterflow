from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Leitura, Contador
from .serializers import LeituraSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

class LeituraViewSet(viewsets.ModelViewSet):
    queryset = Leitura.objects.all().order_by('-captured_at', '-created_at')
    serializer_class = LeituraSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        contador_serial = self.request.query_params.get('contador_serial')
        if contador_serial:
            qs = qs.filter(contador__serial=contador_serial)
        return qs

    def create(self, request, *args, **kwargs):
        # delega validação e criação no serializer
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        leitura = serializer.save()
        return Response(self.get_serializer(leitura).data, status=status.HTTP_201_CREATED)


