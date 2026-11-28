from commands.run_command import RunCommand
import pytest

command_tool = RunCommand("agent-scratch", 1000)

def test_hello_world():

    out = command_tool.run_command(["python", "-c", "print('Hello from sandbox!')"])

    assert out['success'] == True
    assert out["exit_code"] == 0
    assert out["stdout"] == "Hello from sandbox!\n"
    assert out["stderr"] == "  ✓ sandbox shell-agent-scratch — started\n" or out['stderr'] == ""
    assert out["timed_out"] == False

def test_timeout():

    out = command_tool.run_command(["python", "-c", "while True: pass"], 2)

    assert out['success'] == True
    assert out["exit_code"] is 124
    assert out["stdout"] == ""
    assert out["stderr"] == ""
    assert out["timed_out"] == True

def test_valueError():

    out = command_tool.run_command(["python", "-c", "print(int('teststring'))"], 2)

    assert out['success'] == True
    assert out["exit_code"] == 1
    assert out["stdout"] == ""
    assert out["stderr"] == "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\n    print(int('teststring'))\n          ~~~^^^^^^^^^^^^^^\nValueError: invalid literal for int() with base 10: 'teststring'\n"
    assert out["timed_out"] == False

def test_addition():

    out = command_tool.run_command(["python", "-c" "print(2+2)"], 2)

    assert out['success'] == True
    assert out["exit_code"] == 0
    assert out["stdout"] == "4\n"
    assert out["stderr"] == ""
    assert out["timed_out"] == False
