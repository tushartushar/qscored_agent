import os
import subprocess

from file_utils import log
from settings import CS_REPOS_PATH, JAVA_REPOS_PATH, LOGFILE


def download_repo(line, lang, log_lock, is_update):
    repo_path = CS_REPOS_PATH if lang == 'cs' else JAVA_REPOS_PATH
    repo_fullname = line.strip('\n')
    project_name = None
    project_url = None
    if not repo_fullname == "":
        tokens = repo_fullname.split('/')
        project_name = tokens[1] if len(tokens) > 1 else repo_fullname
        project_url = "https://github.com/" + repo_fullname
        folder_name = repo_fullname.replace("/", "_")
        folder_path_new = os.path.join(repo_path, folder_name)

        if (not os.path.exists(folder_path_new)) or is_update:
            _download_with_url(repo_fullname, lang, log_lock)
        else:
            print(folder_name + " already exists. skipping ...")
            log(LOGFILE, folder_name + " already exists. skipping ...", log_lock)
    return project_name, project_url


def _download_with_url(repo_fullname, lang, log_lock):
    repo_path = CS_REPOS_PATH if lang == 'cs' else JAVA_REPOS_PATH

    repo_url = "https://github.com/" + repo_fullname + ".git"
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    os.chdir(repo_path)
    folder_name = repo_fullname.replace("/", "_")
    print("folder path: " + folder_name)
    if not os.path.isdir(os.path.join(repo_path, folder_name)):
        print("cloning... " + repo_url)
        log(LOGFILE, "cloning: " + repo_url, log_lock)
        os.mkdir(folder_name)
        try:
            # call(["git", "clone", fullRepoName, folderName])
            # if you want to clone only the current snapshot otherwise use the above line
            # subprocess.call(["git", "clone", "--depth=1", repo_url, folder_name])
            subprocess.check_call(["git", "clone", "--depth=1", repo_url, folder_name], timeout=60)
            # cmd = "git clone --depth=1" + ' ' + repo_url + ' ' + folder_name
            # check_output(cmd, stderr=STDOUT, timeout=60, shell=True)
        except Exception as ex:
            log(LOGFILE, "Exception occurred while cloning", log_lock)
            print("Exception occurred!!" + str(ex))
            return
    print("cloning done.")
