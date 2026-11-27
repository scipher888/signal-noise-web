import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-praised-release', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': 'praising OpenAI for sharing normally secret data'}


def check(ctx):
    return ctx.require('metr', r'no frontier developer had previously published how the pretraining loss', r'typically considered highly commercially sensitive', r'we think publishing information about pretraining loss is very valuable', r'OpenAI recently published the base-model log-perplexity')


if __name__ == '__main__':
    run_cli(CLAIM, check)
