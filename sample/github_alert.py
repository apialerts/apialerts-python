import asyncio
import sys
import os
import argparse

print(f"Current working directory: {os.getcwd()}")
print(f"sys.path before modification: {sys.path}")

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
# Add the src directory to the Python path
sys.path.insert(0, src_dir)

# Print sys.path after modification to ensure src is added
print(f"sys.path after modification: {sys.path}")

from src.apialerts.apialerts import AlertRequest, ApiAlerts
from src.apialerts.models import ValidationError


def parse_args():
    parser = argparse.ArgumentParser(description="Send alert on build, release, or publish")
    parser.add_argument('--build', action='store_true', help='Build the project')
    parser.add_argument('--release', action='store_true', help='Release the project')
    parser.add_argument('--publish', action='store_true', help='Publish the project')
    return parser.parse_args()

def get_api_key():
    return os.getenv('APIALERTS_API_KEY')

def create_event(build, release, publish):
    event_channel = 'developer'
    event_message = 'apialerts-python'
    event_tags = []
    event_link = 'https://github.com/apialerts/apialerts-python/actions'

    if build:
        event_message = 'Python - PR build success'
        event_tags = ['CI/CD', 'Python', 'Build']
    elif release:
        event_message = 'Python - Build for publish success'
        event_tags = ['CI/CD', 'Python', 'Build']
    elif publish:
        event_channel = 'releases'
        event_message = 'Python - GitHub publish success'
        event_tags = ['CI/CD', 'Python', 'Deploy']

    return AlertRequest(
        message=event_message,
        channel=event_channel,
        tags=event_tags,
        link=event_link
    )

async def main():
    args = parse_args()
    api_key = get_api_key()

    if not args.build and not args.release and not args.publish:
        print('Usage: python github_alert.py --build|--release|--publish')
        return


    if not api_key:
        print('Error: APIALERTS_API_KEY environment variable is not set')
        return

    api_alerts = ApiAlerts()
    api_alerts.configure(api_key, True)
    event = create_event(args.build, args.release, args.publish)

    try:
        await api_alerts.send_async(event)
    except ValidationError as e:
        print('Error:', e)


if __name__ == '__main__':
    asyncio.run(main())