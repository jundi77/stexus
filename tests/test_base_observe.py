from optuna import Trial
import pytest
from stexus.observe.BaseObserve import BaseObserve
from stexus.observe.ObserveException import ObserveException

class NoopObserve(BaseObserve):
    def observe(self, ignore_config_enabled: bool = False) -> None:
        return

def test_empty_config():
    with pytest.raises(ObserveException):
        NoopObserve(None) # type: ignore
