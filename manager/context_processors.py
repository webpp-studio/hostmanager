from django.contrib.auth.models import User


def _can_add_virtualhost(request):
    '''
    Check if user can to add a new virtual host
    '''
    return request.user.has_perm('manager.add_virtualhost')


def auth(request): 
    '''
    Additional context processor for hostmanager
    '''
    response = {
        'user_can_add_vhost': _can_add_virtualhost(request),
        'can_delete': request.user.has_perm('manager.delete_virtualhost'),
        'can_change': request.user.has_perm('manager.change_virtualhost'),
    }
    return response
