# Generated by Django 5.0 on 2023-12-21 12:16

import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_use_email_as_username.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                    "role_name",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("manager", "Manager"),
                            ("customer", "Customer"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
            options={
                "verbose_name": "Role",
                "verbose_name_plural": "Roles",
            },
        ),
        migrations.CreateModel(
            name="User",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, message="Minimum length should be 2"
                            )
                        ],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, message="Minimum length should be 2"
                            )
                        ],
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=14,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be in the format: (999) 999-9999",
                                regex="^\\(\\d{3}\\) \\d{3}-\\d{4}$",
                            )
                        ],
                    ),
                ),
                ("birth_date", models.DateField()),
                (
                    "email",
                    models.EmailField(
                        max_length=80,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Minimum length should be 10"
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
                    "password",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                6, message="Minimum length should be 6"
                            )
                        ],
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
                ("role", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="custom_user_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="custom_user_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
            managers=[
                ("objects", django_use_email_as_username.models.BaseUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserAddress",
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
                ("title", models.CharField(max_length=80)),
                (
                    "first_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, message="Minimum length should be 2"
                            )
                        ],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, message="Minimum length should be 2"
                            )
                        ],
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=14,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be in the format: (999) 999-9999",
                                regex="^\\(\\d{3}\\) \\d{3}-\\d{4}$",
                            )
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=80,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Minimum length should be 10"
                            )
                        ],
                    ),
                ),
                ("tc", models.CharField(max_length=11)),
                (
                    "address",
                    models.TextField(
                        max_length=250,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Minimum length should be 10"
                            )
                        ],
                    ),
                ),
                (
                    "province",
                    models.CharField(
                        max_length=70,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                1, message="Minimum length should be 1"
                            )
                        ],
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        max_length=70,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                1, message="Minimum length should be 1"
                            )
                        ],
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        max_length=70,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                1, message="Minimum length should be 1"
                            )
                        ],
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.user"
                    ),
                ),
            ],
            options={
                "verbose_name": "User Address",
            },
        ),
        migrations.CreateModel(
            name="UserRole",
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
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.user"
                    ),
                ),
            ],
            options={
                "verbose_name": "User Role",
                "verbose_name_plural": "User Roles",
            },
        ),
    ]