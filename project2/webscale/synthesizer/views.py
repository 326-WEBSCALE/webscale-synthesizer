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
    )

def about(request):
    """
    View function for the about page.
    """
    return render(
        request,
        'synthesizer/about.html',
    )
def discussion(request):
    """
    View function for the discussion page.
    """
    return render(
        request,
        'synthesizer/discussion.html',
    )
def faq(request):
    """
    View function for the faq page.
    """
    return render(
        request,
        'synthesizer/faq.html',
    )
def feed(request):
    """
    View function for the feed page.
    """
    return render(
        request,
        'synthesizer/feed.html',
    )
def profile(request):
    """
    View function for the profile page.
    """
    return render(
        request,
        'synthesizer/profile.html',
    )
