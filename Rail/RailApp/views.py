from django.shortcuts import render
from django.contrib import messages
from . models import Complaint
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.

# views.py
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
        # Extract fields
        pnr = request.POST.get("pnr", "UNKNOWN")
        category = request.POST.get("category", "Uncategorized")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        evidence_files = request.FILES.getlist("evidence")

        # Run AI classification (optional)
        # For example:
        # category = ai_predict_category(subject + " " + description)

        # Save complaint (supporting only one evidence file for now)
        complaint = Complaint.objects.create(
            pnr_number=pnr,
            category=category,
            subject=subject,
            complaint_text=description,
            phone=phone,
            email=email,
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

    return render(request, 'track.html', {
        'complaint': complaint,
        'query': query
    })

def analytics(request):
    return render(request, 'analytics.html')

def help_support(request):
    return render(request, 'help.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('admins')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def admin(request):
    complaints = Complaint.objects.all().order_by('-created_at')  # latest first
    return render(request, 'admin.html', {'complaints': complaints})


def classified(request):
    complaints = Complaint.objects.all().order_by('-created_at')  # latest first
    return render(request, 'classified.html', {'grouped_complaints': complaints})