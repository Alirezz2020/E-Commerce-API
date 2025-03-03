from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total(self):
        total = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
        self.total = total
        self.save()

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def clean(self):
        # Ensure quantity is positive and not exceeding available inventory
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        if self.quantity > self.product.inventory:
            raise ValidationError("Not enough inventory for this product.")

    def save(self, *args, **kwargs):
        # Determine if this is an update or a new order item.
        if self.pk:
            previous = OrderItem.objects.get(pk=self.pk)
            diff = self.quantity - previous.quantity
            if diff > 0:
                if diff > self.product.inventory:
                    raise ValidationError("Not enough inventory for the updated quantity.")
                self.product.inventory -= diff
            elif diff < 0:
                self.product.inventory += abs(diff)
            self.product.save()
        else:
            # New order item – validate before reducing inventory.
            if self.quantity > self.product.inventory:
                raise ValidationError("Not enough inventory to fulfill this order.")
            self.product.inventory -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)
        # Update the order total after saving the order item.
        self.order.update_total()

    def delete(self, *args, **kwargs):
        # Return the quantity back to inventory before deleting
        self.product.inventory += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
