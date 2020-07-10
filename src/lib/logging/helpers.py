from datetime import datetime


def logprocessor_add_timestamp(_, __, event_dict):
    event_dict["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return event_dict
