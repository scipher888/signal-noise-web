import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e55-wednesday-paragraph', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson crypto warning', 'quote': "The real alarm came from a brief paragraph in Aaronson's Wednesday post"}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*Wednesday)(?=.*brief paragraph)(?=.*(?:cryptograph|alarm|warning))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
