import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-no-rsa-threat', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google factoring', 'quote': "Google's two factoring papers do not threaten RSA"}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:both|two) .*factoring)(?=.*(?:do not threaten|no practical .* on|do not break) RSA)', note='Subexponential alone does not decide practical impact at RSA key sizes.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
