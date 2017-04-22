# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from common.forms import LoginForm, SignupForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from dashboard.utils import *
from chatMessenger import settings

logger = getLogger()


class BaseView(View):
    BUTTON_TEXT = 'Button Text'
    TEMPLATE_NAME = 'template_name.html'
    target = ''
    next_url = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def render_form(self, request, form, data=None):
        return render(request, self.TEMPLATE_NAME,  {
                                                'form': form,
                                                'data': data,
                                                'button_text': self.BUTTON_TEXT,
                                                'button_target': self.target,
                                                'next': self.next_url
                                                })

    def render_form_with_status(self, request, form, message='message'):
        data = {}
        messages.add_message(request, messages.SUCCESS, message)
        data['status'] = message
        return self.render_form(request, form, data)

    def render_form_with_error(self, request, form, message='Error message'):
        data = {}
        messages.add_message(request, messages.ERROR, message)
        data['error'] = message
        return self.render_form(request, form, data)


class LoginView(BaseView):
    TEMPLATE_NAME = 'login.html'
    BUTTON_TEXT = 'Login'
    next_url = '/'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = authenticate(username=username, password=password)
            except PermissionDenied as p:
                print(p)
            if user:
                login(request, user)
                nextUrl = getNextUrl(request)
                return HttpResponseRedirect(nextUrl)
            else:
                logger.debug('UnAuthorized user...')
                return self.render_form_with_error(request, form, 'login failed')


class SignupView(BaseView):
    TEMPLATE_NAME = 'signup.html'
    BUTTON_TEXT = 'Sign up'
    next_url = '/'

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)

        if form.is_valid():
           user = form.save()
           login(request, user)
           return self.render_form_with_status(request, form, "Sign up successfully..")
        else:
           return self.render_form(request, form)


def do_logout(request):
    logger.debug("Logging out...")
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)