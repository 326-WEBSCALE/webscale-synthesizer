from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *

def index(request, snippetID=None):
    """
    View function for home page of site.
    """
    page_context = {'page_title': 'W E B S C A L E'}

    # Normally the user would be determined by the session, but here we will
    # use Steve's account as an example
    example_user = OldUser.objects.get(name='Steven Borst')
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
                             comment.text, comment.date_posted),
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
    snippits = Snippit.objects.filter(is_public=True).order_by('-id')[:5]
    return render(
        request,
        'synthesizer/feed.html',
        context={'page_title': 'Activity Feed', 'snippits': snippits},
    )

def profile(request, profile_id=""):
    """
    View function for a profile page.
    If the given profile id argument is not given, the profile of
    the current user will be shown
    """

    logged_in_user = None
    if request.user.is_authenticated:
        logged_in_user = request.user

    display_edit_link = False
    if profile_id == "" and logged_in_user:
        profile_id = logged_in_user.get_username()
        profile_id = "d097b337df594c35a01d997bfbeaad42"
        display_edit_link = True
    elif profile_id == "" and not logged_in_user:
        return handler404(request)

    displayed_user = get_object_or_404(OldUser, id=profile_id)
    programs = Snippit.objects.filter(user_id=profile_id)
    return render(
        request,
        'synthesizer/profile.html',
        context={'page_title': displayed_user.name,
                 'display_edit_link': display_edit_link,
                 'programs': programs},
    )

@login_required
def profile_edit(request):
    """
    Allows a user to edit their profile
    """
    user = OldUser.objects.get(name='Steven Borst')
    programs = Snippit.objects.filter(user_id=user.id)
    profile_id = "d097b337df594c35a01d997bfbeaad42"  # default to steven's profile for now
    return render(
        request,
        'synthesizer/profile_edit.html',
        context={'page_title': 'Edit Profile', 'programs': programs, 
          'user': user},
    )

def handler404(request):
    """
    The page to be rendered when the requested path is not found.
    """
    return render(
        request,
        '404.html',
        context={'page_title': '404 Page Not Found'},
        )
