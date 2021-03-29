from django.conf import settings
import os
import git
from celery.decorators import task

def create_dir(env):
    login = env.email.replace('@','---')
    path = os.path.join(settings.WORK_DIR,login)
    os.mkdir(path)

@task()
def git_clone(env_id):
    from .models import Env
    env = Env.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR,env.email.replace('@','---'))
    git.Git(path).clone(settings.GIT_URL)


def nginx_conf(env_id):    
    from .models import Env
    env = Env.objects.get(pk=env_id)
    path = os.path.join(settings.BASE_DIR, 'tpl', 'nginx_vhost.conf')
    with open(path, 'r') as f:
        tpl = f.read()
    tpl = tpl.replace('%media_path%', settings.MEDIA_PATH)
    sname = '%s.%s' % (env.email.replace('@', '---'), settings.DOMAIN)
    tpl = tpl.replace('%server_name%', sname)
    tpl = tpl.replace('%port%', str(env.port))
    conf_path = os.path.join(
            settings.NGINX_PATH, env.email.replace('@', '---'))
    with open(conf_path, 'w+') as f:
        f.write(tpl)