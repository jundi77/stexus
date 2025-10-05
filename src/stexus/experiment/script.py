import subprocess, os, stat
from optuna import Trial
from .base import BaseExperiment
from .exception import ExperimentException
from ..config.loader import ConfigModel
from ..adjust.interface import AdjustInterface

class ExperimentWithScript(BaseExperiment):
    def __init__(self,
                 config: ConfigModel|None = None,
                 adjust: AdjustInterface|None = None
    ) -> None:
        super().__init__(config, adjust)

    def _run_script(self) -> None:
        if os.path.isfile(self._config["experiment"]["args"]) and not os.access(self._config["experiment"]["args"], os.X_OK):
            """if args is file and it doesn't have executable flag,
            add executable flag.
            """
            os.chmod(
                self._config["experiment"]["args"],
                os.stat(
                    self._config["experiment"]["args"]
                ).st_mode | stat.S_IEXEC
            )
        subprocess.run(
            args=self._config["experiment"]["args"],
            check=not self._config["experiment"].get("ignore_exit_code", False),
            shell=True,
        )

    def _get_score(self) -> float:
        with open(self._config["score_path"], "r") as f:
            first_line = f.readline()

        return float(first_line)

    """
    returns score
    either in int or float.
    """
    def experiment(self, advocator: Trial) -> float|int:
        self._adjust.adjust(advocator)
        self._run_script()
        return self._get_score()
