from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import shuffle, choices, randint
from string import ascii_letters, digits 

class ColorChoices(models.TextChoices):
    RED = 'red', _('Red')
    BLUE = 'blue', _('Blue')
    GREEN = 'green', _('Green')
    YELLOW = "yellow", _("Yellow")
    BLACK = 'black', _('Black')
    WHITE = 'white', _('White')
    ORANGE = 'orange', _('Orange')
    PINK = "pink", _("Pink")
    GRAY = "gray", _("Gray")


class CompanyChoices(models.TextChoices):
    APPLE = 'apple', _('Apple')
    SAMSUNG = 'samsung', _('Samsung')
    XIAOMI = 'xiaomi', _('Xiaomi')
    HUAWEI = 'huawei', _('Huawei')
    LG = 'lg', _('LG')
    SONY = 'sony', _('Sony')
    NIKE = 'nike', _('Nike')
    ADIDAS = 'adidas', _('Adidas')
    PUMA = 'puma', _('Puma')
    ZARA = 'zara', _('Zara')
    H_AND_M = 'h&m', _('H&M')
    OTHER = 'other', _('Other')


class BrandChoices(models.TextChoices):
    PREMIUM = 'premium', _('Premium')
    STANDARD = 'standard', _('Standard')
    ECONOMY = 'economy', _('Economy')
    LUXURY = 'luxury', _('Luxury')
    BUDGET = 'budget', _('Budget')
    OTHER = 'other', _('Other')


class SizeChoices(models.TextChoices):
    XS = 'xs', _('Extra Small')
    S = 's', _('Small')
    M = 'm', _('Medium')
    L = 'l', _('Large')
    XL = 'xl', _('Extra Large')
    XXL = 'xxl', _('2XL')
    XXXL = 'xxxl', _('3XL')
    ONE_SIZE = 'one_size', _('One Size')
    OTHER = 'other', _('Other')


class ConditionChoices(models.TextChoices):
    NEW = 'new', _('New')
    LIKE_NEW = 'like_new', _('Like New')
    USED = 'used', _('Used')
    REFURBISHED = 'refurbished', _('Refurbished')
    DAMAGED = 'damaged', _('Damaged')
    FOR_PARTS = 'for_parts', _('For Parts')


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to='category/image')
    description = models.TextField()
    color = models.CharField(max_length=50, choices=ColorChoices.choices, default=ColorChoices.BLACK)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        number = 1

        while Category.objects.filter(slug=slug).exists():
            slug = slugify(self.name) + f"-{number}"
            number += 1
        self.slug = slug

        return super().save(*args, **kwargs)
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_categories')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        suffix = choices(ascii_letters + digits, k=randint(5, 20))
        shuffle(suffix)
        slug += "".join(suffix)
        self.slug = slug

        return super().save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='country/icons')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    desc = models.TextField()
    main_image = models.FileField(upload_to='products/main_images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='products')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=0)
    review = models.PositiveIntegerField(default=0)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    delivery_time = models.CharField(max_length=100)
    star = models.PositiveSmallIntegerField(default=0)
    company = models.CharField(max_length=200, choices=CompanyChoices.choices, blank=True)
    brand = models.CharField(max_length=200, choices=BrandChoices.choices, blank=True)
    size = models.CharField(max_length=100, choices=SizeChoices.choices, blank=True)
    dicount = models.PositiveSmallIntegerField(default=0)
    color = models.CharField(max_length=50, choices=ColorChoices.choices, blank=True)
    verified = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    condition = models.CharField(max_length=100, choices=ConditionChoices.choices, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            suffix = choices(ascii_letters + digits, k=randint(5, 15))
            shuffle(suffix)
            self.slug = slug + "-" + "".join(suffix)
        
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    image = models.FileField(upload_to='products/images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='services/images')
    desc = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title