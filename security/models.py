# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from dashboard.utils import getLogger
from django.utils.translation import ugettext_lazy as _

logger = getLogger()


class ChatUserAuthBackend(object):

    def authentication(self, username, password):
        logger.debug("authenticating user......")
        manager = ChatMessUserManager()
        try:
            ch_user = manager.get_user(username)
            if ch_user.check_password(password) and manager.user_can_authenticate(ch_user):
                logger.debug('Authenticated user: %s' % username)
                return ch_user
        except Exception as e:
            logger.debug(e)
        return None

    def get_user(self, user_id):
        try:
            ch_user = ChatUser.objects.get(id=user_id)
            return ch_user
        except Exception as e:
            logger.debug(e)
        return None


class ChatMessUserManager(BaseUserManager):

    def get_user(self, username):
        try:
            ch_user = ChatUser.objects.get(username)
            return ch_user
        except Exception as e:
            logger.debug(e)
        return None

    def create_user(self, username, password, first_name, last_name):
        ch_user = self.model(username=username,
                             first_name=first_name,
                             last_name=last_name)
        ch_user.set_password(password)
        ch_user.save(using=self._db)
        return ch_user

    def create_superuser(self, username, password, first_name, last_name):
        ch_user = self.create_user(username, password, first_name, last_name)
        ch_user.is_active = True
        ch_user.is_active = True
        ch_user.is_staff = True
        ch_user.save(using=self._db)
        return ch_user


class ChatUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Username'),
                                max_length=30, unique=True)
    first_name = models.CharField(_('Firstname'),
                                  max_length=20, null=True)
    last_name = models.CharField(_('Lastname'),
                                 max_length=20, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = ChatMessUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('ChatUser')
        verbose_name_plural = _('ChatUsers')

    def __init__(self, *args, **kwargs):
        super(ChatUser, self).__init__(*args, **kwargs)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True