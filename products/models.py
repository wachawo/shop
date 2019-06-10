from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category/', blank=True)
    parent_category = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, models.CASCADE)
    price = models.PositiveIntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name
