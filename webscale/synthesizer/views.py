from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime


from .models import *
from django.contrib.auth.models import User

from django import forms

class SnippetSaveForm(forms.Form):
    # Hidden fields on the form
    program = forms.CharField()
    spec = forms.CharField()
    output = forms.CharField()

    name = forms.CharField()
    desc = forms.CharField()
    is_public = forms.BooleanField(required=False)

def index(request, snippetID=None):
    """
    View function for home page of site.
    """
    page_context = {'page_title': 'W E B S C A L E'}

    profile_user = None
    if request.user.is_authenticated:
        profile_user = request.user

        user_snippets = map(lambda snip: (snip.id.hex, snip.name, snip.description),
                                Snippit.objects.filter(user_id=profile_user))

        page_context['user_snippets'] = user_snippets

    # Logic for saving a snippet
    if request.user.is_authenticated and request.method == 'POST':
        form = SnippetSaveForm(request.POST)

        print(snippetID)

        if form.is_valid():
            if not snippetID:
                snippet = Snippit.objects.create()
            else:
                snippet = Snippit.objects.get(pk=snippetID)

            snippet.user_id = request.user
            snippet.name = form.cleaned_data['name']
            snippet.description = form.cleaned_data['desc']
            snippet.is_public = form.cleaned_data['is_public']

            snippet.program_text = form.cleaned_data['spec']
            snippet.program_spec = form.cleaned_data['program']
            snippet.synthesizer_result = form.cleaned_data['output']
            snippet.save()

            user_snippets = map(lambda snip: (snip.id.hex, snip.name, snip.description),
                                Snippit.objects.filter(user_id=profile_user))

            page_context['user_snippets'] = user_snippets
            return HttpResponseRedirect(reverse('program', args=[snippet.id.hex]))


    if snippetID is None:
        return render(request, 'index.html', page_context)

    snippet = Snippit.objects.get(pk=snippetID)

    page_context['snippet_id'] = snippet.id.hex
    page_context['snippet_name'] = ": {0}".format(snippet.name)
    page_context['snippet_actual_name'] = snippet.name
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

class CommentForm(forms.Form):
    text = forms.CharField()

def discussion(request, snippetID):
    """
    View function for the discussion page.
    """
    snippet = Snippit.objects.get(pk=snippetID)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Comment.objects.create()
            post.user_id = request.user
            post.date_posted = datetime.today()
            post.snippit_id = snippet
            post.text = form.cleaned_data['text']
            post.save()
            return HttpResponseRedirect('/discussion/'+snippetID)
        else:
            return handler404(request)

    page_context = {'page_title': 'Discussion'}
    snippet_comments = list(
        map(lambda comment: (comment.user_id.get_full_name(),
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

class ProfileEditForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(required=False)

@login_required
def profile_edit(request):
    """
    Allows a user to edit their profile
    """
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            if form.cleaned_data['password'] is not "":
                user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponseRedirect('/profile/edit')
        else:
            return handler404(request)
    else:
        programs = Snippit.objects.filter(user_id=user.id)
        return render(
            request,
            'synthesizer/profile_edit.html',
            context={'page_title': 'Edit Profile', 'programs': programs, 
            },
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
