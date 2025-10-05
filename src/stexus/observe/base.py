from abc import abstractmethod
from .interface import ObserveInterface
from .exception import ObserveException
from ..config.loader import ConfigModel

class BaseObserve(ObserveInterface):
    def __init__(self,
                 config: ConfigModel|None = None,
    ) -> None:
        super().__init__()
        if config is None:
            raise ObserveException("config cannot be empty.")

        self._config = config

    @abstractmethod
    def observe(self, ignore_config_enabled: bool=False) -> None:
        pass
