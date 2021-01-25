import os
from file_utils import log
from settings import JAVA_RESULTS_PATH, LOGFILE, DESIGNITEJAVA_CONSOLE_PATH
import subprocess

def _build_java_project(dir_path, log_lock):
    print("Attempting compilation...")
    log(LOGFILE, "Attempting compilation...", log_lock)
    os.environ['JAVA_HOME']
    is_compiled = False
    pom_path = os.path.join(dir_path, 'pom.xml')
    if os.path.exists(pom_path):
        print("Found pom.xml")
        os.chdir(dir_path)
        proc = subprocess.Popen(
            # [r'C:\Program Files (x86)\apache-maven-3.6.2\bin\mvn.cmd', 'clean', 'install', '-DskipTests'])
            [r'mvn', 'clean', 'install', '-DskipTests'])
        proc.wait()
        is_compiled = True

    gradle_path = os.path.join(dir_path, "build.gradle")
    if os.path.exists(gradle_path):
        print("Found build.gradle")
        os.chdir(dir_path)
        # proc = subprocess.Popen([r'C:\Program Files\Gradle\gradle-5.6.2\bin\gradle.bat', 'compileJava'])
        proc = subprocess.Popen([r'gradle', 'compileJava'])
        proc.wait()
        is_compiled = True
    if not is_compiled:
        print("Did not compile")


def _run_designite_java(folder_path, out_path, log_lock):
    print("Analyzing ...")
    log(LOGFILE, "Analyzing ...", log_lock)
    proc = subprocess.Popen(
        ["java", "-jar", DESIGNITEJAVA_CONSOLE_PATH, "-i", folder_path, "-o", out_path, "-f", "XML"])
    proc.wait()
    print("done analyzing.")
    log(LOGFILE, "done analyzing.", log_lock)


def _get_xml_file(out_path, potential_xml_file):
    if not os.path.isdir(out_path):
        return '', ''
    cur_file = os.path.join(out_path, potential_xml_file)
    if os.path.isfile(cur_file):
        return potential_xml_file, cur_file
    for item in os.listdir(out_path):
        if item.startswith('.'):
            continue
        if item.endswith('.xml'):
            return item, os.path.join(out_path, item)
    return '', ''


def analyze_java_repo(folder_path, folder_name, log_lock, is_update):
    potential_xml_file = folder_name + '.xml'
    out_path = os.path.join(JAVA_RESULTS_PATH, folder_name)
    xml_file, xml_path = _get_xml_file(out_path, potential_xml_file)

    if os.path.isfile(xml_path) and not is_update:
        print("already exists; skipping ...")
        log(LOGFILE, "already exists; skipping ...", log_lock)
        return xml_path, xml_file
    _build_java_project(folder_path, log_lock)
    _run_designite_java(folder_path, out_path, log_lock)
    xml_file, xml_path = _get_xml_file(out_path, potential_xml_file)
    return xml_path, xml_file
