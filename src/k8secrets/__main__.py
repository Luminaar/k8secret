import argparse
import sys

from .secrets import create_config_object, create_env_map, create_secret_object, parse

DESCRIPTION = """\
description:

'k8secrets' takes an object name and a list of variables as input and creates a
"Secret" Kubernetes object:

    k8secrets mysecret -l KEY1=value1,KEY2=value2

or a "ConfigMap":

    k8secrets --config myconfig -l KEY1=value1,KEY2=value2


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
two sections. First is a complete k8s Secret of ConfigMap object:

    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: mysecret
    type: Opaque
    data:
      key1: dmFsdWUx
      key2: dmFsdWUy

The second is an 'envFrom' section with a reference to the Secret or ConfigMap
object that you can use in your deployments or cronjobs:

    ---
    envFrom:
      - secretRef:
          name: mysecret
"""


PARSER = argparse.ArgumentParser(
    description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter
)
PARSER.add_argument("--config", action="store_true", help="Create a ConfigMap object")
PARSER.add_argument("object_name", type=str)
PARSER.add_argument("-l", type=str, required=False, dest="variable_list")


def main():

    args = PARSER.parse_args()
    object_name = args.object_name
    variable_list = args.variable_list

    if not variable_list and not sys.stdin.isatty():
        variable_list = "".join(sys.stdin.readlines()).strip("\n")
    elif not variable_list:
        sys.exit(
            "Provide variable list with via '-l' argument or pipe something into stdin"
        )

    variables = parse(variable_list)

    print()
    if args.config:
        print(create_config_object(object_name, variables))
    else:
        print(create_secret_object(object_name, variables))
    print()
    print(create_env_map(object_name))


if __name__ == "__main__":
    main()
