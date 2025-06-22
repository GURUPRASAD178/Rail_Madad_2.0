from django.db import models

class Complaint(models.Model):
    name = models.CharField(max_length=100, default="Anonymous")  # Optional name
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    complaint_text = models.TextField()
    category = models.CharField(max_length=100, default="Uncategorized")
    sentiment = models.CharField(max_length=100, default='none')
    image_classification = models.CharField(max_length=100, default='none')
    pnr_number = models.CharField(max_length=50, default='UNKNOWN')
    complaint_image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.email} ({'Resolved' if self.is_resolved else 'Pending'})"
