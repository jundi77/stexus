from abc import abstractmethod
from .interface import StudyInterface
from .exception import StudyException
from ..config.loader import ConfigModel
from ..experiment.interface import ExperimentInterface

class BaseStudy(StudyInterface):
    def __init__(self,
                 config: ConfigModel|None = None,
                 experiment: ExperimentInterface|None = None
    ) -> None:
        super().__init__()
        if config is None:
            raise StudyException("config cannot be empty.")
        if experiment is None:
            raise StudyException("experiment cannot be empty.")

        self._config = config
        self._experiment = experiment

    @abstractmethod
    def study(self):
        pass
