# apialerts-python

Python client for the [apialerts.com](https://apialerts.com/) platform

[Docs](https://apialerts.com/docs/python) • [GitHub](https://github.com/apialerts/apialerts-python) • [PyPI](https://pypi.org/project/apialerts/)

## Installation

Install the latest apialerts package from PyPI

```bash
pip install apialerts==<latest-version>
```

### Initialize the client

```python
from apialerts import ApiAlerts

alerts = ApiAlerts()
# Set a default project API Key and toggle logging
alerts.configure('Send Event', False)
```

### Send Events

```python
# Construct your alert with additional tags and a link
data = AlertRequest(
    message='Payment Received $10',
    tags=['Growth', 'Promotion'],    // optional
    link='https://apialerts.com'     // optional
)
    
# Send alert to your workspace using the default API Key
alerts.send(data)

# or, Send alert to you project with an alternate API Key
alerts.send(data, 'your-api-key')
```
