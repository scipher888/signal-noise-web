import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's01-alphaxiv-watched', 'artifact': 'short', 'type': 'attribution', 'story': 'Society', 'quote': 'alphaXiv watched 936 AI agents run their own preprint server'}


def check(ctx):
    return ctx.require('society', r'Today we.re launching a preprint server built specifically for AI agents', r'nearly 1,000 agents from 35 labs .* on this server', note='alphaXiv launched the server and co-led the study (alphaXiv/MIT/Stanford)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
