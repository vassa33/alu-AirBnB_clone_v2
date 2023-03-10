#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import datetime


env.user = 'ubuntu'
env.hosts = ['3.90.0.75', '54.175.29.140']

def do_pack():
    """Create a compressed archive of the web_static directory."""
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")
    # Create the filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"web_static_{timestamp}.tgz"
    # Compress the web_static directory to the archive file
    result = local(f"tar -cvzf versions/{filename} web_static/")
    # Return the archive path if the compression was successful, otherwise return None
    if result.succeeded:
        return f"versions/{filename}"
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        no_ext = os.path.splitext(archive_name)[0]

        # Upload archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create directory to uncompress the archive
        run("sudo mkdir -p /data/web_static/releases/{}".format(no_ext))

        # Uncompress archive into the folder created
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, no_ext))

        # Delete archive from web server
        run("sudo rm /tmp/{}".format(archive_name))

        # Move uncompressed files to its own folder
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(no_ext, no_ext))

        # Remove original web_static folder
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(no_ext))

        # Delete symbolic link
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link
        run("sudo ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(no_ext))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
