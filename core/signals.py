# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Cart

@receiver(post_save, sender=Cart)
def cart_update_signal(sender, instance, **kwargs):
    print('hhhhhh')
    """
    Signal handler for when a Cart instance is saved (created or updated).
    """
    send_cart_update(instance.customer_id)




@receiver(post_delete, sender=Cart)
def cart_delete_signal(sender, instance, **kwargs):
    """
    Signal handler for when a Cart instance is deleted.
    """
    send_cart_update(instance.customer_id)

def send_cart_update(customer_id):
    print('hhhhhhhhhhhhhh')
    """
    Send updated cart data to the WebSocket group.
    """
    channel_layer = get_channel_layer()
    cart_data = get_cart_data(customer_id)
    async_to_sync(channel_layer.group_send)(
        f"cart_{customer_id}",
        {
            "type": "cart_update",
            "message": cart_data
        }
    )

def get_cart_data(customer_id):
    """
    Fetch cart data for the given customer.
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