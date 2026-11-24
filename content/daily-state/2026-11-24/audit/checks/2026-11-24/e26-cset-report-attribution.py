import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-cset-report-attribution', 'artifact': 'episode', 'type': 'attribution', 'story': 'CSET Cyber Report', 'quote': "an independent report from Georgetown's Center for Security and Emerging Technology"}


def check(ctx):
    return ctx.require('openai', r'Center for Security and Emerging Technology', r'georgetown\.edu')


if __name__ == '__main__':
    run_cli(CLAIM, check)
