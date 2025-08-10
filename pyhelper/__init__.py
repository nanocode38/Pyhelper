# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#   ___      _  _     _
#  | _ \_  _| || |___| |_ __  ___ _ _
#  |  _/ || | __ / -_) | '_ \/ -_) '_|
#  |_|  \_, |_||_\___|_| .__/\___|_|
#       |__/           |_|

#
# Pyhelper - Packages that provide more helper tools for Python
# Copyright (C) 2023-2024   Gao Yuhan(高宇涵)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library Public
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# DON'T EVEN HAVE A PERMIT TOO!
#
# Gao Yuhan(高宇涵)
# nanocode38@88.com
# nanocode38

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PYHELPER--PyHelper--pyhelper
# Pyhelper - Packages that provide more helper tools for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.
-----------------------------------------------------
Pyhelper is a set of packages designed to make writing Python programs better.
It is built on Python 3.13 and contains a rich set of classes and functions.
The package is highly portable and works perfectly on Windows
Python packages containing all sorts of useful data structures, functions,
classes, etc. that Python doesn't have

Because pypi is duplicated, this library on pypi is called nanocode38-pyhelper, but please still use pyhelper
after downloading and importing.

applied environment: Microsoft Windows 11, Python 3.8+
Copyright (C)
By nanocode38 nanocode38@88.com
2025.03.02
"""
import abc
import functools
import multiprocessing
import os
import platform
import subprocess
import sys
from abc import ABC
import inspect
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Generator

__author__ = "nanocode38"
__version__ = "3.0.0"
__all__ = [
    "get_version",
    "file_reopen",
    "chdir",
    "join_startup",
    "system",
    "Singleton",
    "timer",
    "tail_recursive_optimization",
    "gamehelpers",
    "color",
    "mathhelper",
    "tkhelper",
    "random",
    "namespace",
    "readonly_attr"
]


if __name__ != "__main__":
    print(f"PyHelper {__version__}", end=" ")
    os_type = platform.system()
    if os_type == "Windows":
        print("(Microsoft Windows,", end=" ")
    elif os_type == "Darwin":  # macOS
        print("(MacOS,", end=" ")
    elif os_type == "Linux":
        print("(Linux,", end=" ")
    else:
        print("(Unknown OS,", end=" ", file=sys.stderr)
    print(f"Python {sys.version_info[0]}.{sys.version_info[1]}.", end="")
    print(f"{sys.version_info[2]})")
    print("Hello from the PyHelper community!", end=" ")
    print("https://githun.com/nanocode38/pyhelper.git")
    if os_type not in ("Windows", "Darwin", "Linux"):
        print("Warning: Unknown OS, some functions may not work properly.", file=sys.stderr)


def get_version():
    """Returns the current version number of the pygwidgets package"""
    return __version__


@contextmanager
def chdir(path: str) -> Generator[None, Any, None]:
    """
    Context Manager: Temporarily change the current working directory to the specified path.

    Args:
        path: The path to change the current working directory to.

    Returns:
        The original working directory.

    Examples:
        >>> import os
        >>> this_path = os.path.abspath('.')
        >>> father_path = os.path.abspath('..')
        >>> with chdir(father_path):
        ...     os.getcwd() == father_path
        ...
        True
        >>> os.getcwd() == this_path
        True
    """

    original_path = os.path.abspath(os.getcwd())
    os.chdir(path)
    yield
    os.chdir(original_path)


@contextmanager
def file_reopen(file_obj, stream=sys.stdout) -> Generator[None, Any, None]:
    """
    Context Manager: Temporarily change the standard output stream to the specified file.

    Args:
        file_obj: The Object of the file to redirect the standard output stream to.
        stream: The stream to redirect.

    Returns:
        The original standard output stream.

    Examples:
        >>> original_stdin = sys.stdin
        >>> original_stdout = sys.stdout
        >>> if not os.path.isfile("test.in"):
        ...     os.chdir("../tests")
        >>> with open("test.in", "r", encoding="utf-8") as fb:
        ...     with file_reopen(fb, "stdin"):
        ...         print(sys.stdin == fb)
        ...         file_input = input()
        True
        >>> sys.stdin == original_stdin
        True
        >>> file_input == "Hello, World!"
        True
        >>> with open("test.out", "w", encoding="utf-8") as fb:
        ...     with file_reopen(fb, "stdout"):
        ...         print("Hello, World!")
        ...         spam = (sys.stdout == fb)
        >>> sys.stdout == original_stdout
        True
        >>> spam
        True
        >>> with open("test.out", "r", encoding="utf-8") as fb:
        ...     fb.read() == "Hello, World!\\n"
        True
        >>> with open("test.out", "w", encoding="utf-8"):
        ...     pass
    """
    original_stream = sys.stdin
    if isinstance(stream, str):
        stream = stream.lower()
    if stream in (sys.stdin, "stdin"):
        sys.stdin = file_obj
        yield
        sys.stdin = original_stream
    elif stream in (sys.stdout, "stdout"):
        original_stream = sys.stdout
        sys.stdout = file_obj
        yield
        sys.stdout = original_stream
    elif stream in (sys.stderr, "stderr"):
        original_stream = sys.stderr
        sys.stderr = file_obj
        yield
        sys.stderr = original_stream
    else:
        raise ValueError("Invalid stream specified")


def join_startup(target: Path | str, *args, **kwargs) -> bool:
    """
    Add a file to startup on Windows, macOS, or Linux.

    Args:
        target: Absolute path to the file/script to run at startup.
        args and kwargs: Used to be compatible with old versions of name parameters

    Returns:
        True if successful, False otherwise.

    Raises:
        OSError: If the platform is not supported.

    Notes:
        - Windows: Uses registry (HKCU) for user-level startup
        - macOS: Creates Launch Agent plist in ~/Library/LaunchAgents
        - Linux: Creates systemd user service or .desktop file
    """
    # Convert to absolute path and verify existence
    target = os.path.abspath(target)
    if not os.path.exists(target):
        print(f"Error: File not found at {target}", file=sys.stderr)
        return False

    os_type = platform.system()
    try:
        if os_type == "Windows":
            return _windows_startup(target)
        elif os_type == "Darwin":  # macOS
            return _macos_startup(target)
        elif os_type == "Linux":
            return _linux_startup(target)
        else:
            raise OSError("Unsupported platform, join_startup() is only available for Windows, MacOS and Linux systems")
    except Exception as e:
        print(f"Setup failed: {str(e)}")
        return False


def _windows_startup(file_path: str) -> bool:
    """Windows implementation using registry"""
    import winreg  # Standard library for registry access

    # Determine execution command
    cmd = f'"{file_path}"'  # Default for executables/batch files
    if file_path.endswith(".py"):
        python_exe = f'"{sys.executable}"'  # Use current Python interpreter
        cmd = f'{python_exe} "{file_path}"'

    # Create registry entry
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    entry_name = "Startup_" + os.path.basename(file_path).replace(" ", "_")[:30]

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, entry_name, 0, winreg.REG_SZ, cmd)
        print(f"Added to startup: HKCU\\{key_path}\\{entry_name}")
        return True
    except WindowsError as e:
        print(f"Registry error: {str(e)}")
        return False


def _macos_startup(file_path: str) -> bool:
    """macOS implementation using LaunchAgent"""
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.startup.{os.path.basename(file_path)}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable if file_path.endswith('.py') else '/bin/sh'}</string>
        <string>{file_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/{os.path.basename(file_path)}.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/{os.path.basename(file_path)}_error.log</string>
</dict>
</plist>"""

    # Create LaunchAgents directory if missing
    launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(launch_agents_dir, exist_ok=True)

    # Write plist file
    plist_name = f"com.startup.{Path(file_path).stem}.plist"
    plist_path = os.path.join(launch_agents_dir, plist_name)

    with open(plist_path, "w") as f:
        f.write(plist_content)

    # Load the agent
    subprocess.run(["launchctl", "load", plist_path], check=True)
    print(f"LaunchAgent created at {plist_path}")
    return True


