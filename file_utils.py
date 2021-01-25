import datetime
import os
import shutil
import stat
import time
import xml.etree.ElementTree as ET

from pydriller import RepositoryMining

from settings import LOGFILE, UPLOADED_PROJECTS_FILE, JAVA_REPOS_PATH, CS_REPOS_PATH, \
    FAILED_PROJECTS_FILE, PRJ_ACTIVE_DAYS


def get_uploaded_project_lists(uploaded_projects_file):
    return _get_project_lists(uploaded_projects_file, 'uploaded')


def _get_project_lists(_file, mode):
    assert (mode == 'failed' or mode == 'uploaded')
    filepath = _file
    cs_list = []
    java_list = []
    try:
        with open(filepath, 'rt', errors='ignore', encoding='UTF8') as file:
            for line in file.readlines():
                tokens = line.strip('\n').split(',')
                if len(tokens) > 1:
                    if tokens[1] == 'cs':
                        cs_list.append(tokens[0])
                    if tokens[1] == 'java':
                        java_list.append(tokens[0])
    except:
        print("Exception occurred while retrieving project list")
    return cs_list, java_list


def get_failed_project_lists(failed_projects_file):
    return _get_project_lists(failed_projects_file, 'failed')


def log(file_name, line, log_lock):
    log_lock.acquire()
    f = open(file_name, "a", errors='ignore')
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    f.close()
    log_lock.release()


def get_LOC_from_xml(filepath, log_lock):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        loc = root.find('./Solution/LOC')
        if loc is not None:
            return int(loc.text)
        return 0
    except Exception as ex:
        log(LOGFILE, "Exception occurred while getting loc from xml: " + str(ex), log_lock)
        return 0


def is_project_too_small(xml_output_filepath, log_lock):
    loc = get_LOC_from_xml(xml_output_filepath, log_lock)
    if loc > 1000:
        return False
    return True


def write_project_uploaded(line, lock, lang='cs'):
    lock.acquire()
    f = open(UPLOADED_PROJECTS_FILE, "a", errors='ignore')
    f.write(line + "," + lang + "\n")
    f.close()
    lock.release()


def _delete_repo(line, lang, log_lock):
    print("deleting " + line)
    log(LOGFILE, 'deleting ' + line, log_lock)
    try:
        repo_path = CS_REPOS_PATH if lang == 'cs' else JAVA_REPOS_PATH
        repo_fullname = line.strip('\n')
        if not repo_fullname == "":
            folder_name = repo_fullname.replace("/", "_")
            folder_path_new = os.path.join(repo_path, folder_name)

            if os.path.exists(folder_path_new):
                shutil.rmtree(folder_path_new, onerror=err_handler)
            else:
                print(folder_name + " not found. skipping ...")
                log(LOGFILE, folder_name + " not found. skipping ...", log_lock)
    except Exception as ex:
        print('Exception occurred while deleting repo')
        log(LOGFILE, 'Exception occurred while deleting repo', log_lock)


def err_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def write_project_failed(line, lang):
    f = open(FAILED_PROJECTS_FILE, "a", errors='ignore')
    f.write(line + "," + lang + "\n")
    f.close()


def _analysis_failed(line, lang, lock, log_lock):
    print("Could not find the analysis report file; possibly analysis failed.")
    log(LOGFILE, "Could not find the analysis report file; possibly analysis failed.", log_lock)
    lock.acquire()
    write_project_failed(line, lang)
    lock.release()


def is_project_updated(prj, lang):
    return is_project_active_by_days(prj, lang, PRJ_ACTIVE_DAYS)


def is_project_active(prj, lang):
    return is_project_active_by_days(prj, lang, 365)


def is_project_active_by_days(prj, lang, days):
    repo_path = CS_REPOS_PATH if lang == 'cs' else JAVA_REPOS_PATH
    repo_full_path = os.path.join(repo_path, prj.replace("/", "_"))
    try:
        for _ in RepositoryMining(repo_full_path,
                                  since=datetime.datetime.today() - datetime.timedelta(days=days)).traverse_commits():
            return True
    except Exception as ex:
        print(ex)
    return False
