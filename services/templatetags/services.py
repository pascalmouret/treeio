# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext
from treeio.messaging.models import MessageStream, Message

import datetime

register = template.Library()

@contextfunction 
def services_ticket_list(context, tickets, skip_group=False,
                         tick_group=None, nomass=False, group_by=None,
                         by_assigned=False, by_status=False, noheader=False):
    "Print a list of tickets"
    request = context['request']
    
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']
    
    return Markup(render_to_string('services/tags/ticket_list',
                               {'tickets': tickets,
                                'tick_group': tick_group,
                                'skip_group': skip_group,
                                'by_assigned': by_assigned,
                                'by_status': by_status,
                                'group_by': group_by,
                                'noheader': noheader,
                                'nomass': nomass},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(services_ticket_list)

@contextfunction 
def services_service_list(context, services, skip_group=False):
    "Print a list of services"
    request = context['request']
    
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']
    
    return Markup(render_to_string('services/tags/service_list',
                               {'services': services, 'skip_group': skip_group},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(services_service_list)

@contextfunction 
def services_queue_list(context, queues, skip_group=False):
    "Print a list of queues"
    request = context['request']
    
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']
    
    return Markup(render_to_string('services/tags/queue_list',
                               {'queues': queues, 'skip_group': skip_group},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(services_queue_list)

@contextfunction
def services_message_mail(context, record):
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    is_mail = False
    delta = datetime.timedelta(seconds=5)
    try:
        msg = Message.objects.get(body=record.body, author=record.sender,
                                  date_created__range=(record.date_created-delta, record.date_created+delta))
        is_mail = msg.is_mail
    except:
        pass

    return Markup(render_to_string('services/tags/mail_marker',
                               {'is_mail': is_mail},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(services_message_mail)