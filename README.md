# Stexus

*Study, Experiment, adjUst, Study*

Automated best parameter finder.

Supported engine:
    - Optuna ([site](https://optuna.org/))

## Running Stexus

TODO

## Configuration

Stexus take YAML file configuration. Format is as follows:

```yaml
# string
study_name: Stexus Example Configuration

# string, currently only supports: optuna
engine: optuna

# int, amount of trials
trials: 50

# list of strings,
# item can be file or directory.
# if directory, currently not supporting subdirectories
source_templates:
  - ./guess.sh

# string
# where templates should be rendered at
# if source_template is file, a rendered_templates_path is created on their path,
# if source_template is directory, a rendered_templates_path is created inside 'em.
#! NOT on current directory.
rendered_templates_path: rendered

# string, path where an experiment writes a score
score_path: ./result

# string
# if engine is optuna, then storage follows optuna docs.
storage: sqlite:///tmp.sqlite3

# boolean
# if engine is optuna, then load_if_exists follows optuna docs.
load_if_exists: true

# string
# if engine is optuna, then direction follows optuna docs.
# afaik it's either maximize or minimize
direction: minimize

experiment:
  # string
  # currently only supports: script
  type: script

  # string
  # if type is script, then what script will be run on experiment.
  args: ./rendered/guess.sh

observer:
  enabled: true

adjustments:
  - name: param1
    type: int
    config:
      low: 1
      high: 90
  - name: param2
    type: float
    config:
      low: 1.0
      high: 76.9

```
