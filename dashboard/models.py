# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from security.models import ChatUser
from django.utils.translation import ugettext_lazy as _


# users messages model
class Message(models.Model):
    mid = models.AutoField(verbose_name='mid',
                             primary_key=True)
    chatuser = models.ForeignKey(ChatUser, related_name="chatuser", on_delete=models.CASCADE)
    frienduser = models.ForeignKey(ChatUser, related_name="frienduser", on_delete=models.CASCADE)
    message = models.CharField(_('Message'),
                               max_length=350,
                               null=True)
    messdate = models.DateTimeField(verbose_name='Message datetime',
                                    auto_now_add=True)

    class Meta:
        ordering = ['messdate']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __unicode__(self):
        return str(self.message)[0:20]