def _linux_startup(file_path: str) -> bool:
    """Linux implementation using systemd user service"""
    service_content = f"""[Unit]
Description=Startup Service: {os.path.basename(file_path)}
After=network.target

[Service]
ExecStart={'/usr/bin/python3 ' if file_path.endswith('.py') else ''}{file_path}
Restart=on-failure
Environment="DISPLAY=:0"  # Required for GUI apps

[Install]
WantedBy=default.target
"""

    # Create systemd user directory
    user_service_dir = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(user_service_dir, exist_ok=True)

    # Write service file
    service_name = f"startup_{Path(file_path).stem}.service"
    service_path = os.path.join(user_service_dir, service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    # Enable and start service
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "--user", "enable", service_name], check=True)
    subprocess.run(["systemctl", "--user", "start", service_name], check=True)

    print(f"Systemd service created at {service_path}")
    return True


def system(command: str, nonblocking: bool = False) -> int:
    """
    A function is used to replace the os.system()

    Args:
        command: Same as os.system(), the instruction that needs to be run
        nonblocking: Whether to run in a different process (whether not to block the current process), default False

    Returns:
        exit code
    """
    if not nonblocking:
        return os.system(command)
    else:
        multiprocessing.Process(target=os.system, args=(command,)).start()
        return 0


