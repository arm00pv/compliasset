from django.db import models
from django.contrib.auth.models import User
import uuid

def user_directory_path(instance, filename):
    return f'business_{instance.asset.location.business.id}/{filename}'

class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="The legal name of the business.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='locations')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.business.name} - {self.address}, {self.city}"

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=200, help_text="e.g., 'Walk-in Freezer', 'Fire Extinguisher #3'")
    model_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_document = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.name

class ComplianceTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, help_text="e.g., 'Annual Fire Safety Inspection'")
    description = models.TextField(blank=True, null=True)
    frequency_months = models.PositiveIntegerField(default=12, help_text="How often (in months) should this task be performed?")
    last_completed_date = models.DateField(blank=True, null=True)
    next_due_date = models.DateField()
    completion_certificate = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} for {self.asset.name}"

    class Meta:
        ordering = ['next_due_date']

