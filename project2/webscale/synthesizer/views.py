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
