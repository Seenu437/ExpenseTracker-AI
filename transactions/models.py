from django.conf import settings
from django.db import models


class Category(models.Model):

    CATEGORY_TYPES = [
        ('Need', 'Need'),
        ('Want', 'Want'),
        ('Savings', 'Savings'),
        ('Income', 'Income'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category_name = models.CharField(max_length=100)

    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Transaction(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Wallet', 'Wallet'),
        ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='UPI'
    )

    transaction_date = models.DateField()

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['user', 'transaction_date'],
                name='idx_user_date'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"