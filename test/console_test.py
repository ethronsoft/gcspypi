from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.exceptions import *
import sys
import six
import pytest
if six.PY2:
    from StringIO import StringIO # pylint: disable=E0401
else:
    from io import StringIO 

#NOTE: console writes to stderr any messages with the exception
# of `output`, which goes to stdout

def test_no_exception():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as c:
            c.info("hello")
            c.error("wrong")
            c.warning("careful")
            c.badge("hello", "success")
            c.badge("hello", "warning")
            c.badge("hello", "danger")
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 6
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_dynamic():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as c:
            pending = c.info("hello", "\r")
            c.blank(pending)
            c.info("world")
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 1
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_output():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        with Console() as c:
           c.output("hello")
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 1
        assert len(err.readlines()) == 0
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_input_with_response():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO("hello\n")
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as c:
           assert c.input("do this", "default") == "hello"
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 1
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_input_without_response():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO("\n")
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as c:
           assert c.input("do this", "default") == "default"
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 1
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_selection():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    curr_stdin = sys.stdin
    try:
        out = StringIO()
        err = StringIO()
        cin = StringIO("y\n")
        sys.stdout = out
        sys.stderr = err
        sys.stdin = cin
        with Console() as c:
           assert c.selection("do this", ["y", "n"]) == "y"
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 1
    finally:
        sys.stdin = curr_stdin
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_exception():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        try:
            with Console(exit_on_error=False) as c:
                c.info("hello")
                raise Exception("urgh")
        except:
            pass
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == 2
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_exception_verbose():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        try:
            with Console(exit_on_error=False, verbose=True) as c:
                c.info("hello")
                raise Exception("urgh")
        except:
            pass
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) > 1 #expecting more than one line from verbose
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr

def test_custom_exceptions():
    curr_stdout = sys.stdout
    curr_stderr = sys.stderr
    try:
        out = StringIO()
        err = StringIO()
        sys.stdout = out
        sys.stderr = err
        excs = [NotFound, InvalidParameter, InvalidState, RepositoryError, ScriptError]
        for Exc in excs:
            try:
                with Console(exit_on_error=False):
                    raise Exc("urgh")
            except:
                pass
        out.seek(0)
        err.seek(0)
        assert len(out.readlines()) == 0
        assert len(err.readlines()) == len(excs)
    finally:
        sys.stdout = curr_stdout
        sys.stderr = curr_stderr