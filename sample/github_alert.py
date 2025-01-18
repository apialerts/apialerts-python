import asyncio
import os
import argparse
from apialerts import ApiAlerts
from apialerts.models.event import ApiAlertsEvent

# Call from GitHub Actions as `python sample/github_alert.py --build`

async def main():
    # Parse command-line arguments
    args = parse_args()

    # Retrieve the API key from environment variables
    api_key = os.getenv('APIALERTS_API_KEY')

    # Check if any of the required arguments are provided
    if not args.build and not args.release and not args.publish:
        print('Usage: python sample/github_alert.py --build|--release|--publish')
        return

    # Check if the API key is set
    if not api_key:
        print('Error: APIALERTS_API_KEY environment variable is not set')
        return

    # Configure the ApiAlerts client
    ApiAlerts.configure(api_key, debug=True) # debug set to true so the response is shown in GitHub Actions

    # Create an event based on the provided arguments
    event = create_event(args.build, args.release, args.publish)

    # Send the event asynchronously
    await ApiAlerts.send_async(event)

def parse_args():
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description="Send alert on build, release, or publish")
    parser.add_argument('--build', action='store_true', help='Build the project')
    parser.add_argument('--release', action='store_true', help='Release the project')
    parser.add_argument('--publish', action='store_true', help='Publish the project')
    return parser.parse_args()

def create_event(build, release, publish):
    # Define default event properties
    event_channel = 'developer'
    event_message = 'apialerts-python'
    event_tags = []
    event_link = 'https://github.com/apialerts/apialerts-python/actions'

    # Customize the event based on the provided arguments
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

    # Create and return the ApiAlertsEvent object
    return ApiAlertsEvent(
        message=event_message,
        channel=event_channel,
        tags=event_tags,
        link=event_link
    )

if __name__ == '__main__':
    # Run the main function asynchronously
    asyncio.run(main())