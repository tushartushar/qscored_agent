import datetime
import os

import requests

from file_utils import log, write_project_uploaded, is_project_too_small, _analysis_failed
from settings import USERNAME, SERVER, LOGFILE, API_KEY


def _get_headers(link=''):
    headers = {
        'Content-Type': 'application/xml',
        'username': USERNAME,
        'repository-link': link,
        'Authorization': 'Token ' + API_KEY
    }
    return headers


def _upload(lang, line, link, project_name, xml_output_file, xml_output_filepath, file_lock, log_lock, is_update):
    print("Uploading ...")
    dt = datetime.datetime.today()
    version = str(dt.year) + '.' + str(dt.month) + '.' + str(dt.day)
    with open(xml_output_filepath, 'rb') as fp:
        try:
            response = requests.put(
                url=SERVER + xml_output_file + "?version=" + version + "&project_name=" + project_name + "&is_open_access=True",
                files={'file': fp, },
                headers=_get_headers(link),
            )
            log(LOGFILE, "upload response: " + str(response.text), log_lock)
            print("upload response: " + str(response.text))
            if response.status_code == 200 and not is_update:
                write_project_uploaded(line, file_lock, lang)
            if response.status_code == 200:
                return True
        except Exception as ex:
            log(LOGFILE, "exception occurred while uploading .. " + str(ex), log_lock)
            print("exception occurred while uploading .. " + str(ex))
    return False


def upload(lang, line, link, project_name, xml_output_file, xml_output_filepath, file_lock, log_lock, is_update):
    if xml_output_file is not None:
        if os.path.isfile(xml_output_filepath):
            if is_project_too_small(xml_output_filepath, log_lock):
                print("The analyzed project is too small; skipping...")
                log(LOGFILE, "The analyzed project is too small; skipping...", log_lock)
            else:
                return _upload(lang, line, link, project_name, xml_output_file, xml_output_filepath, file_lock, log_lock,
                               is_update=is_update)
        else:
            _analysis_failed(line, lang, file_lock, log_lock)
    else:
        _analysis_failed(line, lang, file_lock, log_lock)
    return False
