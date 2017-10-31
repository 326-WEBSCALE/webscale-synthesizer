from django.shortcuts import render

# Create your views here.
from .models import *

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    d = '14debd2def58452ab795a6b973977920'
    snippet = Snippit.objects.get(pk=d)
    all_user_snippets = map(lambda snip: (snip.get_id(), snip.get_name(), snip.get_description()),
                            Snippit.objects.filter(user_id=snippet.get_user_id()))
    return render(
        request,
        'index.html',
        context={'page_title': 'W E B S C A L E',
                 'snippet_name': ": {0}".format(snippet.get_name()),
                 'snippet_user_id': snippet.get_user_id(),
                 'snippet_description': snippet.get_description(),
                 'snippet_text': snippet.get_program_text(),
                 'snippet_result': snippet.get_synthesizer_result(),
                 'snippet_is_public': snippet.get_is_public(),
                 'all_user_snippets': all_user_snippets,
        },
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
