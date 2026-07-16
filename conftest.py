import os

_original_cwd = None

def pytest_configure(config):
    global _original_cwd
    _original_cwd = os.getcwd()

    if os.path.isdir("pyhelper"):
        os.chdir("pyhelper")

def pytest_sessionfinish(session, exitstatus):
    if _original_cwd and os.getcwd() != _original_cwd:
        os.chdir(_original_cwd)