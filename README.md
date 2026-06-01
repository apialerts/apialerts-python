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

### Global singleton

Call `configure` once at startup, then use `send` / `send_async` anywhere.

```python
from apialerts import ApiAlerts, Event

ApiAlerts.configure('your-api-key')

# Fire-and-forget. Never raises, silently drops errors.
# Pass debug=True to configure() to log them via stdlib logging.
ApiAlerts.send(Event(message='Deploy complete'))

# Or get the result back. Never raises, check result.success.
result = await ApiAlerts.send_async(Event(message='Deploy complete'))
if result.success:
    print(f'Sent to {result.workspace} ({result.channel})')
else:
    print(f'Error: {result.error}')
```

### Enable debug logging

```python
ApiAlerts.configure('your-api-key', debug=True)
```

The SDK uses Python's stdlib `logging` module under the logger name `'apialerts'`. Critical errors (missing API key, not yet configured) always log via `logger.error(...)`. Debug success/warning messages log via `logger.info(...)` and only fire when `debug=True`. Configure the `apialerts` logger to route output anywhere you like:

```python
import logging
logging.getLogger('apialerts').setLevel(logging.INFO)
logging.basicConfig()
```

### Event fields

Only `message` is required. All other fields are optional and omitted from the request body when not set.

```python
from apialerts import Event

event = Event(
    message='Deploy complete',
    channel='releases',
    event='ci.deploy',
    title='Deployed',
    tags=['CI/CD', 'Python'],
    link='https://github.com/apialerts/apialerts-python/actions',
    data={'version': '1.2.0'},
)

result = await ApiAlerts.send_async(event)
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `str` | Yes | Human-readable notification text. This is what appears on the push notification lock screen. |
| `channel` | `str` | No | Workspace channel the push notification fires on. Defaults to the workspace default channel when omitted. |
| `event` | `str` | No | Identifies what kind of thing happened. Optional but recommended. Use dotted notation (e.g. `ci.deploy.success`, `payment.failed`, `user.signup`) so routing rules can match glob patterns like `ci.*` or `*.failed`. |
| `title` | `str` | No | Short headline some destinations render separately from the message body. |
| `tags` | `list[str]` | No | Categorisation tags for filtering and search. |
| `link` | `str` | No | URL associated with the event. Available as a deeplink for push notifications and as a call-to-action for routed destinations. |
| `data` | `dict[str, Any]` | No | Arbitrary key-value metadata. Available to non-push destinations for templating (Slack message bodies, email templates, webhook payloads). |

### Send to multiple workspaces

Pass an `api_key` as the optional second argument to override the configured key for one call.

```python
ApiAlerts.send(Event(message='Deploy complete'), api_key='other-workspace-api-key')

result = await ApiAlerts.send_async(
    Event(message='Deploy complete'),
    api_key='other-workspace-api-key',
)
```

## API

| Method | Description |
|---|---|
| `ApiAlerts.configure(api_key, debug=False)` | Initialise the singleton. First call wins; subsequent calls are no-ops. |
| `ApiAlerts.send(event, api_key=None)` | Fire-and-forget. Never raises, drops errors silently unless `debug` is on. |
| `ApiAlerts.send_async(event, api_key=None)` | Awaitable, returns `SendResult`. Never raises; check `result.success`. |

### SendResult fields

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
