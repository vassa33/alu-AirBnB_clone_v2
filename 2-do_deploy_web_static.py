#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
import re
from datetime import datetime


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
    """Distributes an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = match.group(0)
    result = put(archive_path, "/tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    # Uncompress the archive to the folder

    result = run(
        "mkdir -p /data/web_static/releases/{}/".format(archive_filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False

    # Delete the archive from the web server
    result = run("rm /tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static"
                 .format(archive_filename))
    if result.failed:
        return False

    # Delete the symbolic link /data/web_static/current from the web server
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False

    #  Create a new the symbolic link
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(archive_filename))
    if result.failed:
        return False

    return True
