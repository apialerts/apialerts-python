"""Integration test sample - requires APIALERTS_API_KEY env var."""
from __future__ import annotations

import argparse
import asyncio
import os
import sys

from apialerts import ApiAlerts, Event


async def main() -> None:
    parser = argparse.ArgumentParser(description='API Alerts Python SDK sample')
    parser.add_argument('--build', action='store_true', help='Send build notification')
    parser.add_argument('--release', action='store_true', help='Send release notification')
    parser.add_argument('--publish', action='store_true', help='Send publish notification')
    parser.add_argument('--integration-tests', action='store_true', help='Run integration tests (default when no flag is set)')
    parser.add_argument('--channel', default='testing', help='Channel for integration test sends')
    args = parser.parse_args()

    api_key = os.environ.get('APIALERTS_API_KEY', '')
    if not api_key:
        print('Error: APIALERTS_API_KEY environment variable is not set', file=sys.stderr)
        sys.exit(1)

    ApiAlerts.configure(api_key, debug=True)

    link = 'https://github.com/apialerts/apialerts-python/actions'

    if args.build:
        result = await ApiAlerts.send_async(Event(
            channel='developer',
            event='ci.build',
            title='Build Passed',
            message='Python - PR build success',
            tags=['CI/CD', 'Python', 'Build'],
            link=link,
        ))
        if not result.success:
            print(f'Error: {result.error}', file=sys.stderr)
            sys.exit(1)
        print(f'✓ Sent to {result.workspace} ({result.channel})')

    elif args.release:
        result = await ApiAlerts.send_async(Event(
            channel='developer',
            event='ci.release',
            title='Release Build Passed',
            message='Python - Build for publish success',
            tags=['CI/CD', 'Python', 'Build'],
            link=link,
        ))
        if not result.success:
            print(f'Error: {result.error}', file=sys.stderr)
            sys.exit(1)
        print(f'✓ Sent to {result.workspace} ({result.channel})')

    elif args.publish:
        result = await ApiAlerts.send_async(Event(
            channel='releases',
            event='ci.publish',
            title='Published',
            message='Python - PyPI publish success',
            tags=['CI/CD', 'Python', 'Deploy'],
            link=link,
        ))
        if not result.success:
            print(f'Error: {result.error}', file=sys.stderr)
            sys.exit(1)
        print(f'✓ Sent to {result.workspace} ({result.channel})')

    elif args.integration_tests:
        r1 = await ApiAlerts.send_async(Event(message='Python SDK - minimal', channel=args.channel))
        if not r1.success:
            print(f'Error (minimal): {r1.error}', file=sys.stderr)
            sys.exit(1)
        print(f'✓ sent to {r1.workspace} ({r1.channel})')

        r2 = await ApiAlerts.send_async(Event(
            message='Python SDK - full',
            channel=args.channel,
            event='sdk.test',
            title='Integration Test',
            tags=['CI/CD', 'Python'],
            link=link,
            data={'version': '2.0.0'},
        ))
        if not r2.success:
            print(f'Error (full): {r2.error}', file=sys.stderr)
            sys.exit(1)
        print(f'✓ sent to {r2.workspace} ({r2.channel})')

    else:
        print('Error: pass --build, --release, --publish, or --integration-tests', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
