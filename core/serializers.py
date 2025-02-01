from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import Complaint

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'password']

    def create(self, validated_data):
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        try:
            customer = Customer.objects.get(phone=phone)
            if not check_password(password, customer.password):
                raise serializers.ValidationError("Invalid password")
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number")
        return data
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone']   

class StaffRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ['name', 'phone']

class StaffLoginSerializer(serializers.Serializer):
    random_id = serializers.CharField()

    def validate(self, data):
        random_id = data.get('random_id')

        try:
            # Check if a staff user exists with the provided random_id
            staff = StaffUser.objects.get(random_id=random_id)
        except StaffUser.DoesNotExist:
            raise serializers.ValidationError("Invalid random ID")
        
        return {
            "message": "Login successful",
            "staff_id": staff.random_id,
            "name": staff.name,
            "phone": staff.phone
        }



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'created_at']
        read_only_fields = ['created_at']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'customer', 'subject', 'message', 'status', 'response', 'created_at']
        read_only_fields = ['id', 'customer', 'status', 'response', 'created_at']

        
class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'product', 'product_name', 'product_price', 'quantity', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return obj.total_price()