from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer

from .serializers import *

class CustomerRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginAPIView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CustomerDetailView(APIView):
    def get(self, request, phone):
        customer = get_object_or_404(Customer, phone=phone)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
class StaffLoginAPIView(APIView):
    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer

# Create Product
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get List of Products
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Get Single Product
class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Update Product
class ProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Update product
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Product
class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()  # Delete product
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Update Stock of Product
class ProductStockUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        stock = request.data.get('stock')
        if stock is not None and isinstance(stock, int) and stock >= 0:
            product.stock = stock  # Update stock
            product.save()
            return Response({"message": "Stock updated successfully", "stock": product.stock}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid stock value."}, status=status.HTTP_400_BAD_REQUEST)


class SubmitComplaintAPI(APIView):
    def post(self, request):
        # Extract phone number from the request
        phone = request.data.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the customer by phone number
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a complaint for the customer
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)  # Associate the complaint with the customer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintListAPI(APIView):
    def get(self, request):
        # Extract phone number from query parameters
        phone = request.query_params.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the customer by phone number
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all complaints for the customer
        complaints = Complaint.objects.filter(customer=customer)
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

