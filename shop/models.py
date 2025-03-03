from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Category model for organizing products.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Product model with category relation.
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Review model for product feedback.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.product}"

# Order model with status field.
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    products = models.ManyToManyField(Product, through='OrderItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total(self):
        total = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
        self.total = total
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

# OrderItem model with inventory management.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        if self.quantity > self.product.inventory:
            raise ValidationError("Not enough inventory for this product.")

    def save(self, *args, **kwargs):
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
            if self.quantity > self.product.inventory:
                raise ValidationError("Not enough inventory to fulfill this order.")
            self.product.inventory -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        self.product.inventory += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
