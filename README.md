# API Alerts • Python Client

[![PyPI](https://img.shields.io/pypi/v/apialerts)](https://pypi.org/project/apialerts/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[PyPI](https://pypi.org/project/apialerts/) • [GitHub](https://github.com/apialerts/apialerts-python) • [API Alerts](https://apialerts.com)

Effortless project notifications. Send once, deliver everywhere.

## Installation

```bash
pip install apialerts
```

## Quick Start

```python
from apialerts import ApiAlerts, Event

ApiAlerts.configure('your-api-key')
ApiAlerts.send(Event(message='Deploy complete'))
```

## Usage

### Global singleton (recommended)

Call `configure` once at startup, then use `send` / `send_async` anywhere.

```python
from apialerts import ApiAlerts, Event

ApiAlerts.configure('your-api-key')

# Fire-and-forget — never raises
ApiAlerts.send(Event(message='Deploy complete'))

# Or get the result back — also never raises
result = await ApiAlerts.send_async(Event(message='Deploy complete'))
if result.success:
    print(f'Sent to {result.workspace} ({result.channel})')
else:
    print(f'Error: {result.error}')
```

### Event fields

Only `message` is required. All other fields are optional.

```python
from apialerts import Event

event = Event(
    message='Deploy complete',
    channel='releases',
    event='ci.deploy',
    title='Deployed',
    tags=['CI/CD', 'Python'],
    link='https://github.com/apialerts/apialerts-python/actions',
    data={'version': '2.0.0'},
)
```

| Field     | Type             | Required | Description                      |
|-----------|------------------|----------|----------------------------------|
| `message` | `str`            | Yes      | Main notification message        |
| `channel` | `str`            | No       | Target channel name              |
| `event`   | `str`            | No       | Event key (e.g. `ci.deploy`)     |
| `title`   | `str`            | No       | Short title                      |
| `tags`    | `list[str]`      | No       | Categorisation tags              |
| `link`    | `str`            | No       | URL attached to the notification |
| `data`    | `dict[str, Any]` | No       | Arbitrary key-value metadata     |

### Instance-based client

Use `ApiAlertsClient` directly when you need multiple clients or full
lifecycle control.

```python
from apialerts import ApiAlertsClient, Event

client = ApiAlertsClient('your-api-key', debug=True)
result = await client.send_async(Event(message='Deploy complete'))
if result.success:
    print(f'Sent to {result.workspace} ({result.channel})')
else:
    print(f'Error: {result.error}')
```

### Send to multiple workspaces

```python
result = await ApiAlerts.send_with_key_async('other-api-key', Event(message='Deploy complete'))
if result.success:
    print(f'Sent to {result.workspace} ({result.channel})')
```

### SendResult fields

`send_async()` and `send_with_key_async()` always return a `SendResult` — they never raise.

| Field       | Type            | Description                            |
|-------------|-----------------|----------------------------------------|
| `success`   | `bool`          | `True` if the alert was delivered      |
| `workspace` | `str` or `None` | Workspace name (present on success)    |
| `channel`   | `str` or `None` | Channel name (present on success)      |
| `warnings`  | `list[str]`     | Non-fatal warnings from the server     |
| `error`     | `str` or `None` | Error message (present on failure)     |

## Links

- [Documentation](https://apialerts.com/docs)
- [Sign up](https://apialerts.com)
- [GitHub Issues](https://github.com/apialerts/apialerts-python/issues)
