import base64 
 
from django.core.files.base import ContentFile
from rest_framework import serializers 
 
import webcolors 
 
 
class ColorNameConverter(serializers.Field): 
    def to_representation(self, value): 
        return value 
 
    def to_internal_value(self, data): 
        try: 
            return webcolors.hex_to_name(data) 
        except ValueError: 
            raise serializers.ValidationError( 
                "Имя для данного цвета не найдено." 
            ) 
 
 
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
 