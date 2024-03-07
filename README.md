# API Alerts - Python

APIAlerts require the use of API Keys to integrate with your projects.

Copy your API Key from the projects page in the mobile app.

Get the App
- Android - [Play Store](https://play.google.com/store/apps/details?id=com.apialerts)
- iOS/Mac - [App Store](https://apps.apple.com/us/app/magpie-api-alerts/id6476410789)

Links
- [Integrations](https://apialerts.com/integrations)

## Installation

Available on PyPI

```bash
pip install apialerts
```


### Sample usage

```python
from apialerts import ApiAlerts, AlertRequest

def alerts_basic():
    # Create the ApiAlerts instance
    alerts = ApiAlerts()
    # Construct your message
    data = AlertRequest(
        message='Payment Received $10'
    )
    # Send alert to you project via your API Key
    alerts.send(data, 'PROJECT_API_KEY')
```


### Advanced usage

```python
from apialerts import ApiAlerts, AlertRequest

def alerts_advanced():
    alerts = ApiAlerts()
    # Set a default project API Key and enable logging
    alerts.configure('DEFAULT_API_KEY', True)
    # Construct your alert with additional tags and a link
    data = AlertRequest(
        message='Payment Received $10',
        tags=['Growth', 'Promotion'],
        link='https://apialerts.com'
    )
    # Send alert to default project specified in configure()
    alerts.send(data)
    # Or, send alert to an alternate project
    alerts.send(data, 'ALTERNATE_API_KEY')
```