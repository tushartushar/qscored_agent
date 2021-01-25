import os
from glob import glob

from file_utils import log
from settings import LOGFILE, CS_RESULTS_PATH, DESIGNITE_CONSOLE_PATH, BATCH_FILES_FOLDER
import subprocess

def _get_csharp_solution_paths(folder):
    if not os.path.exists(folder):
        return []
    return [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.sln'))]


def _get_all_csharp_projects_paths(folder, log_lock):
    prj_list = []
    if not os.path.exists(folder):
        return prj_list

    try:
        result = [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.csproj'))]
        for prj in result:
            if not _get_repo_name(prj).lower().__contains__("test"):
                prj_list.append(prj)
    except:
        print('Exception occurred while searching projects.')
        log(LOGFILE, 'Exception occurred while searching projects.', log_lock)
    return prj_list


def _get_repo_name(folder):
    start_index = folder.rfind(os.pathsep)
    if start_index < 0:
        start_index = 0
    if start_index + 1 < len(folder):
        return folder[start_index + 1:]
    else:
        return folder


def _write_batch_file(repo_name, project_paths, batch_files_folder, is_update):
    if not os.path.exists(batch_files_folder):
        os.makedirs(batch_files_folder)
    batch_file_name = os.path.join(batch_files_folder, repo_name + ".batch")
    if os.path.exists(batch_file_name) and not is_update:
        return batch_file_name
    try:
        with open(batch_file_name, "w", errors='ignore') as file:
            file.write("[Projects]\n")
            for line in project_paths:
                file.write(line + "\n")
    except:
        print("Error writing batch file: " + batch_file_name)
    return batch_file_name


def _analyze_projects(batch_file_path, repo_name, result_folder_base, designite_console_path, log_lock,
                      is_update):
    xml_file = repo_name + ".xml"
    xml_path = os.path.join(result_folder_base, xml_file)
    if os.path.isfile(xml_path) and not is_update:
        print("already exists; skipping ...")
        log(LOGFILE, "already exists; skipping ...", log_lock)
        return xml_path, xml_file
    print("analyzing " + str(repo_name) + " ...")
    log(LOGFILE, "analyzing ...", log_lock)
    try:
        if not os.path.isdir(result_folder_base):
            os.makedirs(result_folder_base)
        # subprocess.call([designite_console_path, batch_file_path, "-X", xml_path])
        print(subprocess.check_output([designite_console_path, "-i", batch_file_path, "-x", "-o", xml_path], shell=True))
    except Exception as ex:
        print("Exception occurred: " + str(ex))
    return xml_path, xml_file


def analyze_cs_repo(folder_path, folder, log_lock, is_update):
    print("Searching " + folder)
    project_paths = _get_all_csharp_projects_paths(folder_path, log_lock)
    if len(project_paths) > 0:
        batch_file_path = _write_batch_file(folder, project_paths, BATCH_FILES_FOLDER, is_update)
        path, file = _analyze_projects(batch_file_path, folder, CS_RESULTS_PATH, DESIGNITE_CONSOLE_PATH, log_lock, is_update)
        print("Done with " + folder)
        return path, file
    else:
        print("No projects found.")
        return None, None
