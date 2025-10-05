import pathlib
import pytest
from stexus.adjust.AdjustOptuna import AdjustOptuna
from stexus.study.StudyOptuna import StudyOptuna
from optuna import Trial
from stexus.experiment.ExperimentInterface import ExperimentInterface

class MockExperiment(ExperimentInterface):
    def __init__(self, adjust: AdjustOptuna) -> None:
        self._adjust = adjust

    def experiment(self, advocator: Trial) -> float | int:
        self._adjust.adjust(advocator)
        return 1

def test_adjust_empty_source_template_environments(monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        # so that we don't have to instantiate adjust base class
        m.setattr(AdjustOptuna, '__init__', lambda x: None)

        adjust = AdjustOptuna()

        # force _source_template_environments to become None
        adjust._source_template_environments = None # type: ignore

        assert adjust.adjust(None) == None # type: ignore

def test_study_with_file_as_source_template(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path):
    file_template = tmp_path / 'test_file'
    file_template.write_text(
        '{{ param_int }}\n'
        '{{ param_float }}\n'
        '{{ param_categorical }}\n'
        '{{ param_uniform }}\n'
        '{{ param_discrete_uniform }}\n'
        '{{ param_loguniform }}\n'
    )
    rendered_path = tmp_path / 'rendered'
    mock_score_file = tmp_path / 'result'
    mock_score_file.write_text('1')

    # only releveant config for optuna related study
    config = {
        # score_path is read 
        # 'score_path': str(mock_score_file),
        'study_name': 'test',
        'engine': 'optuna',
        'trials': 1,
        'storage': f'sqlite:///{str(tmp_path)}/tmp.sqlite3',
        'load_if_exists': True,
        'direction': 'maximize',
        'source_templates': [str(file_template)],
        'rendered_templates_path': str(rendered_path),
        'adjustments': [
                {
                    'name': 'param_int',
                    'type': 'int',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_float',
                    'type': 'float',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_categorical',
                    'type': 'categorical',
                    'config': {
                        'choices': [
                            'test'
                        ],
                    }
                },
                {
                    'name': 'param_uniform',
                    'type': 'uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_discrete_uniform',
                    'type': 'discrete_uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                        'q': 1,
                    }
                },
                {
                    'name': 'param_loguniform',
                    'type': 'loguniform',
                    'config': {
                        'low': 1,
                        'high': 2,
                    }
                },
            ]
    }

    adjust = AdjustOptuna(config) # type: ignore
    mock_experiment = MockExperiment(adjust)
    study = StudyOptuna(config, mock_experiment) # type: ignore

    # should not raises any exception
    study.study()
    
    rendered_result = [f for f in rendered_path.iterdir() if f.is_file()]
    assert len(rendered_result) == 1

def test_study_with_files_as_source_templates(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path):
    file_template_0 = tmp_path / 'test_file_0'
    file_template_0.write_text(
        '{{ param_int }}\n'
        '{{ param_float }}\n'
        '{{ param_categorical }}\n'
        '{{ param_uniform }}\n'
        '{{ param_discrete_uniform }}\n'
        '{{ param_loguniform }}\n'
    )
    file_template_1 = tmp_path / 'test_file_1'
    file_template_1.write_text(
        '{{ param_int }}\n'
        '{{ param_float }}\n'
        '{{ param_categorical }}\n'
        '{{ param_uniform }}\n'
        '{{ param_discrete_uniform }}\n'
        '{{ param_loguniform }}\n'
    )
    rendered_path = tmp_path / 'rendered'
    mock_score_file = tmp_path / 'result'
    mock_score_file.write_text('1')

    # only releveant config for optuna related study
    config = {
        # score_path is read 
        # 'score_path': str(mock_score_file),
        'study_name': 'test',
        'engine': 'optuna',
        'trials': 1,
        'storage': f'sqlite:///{str(tmp_path)}/tmp.sqlite3',
        'load_if_exists': True,
        'direction': 'maximize',
        'source_templates': [str(file_template_0), str(file_template_1)],
        'rendered_templates_path': str(rendered_path),
        'adjustments': [
                {
                    'name': 'param_int',
                    'type': 'int',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_float',
                    'type': 'float',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_categorical',
                    'type': 'categorical',
                    'config': {
                        'choices': [
                            'test'
                        ],
                    }
                },
                {
                    'name': 'param_uniform',
                    'type': 'uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_discrete_uniform',
                    'type': 'discrete_uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                        'q': 1,
                    }
                },
                {
                    'name': 'param_loguniform',
                    'type': 'loguniform',
                    'config': {
                        'low': 1,
                        'high': 2,
                    }
                },
            ]
    }

    adjust = AdjustOptuna(config) # type: ignore
    mock_experiment = MockExperiment(adjust)
    study = StudyOptuna(config, mock_experiment) # type: ignore

    # should not raises any exception
    study.study()

    rendered_result = [f for f in rendered_path.iterdir() if f.is_file()]
    assert len(rendered_result) == 2

def test_study_with_dir_as_source_templates(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path):
    subdir = tmp_path / 'subdir'
    subdir.mkdir()
    file_template_0 = subdir / 'test_file_0'
    file_template_0.write_text(
        '{{ param_int }}\n'
        '{{ param_float }}\n'
        '{{ param_categorical }}\n'
        '{{ param_uniform }}\n'
        '{{ param_discrete_uniform }}\n'
        '{{ param_loguniform }}\n'
    )
    file_template_1 = subdir / 'test_file_1'
    file_template_1.write_text(
        '{{ param_int }}\n'
        '{{ param_float }}\n'
        '{{ param_categorical }}\n'
        '{{ param_uniform }}\n'
        '{{ param_discrete_uniform }}\n'
        '{{ param_loguniform }}\n'
    )
    rendered_path = tmp_path / 'rendered'
    mock_score_file = tmp_path / 'result'
    mock_score_file.write_text('1')

    # only releveant config for optuna related study
    config = {
        # score_path is read 
        # 'score_path': str(mock_score_file),
        'study_name': 'test',
        'engine': 'optuna',
        'trials': 1,
        'storage': f'sqlite:///{str(tmp_path)}/tmp.sqlite3',
        'load_if_exists': True,
        'direction': 'maximize',
        'source_templates': [str(subdir)],
        'rendered_templates_path': str(rendered_path),
        'adjustments': [
                {
                    'name': 'param_int',
                    'type': 'int',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_float',
                    'type': 'float',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_categorical',
                    'type': 'categorical',
                    'config': {
                        'choices': [
                            'test'
                        ],
                    }
                },
                {
                    'name': 'param_uniform',
                    'type': 'uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                    }
                },
                {
                    'name': 'param_discrete_uniform',
                    'type': 'discrete_uniform',
                    'config': {
                        'low': 0,
                        'high': 1,
                        'q': 1,
                    }
                },
                {
                    'name': 'param_loguniform',
                    'type': 'loguniform',
                    'config': {
                        'low': 1,
                        'high': 2,
                    }
                },
            ]
    }

    adjust = AdjustOptuna(config) # type: ignore
    mock_experiment = MockExperiment(adjust)
    study = StudyOptuna(config, mock_experiment) # type: ignore

    # should not raises any exception
    study.study()

    rendered_result = [f for f in rendered_path.iterdir() if f.is_file()]
    assert len(rendered_result) == 2
