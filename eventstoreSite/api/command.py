from esdbclient import NewEvent
import json


def createCommand(client, stream_name, expected_position, event_type, event_data, event_metadata):
    stream_position = client.get_stream_position(
        stream_name=stream_name
    )
    if stream_position >= expected_position: expected_position = stream_position
    event1 = NewEvent(
        type=event_type,
        data=json.dumps(event_data, indent=2).encode('utf-8'),
        metadata=json.dumps(event_metadata, indent=2).encode('utf-8'),
    )

    commit_position = client.append_events(
        stream_name=stream_name,
        expected_position=expected_position,
        events=[event1]
    )
    return commit_position
