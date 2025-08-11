from django.contrib import admin
from .models import Business, Location, Asset, ComplianceTask

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'business')
    list_filter = ('state', 'city')
    search_fields = ('address', 'business__name')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'purchase_date')
    list_filter = ('location__business__name',)
    search_fields = ('name', 'model_number', 'serial_number')

@admin.register(ComplianceTask)
class ComplianceTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'asset', 'next_due_date', 'is_completed')
    list_filter = ('is_completed', 'next_due_date', 'asset__location__business__name')
    search_fields = ('title', 'asset__name')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(is_completed=True)
    mark_as_completed.short_description = "Mark selected tasks as completed"
