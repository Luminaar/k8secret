from base64 import b64encode
from textwrap import dedent
from typing import Dict


def parse(input_string: str) -> Dict[str, str]:
    """Try to parse input into a dictionary of `variable`:`value` pairs. Raise
    ValueError if parsing fails for some reason."""

    for sep in ["\r\n", "\n", ";", ","]:
        lines = input_string.split(sep)
        if len(lines) > 1:
            break
    else:  # If none of the characters produced multiple items
        lines = [input_string]

    pairs = {}
    for line in lines:
        line = line.replace("export ", "")

        key = value = None
        for char in ["=", ":", "\t"]:
            try:
                key, value = line.split(char)
                break
            except ValueError:
                pass

        if key is not None and value is not None:
            pairs[key] = value.strip("\"'")

    return pairs


def create_secret_object(name: str, variables: Dict[str, str]) -> str:
    """Return yaml file conent for `secret` object."""

    text = dedent(
        """\
        ---
        apiVersion: v1
        kind: Secret
        metadata:
          name: {}
        type: Opaque
        data:"""
    ).format(name)

    for key, value in variables.items():
        encoded_value = b64encode(value.encode("utf-8")).decode("utf-8")
        text += "\n  {}: {}".format(key, encoded_value)

    return text


def create_config_object(name: str, variables: Dict[str, str]) -> str:
    """Return yaml file conent for `secret` object."""

    text = dedent(
        """\
        ---
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: {}
        data:"""
    ).format(name)

    for key, value in variables.items():
        text += f'\n  {key}: "{value}"'

    return text


def create_env_map(name: str, config: bool = False) -> str:

    ref = "configMapRef" if config else "secretRef"

    text = dedent(
        f"""\
        ---
        envFrom:
          - {ref}:
              name: {name}"""
    )

    return text
