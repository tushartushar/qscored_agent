# QScored agent
QScored agent/client have scripts to select repositories using GraphQL, download the selected repositories from GitHub, analyze them using Designite and DesigniteJava,
and upload the code analysis reports to QScored server.

The sequence is as follows:
- repo_selector.py (to select required repositories to download and analyze)
- agent.py (to download and analyze the repositories and finally upload it to QScored server); first set the parameters in settings.py file
