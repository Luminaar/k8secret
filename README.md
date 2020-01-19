k8secrets
=====
[![PyPI version](https://img.shields.io/pypi/v/k8secrets?color=blue)](https://pypi.org/project/k8secrets/)
[![Python versions](https://img.shields.io/pypi/pyversions/k8secrets)](https://pypi.org/project/k8secrets/)
[![Code style](https://img.shields.io/badge/formatted%20with-black-black)](https://github.com/psf/black)

When deploying an application to k8s cluster you often need to create a
`secret` object that contains environment variables for that application.

This is a tedious process:

1. Create a `.yaml` file
2. `base64` encode it
3. Add key/value pairs to the `.yaml` file
4. Add variables with correspondint references to the `env` section in a
   `deployment` object

This tool will automate that process for you.


## Installation
Use `pip` to install this package. You can install it in a virtualenv or
globally (this package has no dependencies an should not break your
environment).

`pip install --user k8secrets`

After this, you can run `k8secrets` command in your terminal or run the package like this:

`python3 -m k8secrests`


## Usage
`k8secrets` takes a `secret` object name and a list of variables as input:

    k8secrets mysecret KEY1=value1,KEY2=value2

It can also read the variables from `stdin` (you can pipe input into it):

    echo KEY1=value1,KEY2=value2 | k8secrets mysecret

Variable list is a list of key/value pairs in any of the following formats:

- `KEY=value`
- `export KEY=value` - found in `.env` files on Linux
- `KEY:value`
- `KEY\tvalue` (separated by a tab character)

If `value` is wrapped in `''` or `""`, the quotes are ignored. Pairs can be
separated either by a newline character (Unix or Windows), `,` or `;`.

### Output
`k8secrets` prints output to `stdout`. The output is valid `yaml` and contains
two sections. First is a complete k8s `secret` object:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  key1: dmFsdWUx
  key2: dmFsdWUy
```

The second is an `env` section with references to the `secret` object that you
can use in your `deployment`s or `cronjob`s:

```yaml
---
env:
  - name: KEY1
    valueFrom:
      secretKeyRef:
        name: mysecret
        key: key1
  - name: KEY2
    valueFrom:
      secretKeyRef:
        name: mysecret
        key: key2
```
