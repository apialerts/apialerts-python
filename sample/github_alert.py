import os
import argparse
from src.apialerts.apialerts import ApiAlerts, AlertRequest, ValidationError

def parse_args():
    parser = argparse.ArgumentParser(description="Send alert on build, release, or publish")
    parser.add_argument('--build', action='store_true', help='Build the project')
    parser.add_argument('--release', action='store_true', help='Release the project')
    parser.add_argument('--publish', action='store_true', help='Publish the project')
    return parser.parse_args()

def get_api_key():
    return os.getenv('APIALERTS_API_KEY')

def create_event(build, release, publish):
    event_channel = "developer"
    event_message = "apialerts-python"
    event_tags = []
    event_link = "https://github.com/apialerts/apialerts-python/actions"

    if build:
        event_message = "Python - PR build success"
        event_tags = ["CI/CD", "Python", "Build"]
    elif release:
        event_message = "Python - Build for publish success"
        event_tags = ["CI/CD", "Python", "Build"]
    elif publish:
        event_channel = "releases"
        event_message = "Python - GitHub publish success"
        event_tags = ["CI/CD", "Python", "Deploy"]

    return AlertRequest(
        message=event_message,
        channel=event_channel,
        tags=event_tags,
        link=event_link
    )

def main():
    args = parse_args()
    api_key = get_api_key()

    if not api_key:
        print("Error: APIALERTS_API_KEY environment variable is not set")
        return

    api_alerts = ApiAlerts()
    api_alerts.configure(api_key)

    if not args.build and not args.release and not args.publish:
        print("Usage: python github_alert.py --build|--release|--publish")
        return

    event = create_event(args.build, args.release, args.publish)

    try:
        api_alerts.send(event)
        print("Alert sent successfully.")
    except ValidationError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()