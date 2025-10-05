import pytest
import jinja2
import pathlib
from optuna import Trial
from stexus.adjust.BaseAdjust import BaseAdjust
from stexus.adjust.AdjustException import AdjustException

class MockRealizedBaseAdjust(BaseAdjust):
    def adjust(self, advocator: Trial) -> None:
        return super().adjust(advocator)

    def get_config(self):
        return self._config
    
    def get_source_template_environments(self):
        return self._source_template_environments

def test_nil_config():
    # test with nonexistent path inside tmp_path
    with pytest.raises(AdjustException):
        MockRealizedBaseAdjust() # type: ignore

def test_source_templates_nonexistent_path(tmp_path: pathlib.Path):
    # test with nonexistent path inside tmp_path
    with pytest.raises(AdjustException):
        MockRealizedBaseAdjust({
            'source_templates': [tmp_path / 'nonexistent']
        }) # type: ignore

def test_source_templates_is_file(tmp_path: pathlib.Path):
    tmp_file = tmp_path / 'test_file'
    tmp_file.write_text('')

    mock_base_adjust = MockRealizedBaseAdjust({
        'source_templates': [tmp_file]
    }) # type: ignore

    source_template_environment = mock_base_adjust.get_source_template_environments()[0]

    assert source_template_environment['is_file'] == True
    assert source_template_environment['filename'] == tmp_file.name
    assert source_template_environment['path'] == str(tmp_file.parent.absolute())

    # default rendered_templates_path currently is `rendered`
    assert source_template_environment['rendered_path'] == str(tmp_file.parent.absolute().joinpath('rendered'))

    assert isinstance(source_template_environment['environment'], jinja2.Environment)
    assert isinstance(source_template_environment['environment'].loader, jinja2.FileSystemLoader)
    assert source_template_environment['environment'].keep_trailing_newline == True

    ## this returns another function named `autoescape`, idk how to check identical function
    # assert source_template_environment['environment'].autoescape == jinja2.select_autoescape()

def test_source_templates_is_folder(tmp_path: pathlib.Path):
    tmp_dir = tmp_path / 'test_dir'
    tmp_dir.mkdir()
    import os
    print(os.path.isdir(tmp_dir))

    mock_base_adjust = MockRealizedBaseAdjust({
        'source_templates': [tmp_dir]
    }) # type: ignore

    source_template_environment = mock_base_adjust.get_source_template_environments()[0]

    assert source_template_environment['is_file'] == False
    assert source_template_environment['filename'] == None
    assert source_template_environment['path'] == str(tmp_dir.absolute())
    
    # default rendered_templates_path currently is `rendered`
    assert source_template_environment['rendered_path'] == str(tmp_dir.absolute().joinpath('rendered'))

    assert isinstance(source_template_environment['environment'], jinja2.Environment)
    assert isinstance(source_template_environment['environment'].loader, jinja2.FileSystemLoader)
    assert source_template_environment['environment'].keep_trailing_newline == True

    ## this returns another function named `autoescape`, idk how to check identical function
    # assert source_template_environment['environment'].autoescape == jinja2.select_autoescape()
