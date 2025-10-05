import platform
import os, stat
import pathlib
from stexus.adjust.interface import AdjustInterface
from stexus.experiment.script import ExperimentWithScript
from optuna import Trial

class MockAdjust(AdjustInterface):
    def adjust(self, advocator: Trial) -> None:
        return

class MockAdvocator():
    def __init__(self) -> None:
        return

def test_run_script_with_executable_flag(tmp_path: pathlib.Path):
    mock_score = tmp_path / 'score'
    mock_score.write_text('1')

    # this is platform dependant
    system = platform.system()

    if system == 'Linux' or system == 'Darwin':
        script = tmp_path / 'script'
        script.write_text(
            'echo "Hello, World"'
        )
        curr_fstat = os.stat(str(script.absolute()))
        os.chmod(str(script.absolute()), curr_fstat.st_mode | stat.S_IEXEC)
    elif system == 'Windows':
        script = tmp_path / 'script.bat'
        script.write_text(
            '@echo off\n'
            'echo Hello, World'
        )
    else:
        raise Exception('system is unsupported')

    config = {
        'experiment': {
            'args': str(script.absolute()),
            'ignore_exit_code': False
        },
        'score_path': str(mock_score.absolute())
    }

    experiment = ExperimentWithScript(config, MockAdjust()) # type: ignore
    score = experiment.experiment(MockAdvocator) # type: ignore
    assert score == 1


def test_run_script_without_executable_flag(tmp_path: pathlib.Path):
    mock_score = tmp_path / 'score'
    mock_score.write_text('1')

    # this is platform dependant
    system = platform.system()

    if system == 'Linux' or system == 'Darwin':
        script = tmp_path / 'script'
        script.write_text(
            'echo "Hello, World"'
        )
    elif system == 'Windows':
        script = tmp_path / 'script.bat'
        script.write_text(
            '@echo off\n'
            'echo Hello, World'
        )
    else:
        raise Exception('system is unsupported')

    config = {
        'experiment': {
            'args': str(script.absolute()),
            'ignore_exit_code': False
        },
        'score_path': str(mock_score.absolute())
    }

    experiment = ExperimentWithScript(config, MockAdjust()) # type: ignore
    score = experiment.experiment(MockAdvocator) # type: ignore
    assert score == 1
