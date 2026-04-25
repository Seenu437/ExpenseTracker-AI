from django.db import models
from django.contrib.auth.models import User

# 1. CATEGORY TABLE
class Category(models.Model):
    TYPE_CHOICES = [
        ('Need', 'Need'),
        ('Want', 'Want'),
        ('Savings', 'Savings'),
        ('Income', 'Income')
    ]
    
    category_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Null = Global Category
    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

# 2. TRANSACTION TABLE
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Financial standard
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This index ensures your ML queries run in <100ms as promised in your report!
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.category.category_name} - {self.amount}"

# 3. BUDGET TABLE
class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True) # Null = Overall Budget
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 4. INSIGHT TABLE (The Explainable AI Storage)
class Insight(models.Model):
    INSIGHT_TYPES = [
        ('Anomaly', 'Anomaly'),
        ('Budget_Pacing', 'Budget_Pacing'),
        ('Trend', 'Trend')
    ]
    
    insight_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    insight_text = models.TextField() # "Reduce Dining by ₹450"
    insight_type = models.CharField(max_length=50, choices=INSIGHT_TYPES)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Mathematical weight
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_month = models.IntegerField(null=True, blank=True)
    reference_year = models.IntegerField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    analysis_start_date = models.DateField(null=True, blank=True)
    analysis_end_date = models.DateField(null=True, blank=True)
    generation_model = models.CharField(max_length=100, null=True, blank=True) # 'Isolation_Forest', etc.