import contextlib
import json


def clean_string_values(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                value = value.replace("\\r\\n", "")
                with contextlib.suppress(json.JSONDecodeError):
                    value = json.loads(value)

            cleaned_value = clean_string_values(value)
            obj[key] = cleaned_value
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            cleaned_value = clean_string_values(value)
            obj[i] = cleaned_value
    elif isinstance(obj, str):
        obj = obj.replace("\\r\\n", "").replace('\\"', '"')

    return obj
