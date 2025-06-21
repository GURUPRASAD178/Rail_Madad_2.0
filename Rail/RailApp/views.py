from django.shortcuts import render

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
    return render(request, 'complaint.html')

def track_complaint(request):
    return render(request, 'track.html')

def analytics(request):
    return render(request, 'analytics.html')

def help_support(request):
    return render(request, 'help.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('admin')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
