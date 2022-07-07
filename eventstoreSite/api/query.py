def query(client, stream_name, position, backwards, limit):
    events = list(
        client.read_stream_events(
            stream_name,
            position,
            backwards,
            limit
        )
    )
    return events
