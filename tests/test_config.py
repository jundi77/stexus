import pathlib, pytest
from stexus.config.loader import Config
from stexus.config.exception import ConfigException

"""TODO
more config test case should come after the config schema is done
plan is to use openapi schema instead of current cerberus config
"""

def test_valid_config_optuna_script(tmp_path: pathlib.Path):
    config_file = tmp_path / 'config.yaml'
    config_file.write_text(
        'study_name: Number Guessing with Machine Learning\n'
        'engine: optuna\n'
        'trials: 50\n'
        'source_templates:\n'
        '    - ./guess.sh\n'
        'rendered_templates_path: ./rendered\n'
        'score_path: ./result\n'
        'storage: sqlite:///tmp.sqlite3\n'
        'load_if_exists: true\n'
        'direction: minimize\n'
        'experiment:\n'
        '   type: script\n'
        '   args: ./rendered/guess.sh\n'
        'observer:\n'
        '   enabled: true\n'
        'adjustments:\n'
        '    - name: guess_number\n'
        '      type: int\n'
        '      config:\n'
        '         low: 1\n'
        '         high: 40\n'
    )

    config = Config(str(config_file.absolute()))
    assert config.get_parsed_config() == {
        'study_name': 'Number Guessing with Machine Learning',
        'engine': 'optuna',
        'trials': 50,
        'score_path': './result',
        'storage': 'sqlite:///tmp.sqlite3',
        'load_if_exists': True,
        'direction': 'minimize',
        'source_templates': ['./guess.sh'],
        'rendered_templates_path': './rendered',
        'experiment': {
            'type': 'script',
            'args': './rendered/guess.sh',
            'ignore_exit_code': False,
        },
        'observer': {
            'enabled': True,
            'host': '127.0.0.1',
            'port': 8080,
            'quiet': False,
            'server': 'auto',
        },
        'adjustments': [
            {
                'name': 'guess_number',
                'type': 'int',
                'config': {
                    'low': 1,
                    'high': 40,
                    'log': False,
                    'step': None,
                },
            }
        ]
    }

def test_invalid_config_wrong_engine_script(tmp_path: pathlib.Path):
    config_file = tmp_path / 'config.yaml'
    config_file.write_text(
        'study_name: Number Guessing with Machine Learning\n'
        'engine: unsupported\n'
        'trials: 50\n'
        'source_templates:\n'
        '    - ./guess.sh\n'
        'rendered_templates_path: ./rendered\n'
        'score_path: ./result\n'
        'storage: sqlite:///tmp.sqlite3\n'
        'load_if_exists: true\n'
        'direction: minimize\n'
        'experiment:\n'
        '   type: script\n'
        '   args: ./rendered/guess.sh\n'
        'observer:\n'
        '   enabled: true\n'
        'adjustments:\n'
        '    - name: guess_number\n'
        '      type: int\n'
        '      config:\n'
        '      low: 1\n'
        '      high: 40\n'
    )

    with pytest.raises(ConfigException):
        Config(str(config_file.absolute()))

def test_invalid_config_optuna_wrong_experiment(tmp_path: pathlib.Path):
    config_file = tmp_path / 'config.yaml'
    config_file.write_text(
        'study_name: Number Guessing with Machine Learning\n'
        'engine: unsupported\n'
        'trials: 50\n'
        'source_templates:\n'
        '    - ./guess.sh\n'
        'rendered_templates_path: ./rendered\n'
        'score_path: ./result\n'
        'storage: sqlite:///tmp.sqlite3\n'
        'load_if_exists: true\n'
        'direction: minimize\n'
        'experiment:\n'
        '   type: script_but_unsupported\n'
        '   args: ./rendered/guess.sh\n'
        'observer:\n'
        '   enabled: true\n'
        'adjustments:\n'
        '    - name: guess_number\n'
        '      type: int\n'
        '      config:\n'
        '      low: 1\n'
        '      high: 40\n'
    )

    with pytest.raises(ConfigException):
        Config(str(config_file.absolute()))

def test_invalid_config_optuna_script_nonexistent_adjustments(tmp_path: pathlib.Path):
    config_file = tmp_path / 'config.yaml'
    config_file.write_text(
        'study_name: Number Guessing with Machine Learning\n'
        'engine: unsupported\n'
        'trials: 50\n'
        'source_templates:\n'
        '    - ./guess.sh\n'
        'rendered_templates_path: ./rendered\n'
        'score_path: ./result\n'
        'storage: sqlite:///tmp.sqlite3\n'
        'load_if_exists: true\n'
        'direction: minimize\n'
        'experiment:\n'
        '   type: script_but_unsupported\n'
        '   args: ./rendered/guess.sh\n'
        'observer:\n'
        '   enabled: true\n'
        'adjustments:\n'
        '    - name: guess_number\n'
        '      type: qbit_unsupported\n'
        '      config:\n'
        '      low: 1\n'
        '      high: 40\n'
    )

    with pytest.raises(ConfigException):
        Config(str(config_file.absolute()))
