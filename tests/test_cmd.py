import pytest
import argparse
from stexus import cmd
from stexus.config.Config import Config
from stexus.experiment.ExperimentWithScript import ExperimentWithScript
from stexus.adjust.AdjustInterface import AdjustInterface
from stexus.study.StudyOptuna import StudyOptuna
from stexus.adjust.BaseAdjust import BaseAdjust
from stexus.observe.ObserveOptuna import ObserveOptuna
from stexus.observe.ObserveInterface import ObserveInterface
from stexus.study.StudyInterface import StudyInterface

class MockAdjustInterface(AdjustInterface):
    def adjust(self, advocator) -> None:
        return

class MockObserveInterface(ObserveInterface):
    def observe(self, ignore_config_enabled: bool=False) -> None:
        return

class MockStudyInterface(StudyInterface):
    def study(self):
        return

class MockParseArgsStudyAndObserve():
    def __getattr__(self, name):
        if name == 'observe_only':
            return False
        elif name == 'config':
            return {} # empty config

class MockParseArgsObserveOnly():
    def __getattr__(self, name):
        if name == 'observe_only':
            return True
        elif name == 'config':
            return {} # empty config

@pytest.mark.parametrize(
    ['config','expected', 'exception'], [
        ({
            'experiment': {
                'type': 'script'
            }
        }, ExperimentWithScript, None),
        ({
            'experiment': {
                'type': 'nonexistent'
            }
        }, None, Exception),
    ]
)
def test_get_experiment(monkeypatch: pytest.MonkeyPatch, config, expected, exception):

    with monkeypatch.context() as m:
        mock_adjust = MockAdjustInterface()
        if exception is not None:
            with pytest.raises(exception) as excinfo:
                cmd._get_experiment(config, mock_adjust)
        else:
            experiment = cmd._get_experiment(config, mock_adjust)
            assert isinstance(experiment, expected)

@pytest.mark.parametrize(
        ['config', 'expected', 'exception'],
        [
            ({
                'engine': 'optuna'
            }, StudyOptuna, None),
            ({
                'engine': 'nonexistent'
            }, None, Exception),
        ]
)
def test_get_study(monkeypatch: pytest.MonkeyPatch, config, expected, exception):
    def mock_init(self, config):
        return None
    
    def mock_get_experiment(config, adjust):
        return MockAdjustInterface()

    with monkeypatch.context() as m:
        m.setattr(cmd, '_get_experiment', mock_get_experiment)
        m.setattr(BaseAdjust, '__init__', mock_init)
        if exception is not None:
            with pytest.raises(exception) as excinfo:
                cmd._get_study(config)
        else:
            study = cmd._get_study(config)
            assert isinstance(study, expected)

@pytest.mark.parametrize(
        ['config','expected', 'exception'],
        [
            ({
                'engine': 'optuna'
            }, ObserveOptuna, None),
            ({
                'engine': 'nonexistent'
            }, None, Exception),
        ]
)
def test_get_observe(config, expected, exception):
    if exception is not None:
        with pytest.raises(exception) as excinfo:
            cmd._get_observe(config)
    else:
        observe = cmd._get_observe(config)
        assert isinstance(observe, expected)

def test_run_study_and_observe(monkeypatch: pytest.MonkeyPatch):
    def mock_parse_args(self):
        return MockParseArgsStudyAndObserve()

    def mock_config_init(self, config_file: str|None=None) -> None:
        return
    
    def mock_config_get_parsed_config(self):
        return {}

    with monkeypatch.context() as m:
        # mock empty config
        m.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

        # mock Config class
        # don't test Config class here, test it on separate test unit
        m.setattr(Config, '__init__', mock_config_init)
        m.setattr(Config, 'get_parsed_config', mock_config_get_parsed_config)

        m.setattr(cmd, '_get_study', lambda x: MockStudyInterface())
        m.setattr(cmd, '_get_observe', lambda x: MockObserveInterface())

        # this test fail if cmd.run cause exception
        cmd.run()

def test_run_observe_only(monkeypatch: pytest.MonkeyPatch):
    def mock_parse_args(self):
        return MockParseArgsObserveOnly()

    def mock_config_init(self, config_file: str|None=None) -> None:
        return
    
    def mock_config_get_parsed_config(self):
        return {}

    with monkeypatch.context() as m:
        # mock empty config
        m.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

        # mock Config class
        # don't test Config class here, test it on separate test unit
        m.setattr(Config, '__init__', mock_config_init)
        m.setattr(Config, 'get_parsed_config', mock_config_get_parsed_config)

        m.setattr(cmd, '_get_study', lambda x: MockStudyInterface())
        m.setattr(cmd, '_get_observe', lambda x: MockObserveInterface())

        # this test fail if cmd.run cause exception
        cmd.run()
