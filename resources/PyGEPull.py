import os
import stat
import sys


def pull_changes(dst_dir="PyGE"):
    """
    Pulls the latest version of the PyGE repository
    :param dst_dir: the destination to pull the source to. NOTE: This MUST be in a directory called "PyGE" beside your main script
    """

    # check if the destination directory exists
    if os.path.isdir(dst_dir):

        # if it does, clear it (this way results in less chance of permission problems)
        for root, dirs, files in os.walk(dst_dir, topdown=False):
            for name in files:
                # for each file, set the permission level to be written by the file owner, and delete it
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)

            for name in dirs:
                # remove each subdirectory too
                os.rmdir(os.path.join(root, name))
    else:
        # if the destination does not exist, create it
        os.mkdir(dst_dir)

    # clone the repository to the specified destination
    os.system('git clone https://github.com/CPSuperstore-Inc/PyGE.git ' + dst_dir)


if __name__ == "__main__":
    # if this module is run, use the command-line arguments to set properties
    dst = "PyGE"

    # if "dst" has been set, get the argument value (the next arg) to pass into the function
    if "dst" in sys.argv:
        dst = sys.argv[sys.argv.index("dst") + 1]

    # pull the changes
    pull_changes(dst)
