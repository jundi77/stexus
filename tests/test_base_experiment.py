from optuna import Trial
import pytest
from stexus.experiment.base import BaseExperiment
from stexus.experiment.exception import ExperimentException
from stexus.adjust.interface import AdjustInterface

class NoopExperiment(BaseExperiment):
    def experiment(self, advocator: Trial) -> float | int:
        return 1

class MockAdjust(AdjustInterface):
    def adjust(self, advocator: Trial) -> None:
        return

def test_empty_config():
    with pytest.raises(ExperimentException):
        NoopExperiment(None, MockAdjust())

def test_empty_adjust():
    with pytest.raises(ExperimentException):
        NoopExperiment({}, None) # type: ignore