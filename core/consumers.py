# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from .models import Cart, Customer
from asgiref.sync import sync_to_async

class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.customer_id = self.scope['url_route']['kwargs']['customer_id']
        self.room_group_name = f"cart_{self.customer_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Fetch cart data for the customer
        cart_data = await self.get_cart_data(self.customer_id)
        
        # Send the cart data as a JSON response
        await self.send(text_data=json.dumps({
            "type": "initial_cart_data",
            "data": cart_data
        }, cls=DjangoJSONEncoder))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        pass

    async def cart_update(self, event):
        """
        Send updated cart data to the client.
        """
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type": "cart_update",
            "data": message
        }))

    @sync_to_async
    def get_cart_data(self, customer_id):
        """
        Fetch cart data for the customer.
        """
        carts = Cart.objects.filter(customer_id=customer_id).select_related('product')
        cart_data = []
        for cart in carts:
            cart_data.append({
                "product_name": cart.product.name,
                "quantity": cart.quantity,
                "total_price": float(cart.total_price()),  # Convert Decimal to float for JSON serialization
                "created_at": cart.created_at.isoformat()
            })
        return cart_data