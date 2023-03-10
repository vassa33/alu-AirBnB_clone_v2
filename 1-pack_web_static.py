#!/usr/bin/python3
"""Compress before sending"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a compressed archive of the web_static directory."""
    local("mkdir -p versions")

    # Create the filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "web_static_{}.tgz".format(timestamp)

    # Compress the web_static directory to the archive file
    result = local("tar -cvzf versions/{} web_static/".format(filename))

    # Return the archive path if the compression was successful
    if result.succeeded:
        return "versions/{}".format(filename)
    else:
        return None
