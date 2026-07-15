from django.conf import settings
from django.db import models
from transactions.models import Category


class Insight(models.Model):

    INSIGHT_TYPES = [
        ('Anomaly', 'Anomaly'),
        ('Budget_Pacing', 'Budget Pacing'),
        ('Trend', 'Trend'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    insight_text = models.TextField()

    insight_type = models.CharField(
        max_length=30,
        choices=INSIGHT_TYPES
    )

    metric_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    threshold_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    reference_month = models.IntegerField(
        null=True,
        blank=True
    )

    reference_year = models.IntegerField(
        null=True,
        blank=True
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    analysis_start_date = models.DateField(
        null=True,
        blank=True
    )

    analysis_end_date = models.DateField(
        null=True,
        blank=True
    )

    generation_model = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.insight_type}"