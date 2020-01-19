from textwrap import dedent

from k8secrets.secrets import create_secret_object, create_env_map

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
          key1: dmFsdWUx
          key2: dmFsdWUy""".format(
            NAME
        )
    )

    result = create_secret_object(NAME, PAIRS)
    assert result == content


def test_create_env_map():

    content = dedent(
        """\
        ---
        env:
          - name: KEY1
            valueFrom:
              secretKeyRef:
                name: {name}
                key: key1
          - name: KEY2
            valueFrom:
              secretKeyRef:
                name: {name}
                key: key2""".format(
            name=NAME
        )
    )

    result = create_env_map(NAME, PAIRS)
    assert result == content
