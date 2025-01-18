import asyncio
import os
import argparse

from apialerts import ApiAlerts
from apialerts.event import Event

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
        event_message = 'Python - PyPI publish success'
        event_tags = ['CI/CD', 'Python', 'Deploy']

    return Event(
        message=event_message,
        channel=event_channel,
        tags=event_tags,
        link=event_link
    )

async def main():
    args = parse_args()
    api_key = get_api_key()

    if not args.build and not args.release and not args.publish:
        print('Usage: python sample/github_alert.py --build|--release|--publish')
        return


    if not api_key:
        print('Error: APIALERTS_API_KEY environment variable is not set')
        return

    api_alerts = ApiAlerts()
    api_alerts.configure(api_key, True)
    event = create_event(args.build, args.release, args.publish)

    await api_alerts.send_async(event)


if __name__ == '__main__':
    asyncio.run(main())