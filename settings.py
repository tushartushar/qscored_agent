import os

SERVER = "https://www.qscored.com/api/upload/"
USERNAME = 'myemail@email.com' # specify your email here as your usename that you used to register on QScored platform

# workspace path is the base path where temp files are kept
WORKSPACE_PATH = r'C:\path\to\data'
DATA_PATH = r'D:\data\csvs'


CS_REPOS_PATH = os.path.join(WORKSPACE_PATH, r'cs_repos')  # All the C# repositories are in this path
JAVA_REPOS_PATH = os.path.join(WORKSPACE_PATH, r'java_repos') # All the Java repositories are in this path
CS_RESULTS_PATH = os.path.join(WORKSPACE_PATH, r'analyzed_repo', 'cs')
JAVA_RESULTS_PATH = os.path.join(WORKSPACE_PATH, r'analyzed_repo', 'java')
BATCH_FILES_FOLDER = os.path.join(WORKSPACE_PATH, r'batch_files')
ALL_REPOS_FILE_CS = os.path.join(DATA_PATH, r'complete_list_cs_1year.csv')
ALL_REPOS_FILE_JAVA = os.path.join(DATA_PATH, r'complete_list_java_1year.csv')
UPLOADED_PROJECTS_FILE = os.path.join(DATA_PATH, r'uploaded_projects.csv')
FAILED_PROJECTS_FILE = os.path.join(DATA_PATH, r'failed_projects.csv')

# Make sure to use the latest version always.
# Download and install Designite/DesigniteJava if not installed from designite-tools.com
DESIGNITE_CONSOLE_PATH = r'C:\Program Files (x86)\Designite\DesigniteConsole.exe'
DESIGNITEJAVA_CONSOLE_PATH = r'D:\DesigniteJava\DesigniteJava.jar'


PRJ_ACTIVE_DAYS = 30
# PROJECTS_TO_SKIP = 0 #c#
PROJECTS_TO_SKIP = 0 #java
PROJECTS_TO_SKIP_UPDATE_2 = 0
MAX_PROJECTS_TO_PROCESS = 0
LOGFILE = os.path.join(WORKSPACE_PATH, 'log.txt')
MODE = 'update'  # 'update' or 'new' -> it governs whether we are running it in update mode (meaning updating the already existing repos) or uploading new repos.
MAX_PROCESSES = 1 # based on your machine; analysis can be performed in many processes

# Get your API key from QScored platform; it will be used to upload the analysis report
API_KEY = ''
