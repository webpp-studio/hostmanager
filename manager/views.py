#! -*- coding: utf-8 -*-

import os
import re
import sys
import subprocess
import commands

from  django.conf import settings

from django import http
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q

from manager import models
from manager.models import VirtualHost
from manager.forms import VirtualHostForm
from manager.create_site import create_site, delete_site


def object_list(request, queryset, template_name, context):
    paginator = Paginator(queryset, settings.HOSTMANAGER_PAGINATE_BY)
    try:
        page = paginator.page(int(request.GET.get("page", "1")))
    except (InvalidPage, ValueError):
        raise http.Http404()

    context.update({
        "object_list": page.object_list,
        "paginator": paginator,
        "page": page,
    })
    return render(request, template_name, context)

@login_required
def index(request):
    return render(request, 'manager/index.html', {
        'sites_enabled': VirtualHost.enabled.all(),
        'sites_disabled': VirtualHost.disabled.all(),
        'create_site_form': VirtualHostForm(),
    })

@login_required
def site_list(request):
    filterString = request.GET.get("filter", "").strip()
    if filterString:
        sites = VirtualHost.objects.filter(
            Q(domain__icontains=filterString) |
            Q(site_name__icontains=filterString)).order_by('-created')
    else:
        sites = VirtualHost.objects.all().order_by('-created')
    return object_list(request, sites, 'manager/site_list.html', {
                           "filterString": filterString,
                       })

@login_required
def add_site(request):
    if request.method == 'POST':
        response = {'success': 0, 'data': 'Unknown error'}
        if request.user.has_perm('manager.add_virtualhost'):
            form = VirtualHostForm(request.POST)
            if form.is_valid():
                if not re.match(r'^[a-z\d\-\.]{2,}\.[a-z]{2,}$', form.cleaned_data['domain']):
                    response['success'] = 0
                    response['data'] = 'Incorrect domain name'
                else:
                    success, data = create_site(form.cleaned_data['domain'].encode('utf-8'))
                    if success:
                        obj = models.VirtualHost(
                            site_name=form.cleaned_data['name'],
                            domain=form.cleaned_data['domain'],
                            is_active=form.cleaned_data['is_active'],
                            username = data['system']['user'],
                            password = data['system']['passwd'],
                            db_password = data['db']['passwd'],
                        )
                        obj.save()
                        data["host"] = request.META['SERVER_NAME'],
                        response['success'] = 1
                        response['data'] = data
                        with open(settings.BACKUP_DATABASE_LIST, 'a+') as f:
                            f.write(data['system']['user'] + "\n")
                        f.closed
                    else:
                        response['success'] = 0
                        response['data'] = data
        else:
            response['success'] = 0
            response['data'] = 'Permission denied'
        return http.HttpResponse(json.dumps(response), mimetype='application/json')
    else:
        # Request method is GET
        return render(request, 'manager/add_form.html', {
            'create_site_form': VirtualHostForm(),
        })


@login_required
def get_site_info(request, host_id):
    host = get_object_or_404(models.VirtualHost, pk=host_id)
    response = {'success': 1, 'data': {
        'id': host.pk,
        'site_name': host.site_name,
        'domain': host.domain,
        'is_active': int(host.is_active),
        'description': host.description or "",
        "host": request.META['SERVER_NAME'],
    }}
    if request.GET.get('private'):
        if request.user.has_perm('manager.add_virtualhost'):
            response['data']['username'] = host.username
            response['data']['password'] = host.password
            response['data']['db_password'] = host.db_password
        else:
            response = {'success': 0, 'data': {'err_msg': 'Permission denied'}}

    return http.HttpResponse(json.dumps(response), mimetype='application/json')

@login_required
def change_host(request):
    pass

@require_http_methods(('POST', 'GET'))
@login_required
def delete_host(request, host_id):
    host = get_object_or_404(models.VirtualHost, pk=host_id)
    if request.POST.get("domain", "") != host.domain:
        response = {
            'success': 0,
            'data': {'err_msg': u"Вы ввели неверное имя домена для подтверждения."}
        }
        return http.HttpResponse(json.dumps(response))
    if request.user.has_perm('manager.delete_virtualhost'):
        success, data = delete_site(host.domain)
        if success:
            host.delete()
            response = {'success': 1};
        else:
            response = {'success': 0, 'data': data};
    else:
        response = {'success': 0, 'data': {'err_msg': "Permission denied"}}
        return http.HttpResponseForbidden(json.dumps(response))
    return http.HttpResponse(json.dumps(response))