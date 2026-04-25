from django.contrib import admin
from .models import Category, Transaction, Budget, Insight

# This tells Django to show these tables in your dashboard
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Insight)