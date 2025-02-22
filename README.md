# API Alerts • Python Client

[GitHub Repo](https://github.com/apialerts/apialerts-python) • [PyPI](https://pypi.org/project/apialerts/)

## Installation

Install the latest apialerts package from PyPI

```bash
pip install apialerts
```

### Initialize the client

```python
from apialerts import ApiAlerts

# Configure the client with a default workspace API Key
ApiAlerts.configure('your-api-key')

# Or, Configure the client with a default workspace API Key with logging enabled
ApiAlerts.configure('your-api-key', debug=True)
```

Note: The ApiAlerts class is implemented as a singleton.


### Send Events

```python
from apialerts import ApiAlerts, ApiAlertsEvent

# Construct your alert with additional channel, tags and a link
data = ApiAlertsEvent(
    message='Payment Received',   # required
    channel='revenue',            # optional, uses the default channel if not provided
    tags=['Growth', 'Promotion'], # optional
    link='https://stripe.com'     # optional
)
# Send alert to your workspace using the default API Key
ApiAlerts.send(data)

# Or, Send alert to you project with an alternate API Key
ApiAlerts.send_with_api_key('your-api-key', data)
```

The send_async() and send_with_api_key_async() methods are also available if you need to wait for a successful execution. However, the send() functions are generally always preferred.