def get_annotation():
    """
    Returns:
        A decorator to simulate annotations in Java. This decorator is temporal
    """

    def annotation(func, *args, **kwargs):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return annotation


class Singleton(ABC):
    """
    An abstract base class to allow its subclass to be instantiated only once.

    Warning:
        If the subclass overloads the __new__() method, the parent class's __new__()
        method must be called in the __new__() method of the subclass, otherwise this abstract base class is invalid

    Examples:
        >>> class FooSingleton(Singleton):
        ...     def __init__(self):
        ...         self.foo = 1
        ...
        >>> spam = FooSingleton()
        >>> egg = FooSingleton()
        Traceback (most recent call last):
        ...
        RuntimeError: The Singleton Class can only be instantiated once
    """

    _has_instantiation = False

    def __new__(cls, *args, **kwargs):
        if cls._has_instantiation:
            raise RuntimeError("The Singleton Class can only be instantiated once")
        cls._has_instantiation = True
        return super().__new__(cls)


@contextmanager
def timer(callback: Callable[[float, ...], Any] | None = None, *args, **kwargs) -> Generator[float, Any, None]:
    """
    Context Manager for Calculating Program Running Time

    Args:
        callback: Callback function, called at the end of the manager, contains at least the first parameter and the parameter type is float to accept time, Default: Do Nothing
        args: Positional parameters will be passed to the callback function
        kwargs: keyword parameters will be passed to the callback function

    Returns:
        Generator[float, Any, None]: The starting execution time (UTC time)

    Examples:
        >>> import time
        >>> import math
        >>> t0 = time.time()
        >>> time.sleep(2)
        >>> t1 = time.time() - t0
        >>> t2: int
        >>> def spam(t1: float, bar, egg):
        ...     global t2
        ...     print(egg)
        ...     print(bar)
        ...     t2 = t1
        ...
        >>> with timer(spam, 1, egg="Hello"):
        ...     time.sleep(2)
        ...
        Hello
        1
        >>> math.isclose(t1, t2, rel_tol=.1)
        True
        >>> math.isclose(t2, 2., rel_tol=.1)
        True
    """
    import time

    t = time.time()
    yield t
    if callback is not None:
        callback(time.time() - t, *args, **kwargs)


