# This script is the starting point for the QScored agent after the repos are selected
# First configure the parameters in settings file

from agent_worker import process, process_updated_repos
from file_utils import get_failed_project_lists, \
    get_uploaded_project_lists
from settings import UPLOADED_PROJECTS_FILE, FAILED_PROJECTS_FILE, MODE, ALL_REPOS_FILE_CS, \
    ALL_REPOS_FILE_JAVA, CS_REPOS_PATH, JAVA_REPOS_PATH, CS_RESULTS_PATH, JAVA_RESULTS_PATH, BATCH_FILES_FOLDER
import os


def _create_workspace_folders():
    if not os.path.isdir(CS_REPOS_PATH):
        os.makedirs(CS_REPOS_PATH)
    if not os.path.isdir(JAVA_REPOS_PATH):
        os.makedirs(JAVA_REPOS_PATH)
    if not os.path.isdir(CS_RESULTS_PATH):
        os.makedirs(CS_RESULTS_PATH)
    if not os.path.isdir(JAVA_RESULTS_PATH):
        os.makedirs(JAVA_RESULTS_PATH)
    if not os.path.isdir(BATCH_FILES_FOLDER):
        os.makedirs(BATCH_FILES_FOLDER)


if __name__ == "__main__":
    _create_workspace_folders()
    uploaded_prj_cs, uploaded_prj_java = get_uploaded_project_lists(UPLOADED_PROJECTS_FILE)
    failed_prj_cs, failed_prj_java = get_failed_project_lists(FAILED_PROJECTS_FILE)
    if MODE == 'new':
        # process(ALL_REPOS_FILE_CS, uploaded_prj_cs, failed_prj_cs, 'cs')
        process(ALL_REPOS_FILE_JAVA, uploaded_prj_java, failed_prj_java, 'java')
    if MODE == 'update':
        process_updated_repos('java')
