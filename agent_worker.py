import multiprocessing
import os
import threading
from functools import partial
import shutil

from analyzer_cs import analyze_cs_repo
from analyzer_java import analyze_java_repo
from downloader import download_repo
from file_utils import get_LOC_from_xml, log, _delete_repo, is_project_updated, is_project_active
from settings import MAX_PROCESSES, MAX_PROJECTS_TO_PROCESS, LOGFILE, \
    CS_REPOS_PATH, JAVA_REPOS_PATH, UPLOADED_PROJECTS_FILE, PROJECTS_TO_SKIP_UPDATE_2, PROJECTS_TO_SKIP
from uploader import upload
from pathlib import Path


def process(all_repos_file, uploaded_prj_list, failed_prj_list, lang):
    assert (lang == 'cs' or lang == 'java')
    file = open(all_repos_file, 'rt', errors='ignore', encoding='UTF8')
    i = PROJECTS_TO_SKIP - 1 if PROJECTS_TO_SKIP > 0 else 0

    all_lines = file.readlines()[PROJECTS_TO_SKIP - 1:]
    manager = multiprocessing.Manager()
    file_lock = manager.Lock()
    log_lock = manager.Lock()
    shared_dict = manager.dict()
    shared_dict['i'] = i
    shared_dict['uploaded_prj_list'] = uploaded_prj_list
    shared_dict['failed_prj_list'] = failed_prj_list
    shared_dict['lang'] = lang
    shared_dict['file_lock'] = file_lock
    shared_dict['log_lock'] = log_lock

    process_pool = multiprocessing.Pool(MAX_PROCESSES)
    _process_func = partial(_process, shared_dict)
    process_pool.map(_process_func, all_lines)
    # process_pool.close()
    # process_pool.join()


def _delete_maven_gradle_libs():
    try:
        shutil.rmtree(os.path.join(str(Path.home()), '.m2'), ignore_errors=True)
        shutil.rmtree(os.path.join(str(Path.home()), '.gradle'), ignore_errors=True)
    except:
        pass


def _process(my_dict, line):
    uploaded_prj_list = my_dict['uploaded_prj_list']
    failed_prj_list = my_dict['failed_prj_list']
    lang = my_dict['lang']
    file_lock = my_dict['file_lock']
    log_lock = my_dict['log_lock']
    cur_repo_no = my_dict['i'] + 1
    my_dict['i'] = cur_repo_no

    # if cur_repo_no <= PROJECTS_TO_SKIP:
    #     print("skipping ...")
    #     return
    line = line.strip('\n')
    if line in uploaded_prj_list:
        print("repo is already analyzed and uploaded ... skipping.")
        return
    if line in failed_prj_list:
        print("repo is already analyzed and failed ... skipping.")
        return
    log(LOGFILE, "processing repo: " + str(cur_repo_no), log_lock)
    project_name, link = download_repo(line, lang, log_lock, is_update=False)
    if is_project_active(line, lang):
        xml_output_file, xml_output_filepath = _analyze_project(cur_repo_no, lang, line, log_lock, is_update=False)
        upload_status = upload(lang, line, link, project_name, xml_output_file, xml_output_filepath, file_lock,
                               log_lock, is_update=False)
        if upload_status:
            loc = get_LOC_from_xml(xml_output_filepath, log_lock)
    else:
        print(str(cur_repo_no) + ": project not active ... skipping.")
        log(LOGFILE, "project not active ... skipping.", log_lock)
    _delete_repo(line, lang, log_lock)
    if cur_repo_no % 100 == 0:
        _delete_maven_gradle_libs()
    print("Done with " + line)
    # if cur_repo_no > MAX_PROJECTS_TO_PROCESS:
    #     return


def process_updated_repos(process_lang='all'):
    file = open(UPLOADED_PROJECTS_FILE, 'rt', errors='ignore', encoding='UTF8')
    i = 0
    file_lock = threading.Lock()
    log_lock = threading.Lock()
    for line in file.readlines():
        i += 1
        if i < PROJECTS_TO_SKIP_UPDATE_2:
            print(str(i) + ' skipping ...')
            log(LOGFILE, str(i) + " skipping ...", log_lock)
            continue
        else:
            print('processing ' + str(i) + ':' + line)
            log(LOGFILE, 'processing ' + str(i) + ':' + line, log_lock)
        line = line.strip('\n')
        prj_token, lang = _parse_line(line)
        if not process_lang == 'all':
            if not lang == process_lang:
                continue
        project_name, link = download_repo(prj_token, lang, log_lock, is_update=True)
        if is_project_updated(prj_token, lang):
            xml_output_file, xml_output_filepath = _analyze_project(i, lang, prj_token, log_lock, is_update=True)
            upload(lang, line, link, project_name, xml_output_file, xml_output_filepath, file_lock, log_lock,
                   is_update=True)
        else:
            print("project did not update; skipping ...")
            log(LOGFILE, "project did not update; skipping ...", log_lock)
        _delete_repo(prj_token, lang, log_lock)
        print("Done with " + prj_token)


def _parse_line(line):
    line = line.strip('\n')
    tokens = line.split(',')
    if len(tokens) > 1:
        return tokens[0], tokens[1]
    else:
        return '', ''


def _analyze_project(i, lang, prj_token, log_lock, is_update):
    print("Processing " + str(i) + " : " + prj_token)
    folder_name = prj_token.replace("/", "_")
    if lang == 'cs':
        xml_output_filepath, xml_output_file = analyze_cs_repo(os.path.join(CS_REPOS_PATH, folder_name),
                                                               folder_name, log_lock, is_update)
    else:
        xml_output_filepath, xml_output_file = analyze_java_repo(os.path.join(JAVA_REPOS_PATH, folder_name),
                                                                 folder_name, log_lock, is_update)
    print("Done analyzing " + prj_token)
    return xml_output_file, xml_output_filepath
