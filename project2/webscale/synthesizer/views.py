from django.shortcuts import render

# Create your views here.
from .models import *

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    return render(
        request,
        'index.html',
        context={'page_title': 'W E B S C A L E'},
    )

def about(request):
    """
    View function for the about page.
    """
    return render(
        request,
        'synthesizer/about.html',
        context={'page_title': 'About Us'},
    )
def discussion(request):
    """
    View function for the discussion page.
    """
    return render(
        request,
        'synthesizer/discussion.html',
        context={'page_title': 'Discussion'},
    )
def faq(request):
    """
    View function for the faq page.
    """
    return render(
        request,
        'synthesizer/faq.html',
        context={'page_title': 'FAQ'},
    )
def feed(request):
    """
    View function for the feed page.
    """
    return render(
        request,
        'synthesizer/feed.html',
        context={'page_title': 'Activity Feed'},
    )
def profile(request):
    """
    View function for the profile page.
    """
    return render(
        request,
        'synthesizer/profile.html',
        context={'page_title': 'Profile'},
    )