class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_recursive_optimization(func):
    """
    A decorator to optimize tail recursion

    Warning: Do not use this decorator on functions called without tailless recursively, otherwise there will be
    unpredictable consequences


    Examples:
        >>> def factorial(n, acc=1):
        ...     if n == 0:
        ...         return acc
        ...     return factorial(n - 1, n * acc)
        ...
        >>> factorial(1000)
        Traceback (most recent call last):
        ...
        RecursionError: maximum recursion depth exceeded
        >>> @tail_recursive_optimization
        ... def factorial(n, acc=1):
        ...    if n == 0:
        ...       return acc
        ...    return factorial(n - 1, n * acc)
        ...
        >>> factorial(1000)
        402387260077093773543702433923003985719374864210714632543799910429938512398629020592044208486969404800479988610197196058631666872994808558901323829669944590997424504087073759918823627727188732519779505950995276120874975462497043601418278094646496291056393887437886487337119181045825783647849977012476632889835955735432513185323958463075557409114262417474349347553428646576611667797396668820291207379143853719588249808126867838374559731746136085379534524221586593201928090878297308431392844403281231558611036976801357304216168747609675871348312025478589320767169132448426236131412508780208000261683151027341827977704784635868170164365024153691398281264810213092761244896359928705114964975419909342221566832572080821333186116811553615836546984046708975602900950537616475847728421889679646244945160765353408198901385442487984959953319101723355556602139450399736280750137837615307127761926849034352625200015888535147331611702103968175921510907788019393178114194545257223865541461062892187960223838971476088506276862967146674697562911234082439208160153780889893964518263243671616762179168909779911903754031274622289988005195444414282012187361745992642956581746628302955570299024324153181617210465832036786906117260158783520751516284225540265170483304226143974286933061690897968482590125458327168226458066526769958652682272807075781391858178889652208164348344825993266043367660176999612831860788386150279465955131156552036093988180612138558600301435694527224206344631797460594682573103790084024432438465657245014402821885252470935190620929023136493273497565513958720559654228749774011413346962715422845862377387538230483865688976461927383814900140767310446640259899490222221765904339901886018566526485061799702356193897017860040811889729918311021171229845901641921068884387121855646124960798722908519296819372388642614839657382291123125024186649353143970137428531926649875337218940694281434118520158014123344828015051399694290153483077644569099073152433278288269864602789864321139083506217095002597389863554277196742822248757586765752344220207573630569498825087968928162753848863396909959826280956121450994871701244516461260379029309120889086942028510640182154399457156805941872748998094254742173582401063677404595741785160829230135358081840096996372524230560855903700624271243416909004153690105933983835777939410970027753472000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        frame = sys._getframe()
        # Check whether the grandfather stack frame (f_back.f_back) of the current stack frame is the same as the current function
        if frame.f_back and frame.f_back.f_back and frame.f_back.f_back.f_code == frame.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while True:
                try:
                    return func(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    return wrapper


def _getattr(origin, **kwargs):
    @functools.wraps(origin)
    def __getattr__(self, name):
        if name in kwargs.keys():
            return kwargs[name]
        return origin(self, name)
    return __getattr__

def _setattr(origin, **kwargs):
    @functools.wraps(origin)
    def __setattr__(self, name, value):
        if name in kwargs.keys():
            raise AttributeError(f"Readonly attribute {name}")
        origin(self, name, value)
    return __setattr__

def _dir(origin, **kwargs):
    @functools.wraps(origin)
    def __dir__(self):
        return origin(self) + list(kwargs.keys())



def readonly_attr(**kwargs):
    """
    Class decorator, used to set read-only attributes. Pass the attribute name and value through keyword parameters

    Args:
        **kwargs: Set of parameters used to set read-only attributes

    Examples:
        >>> @readonly_attr(a='a', b=[1, 2])
        ... class Span:
        ...     def __init__(self):
        ...         self.c = 1
        ...         self.d = 2
        ...     def __getattr__(self, item):
        ...         if item == 'w':
        ...             return self.c
        ...         return self.__dict__[item]
        ...
        >>> span = Span()
        >>> span.w
        1
        >>> span.c, span.d
        (1, 2)
        >>> span.a, span.b
        ('a', [1, 2])
        >>> span.a = 'b'
        Traceback (most recent call last):
        ...
        AttributeError: Readonly attribute a
        >>> span.a
        'a'
        >>> span.b = 'b'
        Traceback (most recent call last):
        ...
        AttributeError: Readonly attribute b
        >>> span.b
        [1, 2]
    """
    def wrapper(cls):
        cls.__setattr__ = _setattr(cls.__setattr__, **kwargs)
        cls.__getattribute__ = _getattr(cls.__getattribute__, **kwargs)
        cls.__dir__ = _dir(cls.__dir__, **kwargs)
        return cls
    return wrapper

if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
