from datetime import datetime
from fabric.api import local


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

