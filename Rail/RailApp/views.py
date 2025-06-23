from PIL import Image
from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from transformers import pipeline
from .models import Complaint
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404


# Hugging Face pipelines
sentiment_classifier = pipeline("sentiment-analysis")
image_classifier = pipeline("zero-shot-image-classification")


def index(request):
    features = [
        {"title": "AI Categorization", "icon": "fa-brain", "text": "Complaints auto-categorized using NLP.", "gradient": "#2196f3, #00bcd4"},
        {"title": "Urgency Detection", "icon": "fa-bolt", "text": "Detects and prioritizes critical complaints.", "gradient": "#43cea2, #185a9d"},
        {"title": "Smart Routing", "icon": "fa-route", "text": "Auto-routes to correct department.", "gradient": "#ff9800, #f44336"},
        {"title": "AI Insights", "icon": "fa-chart-line", "text": "Visual analytics for better services.", "gradient": "#00c6ff, #0072ff"},
    ]
    return render(request, 'index.html', {'features': features})


def file_complaint(request):
    if request.method == "POST":
        pnr = request.POST.get("pnr", "UNKNOWN")
        category = request.POST.get("category", "Uncategorized")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        evidence_files = request.FILES.getlist("evidence")

        sentiment_result = sentiment_classifier(description)
        sentiment = sentiment_result[0]['label']

        image_classification = "No image provided"
        if evidence_files:
            try:
                image = Image.open(evidence_files[0])
                candidate_labels = ["cleanliness", "security", "emergency"]
                image_result = image_classifier(image, candidate_labels=candidate_labels)
                image_classification = image_result[0]['label']
            except:
                image_classification = "Image processing failed"

        complaint = Complaint.objects.create(
            pnr_number=pnr,
            category=category,
            subject=subject,
            complaint_text=description,
            phone=phone,
            email=email,
            sentiment=sentiment,
            image_classification=image_classification,
            complaint_image=evidence_files[0] if evidence_files else None
        )

        messages.success(request, "Complaint submitted successfully.")
        return redirect("/")

    return render(request, "complaint.html")


def track_complaint(request):
    complaint = None
    query = ""

    if request.method == "POST":
        query = request.POST.get("query")
        try:
            complaint = Complaint.objects.filter(pnr_number__iexact=query).latest('created_at')
        except Complaint.DoesNotExist:
            complaint = None

    return render(request, 'track.html', {'complaint': complaint, 'query': query})


def analytics(request):
    return render(request, 'analytics.html')


def help_support(request):
    return render(request, 'help.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('admins')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def admin(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin.html', {'complaints': complaints})


def classified(request):
    cleanliness_complaints = Complaint.objects.filter(image_classification="cleanliness").order_by('-created_at')
    emergency_complaints = Complaint.objects.filter(image_classification="emergency").order_by('-created_at')
    security_complaints = Complaint.objects.filter(image_classification="security").order_by('-created_at')

    return render(request, 'classified.html', {
        'cleanliness_complaints': cleanliness_complaints,
        'emergency_complaints': emergency_complaints,
        'security_complaints': security_complaints,
    })


def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    # Mark as resolved
    complaint.is_resolved = True
    complaint.save()

    # Send email
    send_mail(
        subject='Rail Madad - Your Complaint Has Been Resolved',
        message=f"Dear {complaint.name},\n\nYour complaint (PNR: {complaint.pnr_number}) has been resolved. Thank you for reporting.\n\n-- Rail Madad AI Team",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[complaint.email],
        fail_silently=False,
    )

    messages.success(request, f"Complaint by {complaint.email} marked as resolved and email sent.")
    return redirect('classified') 


def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    messages.success(request, "Complaint deleted successfully.")
    return redirect('admin')