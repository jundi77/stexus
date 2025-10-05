from optuna import Trial
import pytest
from stexus.study.base import BaseStudy
from stexus.study.exception import StudyException

class NoopStudy(BaseStudy):
    def study(self):
        return

class MockExperiment():
    def experiment(self, advocator: Trial) -> float | int:
        return 1

def test_empty_config():
    with pytest.raises(StudyException):
        NoopStudy(None, MockExperiment()) # type: ignore

def test_empty_experiment():
    with pytest.raises(StudyException):
        NoopStudy({}, None) # type: ignore
