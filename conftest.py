import os

_original_cwd = None
_original_sdl = None

def pytest_configure(config):
    global _original_cwd, _original_sdl

    # Set up headless SDL driver so pygame works without a real display
    _original_sdl = os.environ.get("SDL_VIDEODRIVER")
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    # Patch pygame.sysfont to handle non-string registry values on Windows.
    # Some registry entries returned by _winreg.EnumValue are ints, which
    # causes os.path.splitext() to raise TypeError.  This makes SysFont()
    # fail for every widget that uses fonts.
    import pygame.sysfont as _sf
    _orig_splitext = _sf.splitext

    def _safe_splitext(path):
        if isinstance(path, (str, bytes, os.PathLike)):
            return _orig_splitext(path)
        return ("", "")

    _sf.splitext = _safe_splitext

    _original_cwd = os.getcwd()

    if os.path.isdir("pyhelper"):
        os.chdir("pyhelper")

def pytest_sessionfinish(session, exitstatus):
    if _original_cwd and os.getcwd() != _original_cwd:
        os.chdir(_original_cwd)
    if _original_sdl is not None:
        os.environ["SDL_VIDEODRIVER"] = _original_sdl
    elif "SDL_VIDEODRIVER" in os.environ:
        del os.environ["SDL_VIDEODRIVER"]