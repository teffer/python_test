from rest_framework import serializers
from .models import CustomUser, Organization
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(many=True, queryset=Organization.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'organizations']

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        print("Token generated:", token)
        return token
    
    def create(self, validated_data):
        print('creat called')
        user = validated_data['user']
        print(user)
        user_data = CustomUserSerializer(user).data
        token = self.get_token(user)
        return {
            'refresh': str(token),
            'access': str(token),
            'user': user_data 
        }
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError({'non_field_errors': ['Invalid credentials']})
        token = self.get_token(user)
        response_data = {
            'refresh': str(token),
            'access': str(token),
            'user': CustomUserSerializer(user).data 
        }
        print(response_data)
        return response_data