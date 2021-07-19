from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Images will be a sequenceof seperate models
    # Tags m2m relation
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    # Category foreign key
    # Reviews, related name
    # Specifications -> table like representation
    # Shop foreign key
    times_bought = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)


# To be used only with the Product model
class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.ImageField(upload_to='images/',
    default='images/default_product.png')

    def __str__(self):
        return f'{self.product.title}\'s image'
