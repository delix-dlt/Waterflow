from rest_framework import serializers
from .models import Leitura, Contador

class LeituraSerializer(serializers.ModelSerializer):
    contador_serial = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Leitura
        fields = [
            'id','contador','contador_serial','device','volume','flow_rate',
            'captured_at','type','external_id','created_at'
        ]
        read_only_fields = ['id','created_at','device','contador']

    def validate(self, data):
        # volume obrigatório e >= 0
        vol = data.get('volume')
        if vol is None:
            raise serializers.ValidationError({'volume': 'This field is required.'})
        if float(vol) < 0:
            raise serializers.ValidationError({'volume': 'Must be >= 0.'})
        # precisa contar id ou serial
        if not data.get('contador') and not data.get('contador_serial'):
            # note: 'contador' normalmente não vem do JSON
            return data
        return data

    def create(self, validated_data):
        # resolve contador por serial (se fornecido)
        serial = validated_data.pop('contador_serial', None)
        if serial:
            contador = Contador.objects.filter(serial=serial).first()
            if not contador:
                raise serializers.ValidationError({'contador_serial': 'Contador not found.'})
            validated_data['contador'] = contador
        # device pode ser anexado pela view (request.device)
        request = self.context.get('request')
        if request and hasattr(request, 'device'):
            validated_data['device'] = request.device
        # captured_at uso -> se None ficará null no BD (ou usa now())
        return super().create(validated_data)
