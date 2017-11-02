from django.shortcuts import get_object_or_404, render

# Create your views here.
from .models import *

def index(request, snippetID=None):
    """
    View function for home page of site.
    """
    page_context = {'page_title': 'W E B S C A L E'}

    # Normally the user would be determined by the session, but here we will
    # use Steve's account as an example
    example_user = User.objects.get(name='Steven Borst')
    all_user_snippets = map(lambda snip: (snip.id.hex, snip.name, snip.description),
                            Snippit.objects.filter(user_id=example_user.id))
    page_context['all_user_snippets'] = all_user_snippets

    if snippetID is None:
        return render(request, 'index.html', page_context)


    snippet = Snippit.objects.get(pk=snippetID)

    page_context['snippet_id'] = snippet.id.hex
    page_context['snippet_name'] = ": {0}".format(snippet.name)
    page_context['snippet_user_id'] = snippet.user_id
    page_context['snippet_description'] = snippet.description
    page_context['snippet_text'] = snippet.program_text
    page_context['snippet_spec'] = snippet.program_spec
    page_context['snippet_result'] = snippet.synthesizer_result
    page_context['snippet_is_public'] = snippet.is_public

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
def discussion(request, snippetID):
    """
    View function for the discussion page.
    """
    page_context = {'page_title': 'Discussion'}
    snippet = Snippit.objects.get(pk=snippetID)
    snippet_comments = list(
        map(lambda comment: (comment.user_id.name,
                         comment.text, comment.date),
                            Comment.objects.filter(snippit_id=snippetID))
        )
    print(list(snippet_comments))
    page_context['snippet_id'] = snippet.id.hex
    page_context['snippet_name'] = snippet.name
    page_context['snippet_user_id'] = snippet.user_id
    page_context['snippet_description'] = snippet.description
    page_context['snippet_text'] = snippet.program_text
    page_context['snippet_result'] = snippet.synthesizer_result
    page_context['snippet_comments'] = snippet_comments

    return render(
        request,
        'synthesizer/discussion.html',
        page_context,
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
def profile(request, profile_id="0"):
    """
    View function for a profile page.
    If the given profile id argument is not given, the profile of
    the current user will be shown
    """
    if profile_id == "0":
        profile_id = "d097b337df594c35a01d997bfbeaad42"  # default to steven's profile for now
    user = get_object_or_404(User, id=profile_id)
    programs = Snippit.objects.filter(user_id=user.id)
    return render(
        request,
        'synthesizer/profile.html',
        context={'page_title': user.name, 'user': user, 'programs': programs},
    )

def profile_edit(request):
    """
    Allows a user to edit their profile
    """
    user = User.objects.get(name='Steven Borst')
    programs = Snippit.objects.filter(user_id=user.id)
    return render(
        request,
        'synthesizer/profile_edit.html',
        context={'page_title': 'Edit Profile', 'programs': programs},
    )
