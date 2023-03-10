#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
from datetime import datetime
from fabric.api import env, put, run
import os

env.user = 'ubuntu'
env.hosts = ['3.90.0.75', '54.175.29.140']

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    try:
        if not os.path.isdir("versions"):
            os.makedirs("versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Distribute archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive_name = archive_path.split("/")[-1]
        archive_dir = "/data/web_static/releases/" + archive_name[:-4]
        run("mkdir -p {}".format(archive_dir))
        run("tar -xzf /tmp/{} -C {}"
            .format(archive_name, archive_dir))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}".format(archive_dir, archive_dir))
        run("rm -rf {}/web_static".format(archive_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_dir))
        return True
    except:
        return False

def deploy():
    """Create and distribute archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
