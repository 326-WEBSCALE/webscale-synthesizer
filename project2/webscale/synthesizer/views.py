from django.shortcuts import render

# Create your views here.
from .models import *

def index(request, snippetID=None):
    """
    View function for home page of site.
    """
    page_context = {'page_title': 'W E B S C A L E'}
    if snippetID is None:
        return render(request, 'index.html', page_context)

    snippet = Snippit.objects.get(pk=snippetID)
    all_user_snippets = map(lambda snip: (snip.get_id().hex, snip.get_name(), snip.get_description()),
                            Snippit.objects.filter(user_id=snippet.get_user_id()))

    page_context['snippet_id'] = snippet.get_id()
    page_context['snippet_name'] = ": {0}".format(snippet.get_name())
    page_context['snippet_user_id'] = snippet.get_user_id()
    page_context['snippet_description'] = snippet.get_description()
    page_context['snippet_text'] = snippet.get_program_text()
    page_context['snippet_result'] = snippet.get_synthesizer_result()
    page_context['snippet_is_public'] = snippet.get_is_public()
    page_context['all_user_snippets'] = all_user_snippets

    return render(
        request,
        'index.html',
        page_context,
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
