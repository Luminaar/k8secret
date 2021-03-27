from textwrap import dedent

from k8secrets.secrets import create_config_object, create_secret_object

NAME = "mysecret"
PAIRS = {"KEY1": "value1", "KEY2": "value2"}


def test_create_secret_object():

    content = dedent(
        """\
        ---
        apiVersion: v1
        kind: Secret
        metadata:
          name: {}
        type: Opaque
        data:
          KEY1: dmFsdWUx
          KEY2: dmFsdWUy""".format(
            NAME
        )
    )

    result = create_secret_object(NAME, PAIRS)
    assert result == content


def test_create_config_object():

    content = dedent(
        '''\
        ---
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: {}
        data:
          KEY1: "value1"
          KEY2: "value2"'''.format(
            NAME
        )
    )

    result = create_config_object(NAME, PAIRS)
    assert result == content
