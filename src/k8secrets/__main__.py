import argparse
import sys

from .secrets import create_env_map, create_secret_object, parse


DESCRIPTION = """\
description:

'k8secrets' takes a secret object name and a list of variables as input:

    k8secrets mysecret -l KEY1=value1,KEY2=value2


It can also read the variables from stdin (you can pipe input into it):

    echo KEY1=value1,KEY2=value2 | k8secrets mysecret

Variable list is a list of key/value pairs in any of the following formats:

    KEY=value
    export KEY=value - found in .env files on Linux
    KEY:value
    KEY\\tvalue - separated by a tab character

If value is wrapped in single or double quotes they will be ignored. Pairs can
be separated either by a newline character (Unix or Windows) or a comma or a
semicolon.

'k8secrets' prints output to stdout. The output is valid yaml and contains
two sections. First is a complete k8s secret object:

    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: mysecret
    type: Opaque
    data:
      key1: dmFsdWUx
      key2: dmFsdWUy

The second is an 'env' section with references to the secret object that you
can use in your deployments or cronjobs:

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
"""


PARSER = argparse.ArgumentParser(
    description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter
)
PARSER.add_argument("secret_name", type=str)
PARSER.add_argument("-l", type=str, required=False, dest="variable_list")


def main():

    args = PARSER.parse_args()
    secret_name: str = args.secret_name
    variable_list: str = args.variable_list

    if not variable_list and not sys.stdin.isatty():
        variable_list = "".join(sys.stdin.readlines()).strip("\n")
    elif not variable_list:
        sys.exit(
            "Provide variable list with via '-l' argument or pipe something into stdin"
        )

    variables = parse(variable_list)

    print()
    print(create_secret_object(secret_name, variables))
    print()
    print(create_env_map(secret_name, variables))


if __name__ == "__main__":
    main()
