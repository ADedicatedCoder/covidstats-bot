def returnPing(client):
    return f"Pong! ({round(client.latency * 1000)}ms)"
