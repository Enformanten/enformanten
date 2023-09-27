from tilly.api.helpers import merge


def test_merge_dict():
    list1 = [
        {"conversation_code": "A1", "data1": "value1"},
        {"conversation_code": "A2", "data1": "value1"},
    ]
    list2 = [{"conversation_code": "A1", "data2": "value2"}]

    result = merge(list1, list2)
    assert result == [{"conversation_code": "A1", "data1": "value1", "data2": "value2"}]
