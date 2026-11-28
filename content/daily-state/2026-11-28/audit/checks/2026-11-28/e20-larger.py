import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-larger', 'artifact': 'episode', 'type': 'comparison', 'story': 'Mir2k', 'quote': 'The larger campaign, named Mir2k'}


def check(ctx):
    return ctx.require('gguf', r'The largest campaign, Mir2k', note='Larger by downloads, not by number of repositories.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
