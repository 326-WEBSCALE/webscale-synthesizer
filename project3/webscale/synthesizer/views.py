from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request, snippetID=None):
    """
    View function for home page of site.
    """
    page_context = {'page_title': 'W E B S C A L E'}

    # Normally the user would be determined by the session, but here we will
    # use Steve's account as an example
    example_user = User.objects.get(username='sborst')
    all_user_snippets = map(lambda snip: (snip.id.hex, snip.name, snip.description),
                            Snippit.objects.filter(user_id=example_user))
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

def profile(request, profile_id=None):
    """
    View function for a profile page.
    If the given profile id argument is not given, the profile of
    the current user will be shown
    """
    # If at /profile/, show logged in user or 404
    display_edit_link = False
    if profile_id is None:
        if request.user.is_authenticated:
            profile_user = request.user
            display_edit_link = True
        else:
            return handler404(request)
    else:
        profile_user = get_object_or_404(User, username=profile_id)
        if request.user.is_authenticated and request.user.username == profile_user.username:
            display_edit_link = True

    programs = Snippit.objects.filter(user_id=profile_user)

    return render(
        request,
        'synthesizer/profile.html',
        context={'page_title': profile_user.get_full_name(),
                 'user': profile_user,
                 'user_full_name': profile_user.get_full_name(),
                 'display_edit_link': display_edit_link,
                 'programs': programs},
    )

@login_required
def profile_edit(request):
    """
    Allows a user to edit their profile
    """
    user = User.objects.get(username='sborst')
    programs = Snippit.objects.filter(user_id=user.id)
    #TODO: This is overriding the session user var. Fix.
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
