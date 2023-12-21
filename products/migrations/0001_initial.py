# Generated by Django 5.0 on 2023-12-21 12:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=70,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                4, message="Minimum length should be 4"
                            )
                        ],
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Not published"), (1, "Published (for users)")],
                        default=0,
                    ),
                ),
                ("image", models.ImageField(upload_to="")),
                (
                    "builtIn",
                    models.BooleanField(
                        choices=[
                            (0, "Cannot be deleted or updated"),
                            (1, "Can be deleted or updated"),
                        ],
                        default=0,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=80,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, message="Minimum length should be 2"
                            )
                        ],
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Not published"), (1, "Published (for users)")],
                        default=0,
                    ),
                ),
                (
                    "builtIn",
                    models.BooleanField(
                        choices=[
                            (0, "Cannot be deleted or updated"),
                            (1, "Can be deleted or updated"),
                        ],
                        default=0,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_id", models.CharField(max_length=100, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "Shopping Cart Item",
                "verbose_name_plural": "Shopping Cart Items",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction",
                    models.CharField(
                        choices=[
                            ("CREATED", "Created"),
                            ("UPDATED", "Updated"),
                            ("CANCELED", "Canceled"),
                            ("COMPLETED", "Completed"),
                        ],
                        max_length=100,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sku",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Minimum length should be 10"
                            )
                        ],
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, message="Minimum length should be 5"
                            )
                        ],
                    ),
                ),
                ("short_desc", models.CharField(blank=True, max_length=300, null=True)),
                ("long_desc", models.TextField(blank=True, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tax", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinLengthValidator(
                                0, message="Minimum length should be 0"
                            )
                        ]
                    ),
                ),
                ("stock_amount", models.IntegerField()),
                ("stock_alarm_limit", models.IntegerField()),
                (
                    "slug",
                    models.SlugField(
                        max_length=200,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, message="Minimum length should be 5"
                            )
                        ],
                    ),
                ),
                ("featured", models.BooleanField(default=False)),
                ("image", models.ImageField(upload_to="")),
                ("new_product", models.BooleanField()),
                ("like", models.IntegerField(default=0)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Not published"), (1, "Published (for users)")],
                        default=0,
                    ),
                ),
                ("width", models.DecimalField(decimal_places=2, max_digits=10)),
                ("length", models.DecimalField(decimal_places=2, max_digits=10)),
                ("height", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "builtIn",
                    models.BooleanField(
                        choices=[
                            (0, "Cannot be deleted or updated"),
                            (1, "Can be deleted or updated"),
                        ],
                        default=0,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "brand_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.brand"
                    ),
                ),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.BinaryField()),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
                "db_table": "your_table_name",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=200)),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Minimum value should be 1"
                            ),
                            django.core.validators.MaxValueValidator(
                                5, message="Maximum value should be 5"
                            ),
                        ]
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Not published"), (1, "Published (for users)")],
                        default=0,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("published_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
            },
        ),
    ]
