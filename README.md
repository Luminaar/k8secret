k8secrets
=====
[![PyPI version](https://img.shields.io/pypi/v/k8secrets?color=blue)](https://pypi.org/project/k8secrets/)
[![Python versions](https://img.shields.io/pypi/pyversions/k8secrets)](https://pypi.org/project/k8secrets/)
[![Code style](https://img.shields.io/badge/formatted%20with-black-black)](https://github.com/psf/black)

When deploying an application to k8s cluster you often need to create a `Secret`
or `ConfigMap` object that contains environment variables for that application.

This is a tedious process:

1. Create a `.yaml` file
2. `base64` encode it
3. Add key/value pairs to the `.yaml` file

This tool will automate that process for you.


## Installation
Use [pipx](https://pipxproject.github.io/pipx/installation/) to install this
package. The package will be installed in isolation and a `k8secret` command
will be added to your path.

`pipx install k8secrets`


## Usage
`k8secrets` takes an object name and a list of variables as input and creates a
`Secret` Kubernetes object:

    k8secrets mysecret -l KEY1=value1,KEY2=value2

or a `ConfigMap`:

    k8secrets --config myconfig -l KEY1=value1,KEY2=value2

Variable list is a list of key/value pairs in any of the following formats:

- `KEY=value`
- `export KEY=value` - found in `.env` files on Linux
- `KEY:value`
- `KEY\tvalue` (separated by a tab character)

If `value` is wrapped in `''` or `""`, the quotes are ignored. Pairs can be
separated either by a newline character (Unix or Windows), `,` or `;`.

### Output
`k8secrets` prints output to `stdout`. The output is valid `yaml` and contains
two sections. First is a complete k8s `Secret` or `ConfigMap` object:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  KEY1: dmFsdWUx
  KEY2: dmFsdWUy
```

The second is an `envFrom` section with a reference to the Secret or ConfigMap object that you
can use in your deployments or cronjobs:

```yaml
---
envFrom:
  - secretRef:
      name: mysecret
```

## Development
The application is written in Python and uses
[Poetry](https://python-poetry.org/docs/) to configure the package and manage
it's dependencies.

Make sure you have [Poetry CLI installed](https://python-poetry.org/docs/#installation).
Then you can run

    $ poetry install

which will install the project dependencies (including `dev` dependencies) into a
Python virtual environment managed by Poetry (alternatively, you can activate
your own virtual environment beforehand and Poetry will use that).

### Run tests with pytest

    $ poetry run pytest

or activate the `poetry` shell first

	$ poetry shell
	$ pytest
