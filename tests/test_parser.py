import pytest
from k8secrets import secrets


SINGLE_PARAMS = [
    "KEY=value",
    "KEY='value'",
    'KEY="value"',
    "export KEY=value",
    "export KEY='value'",
    'export KEY="value"',
    "KEY:value",
    'KEY:"value"',
    "KEY\tvalue",
    "KEY\t'value'",
    'KEY\t"value"',
]
SINGLE_RESULT = {"KEY": "value"}


@pytest.mark.parametrize("input_string", SINGLE_PARAMS)
def test_parser_single(input_string):

    assert secrets.parse(input_string) == SINGLE_RESULT


MULTI_PARAMS = [
    "KEY1=value,KEY2=value",
    "KEY1=value,KEY2='value'",
    'KEY1="value",KEY2="value"',
    "export KEY1=value,export KEY2=value",
    "export KEY1='value',export KEY2='value'",
    'export KEY1="value",export KEY2="value"',
    "KEY1:value,KEY2:value",
    "KEY1:'value',KEY2:'value'",
    'KEY1:"value",KEY2:"value"',
    "KEY1\tvalue,KEY2\tvalue",
    "KEY1\t'value',KEY2\t'value'",
    'KEY1\t"value",KEY2\t"value"',
    "KEY1=value\nKEY2=value",
    "KEY1='value'\nKEY2='value'",
    'KEY1="value"\nKEY2="value"',
    "export KEY1=value\nexport KEY2=value",
    "export KEY1='value'\nexport KEY2='value'",
    'export KEY1="value"\nexport KEY2="value"',
    "KEY1:value\nKEY2:value",
    "KEY1:'value'\nKEY2:'value'",
    'KEY1:"value"\nKEY2:"value"',
    "KEY1\tvalue\nKEY2\tvalue",
    "KEY1\t'value'\nKEY2\t'value'",
    'KEY1\t"value"\nKEY2\t"value"',
    "KEY1=value\r\nKEY2=value",
    "KEY1='value'\r\nKEY2='value'",
    'KEY1="value"\r\nKEY2="value"',
    "export KEY1=value\r\nexport KEY2=value",
    "export KEY1='value'\r\nexport KEY2='value'",
    'export KEY1="value"\r\nexport KEY2="value"',
    "KEY1:value\r\nKEY2:value",
    "KEY1:'value'\r\nKEY2:'value'",
    'KEY1:"value"\r\nKEY2:"value"',
    "KEY1\tvalue\r\nKEY2\tvalue",
    "KEY1\t'value'\r\nKEY2\t'value'",
    'KEY1\t"value"\r\nKEY2\t"value"',
]
MULTI_RESULT = {"KEY1": "value", "KEY2": "value"}


@pytest.mark.parametrize("input_string", MULTI_PARAMS)
def test_parser_multi(input_string):

    assert secrets.parse(input_string) == MULTI_RESULT


def test_parser_invalid_pair():

    assert secrets.parse("INVALID") == {}


def test_parser_invalid_skip():
    assert secrets.parse("KEY=value,INVALID") == SINGLE_RESULT


def test_parser_repeat_variable():
    assert secrets.parse("KEY=xxx,KEY=value") == SINGLE_RESULT
