import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e46-neon-absent', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Blueprint', 'quote': "Google's newly released Gemini 4 Neon isn't even on the board yet"}


def check(ctx):
    if not ctx.absent('blueprint', r'Neon'): return ctx.fail('blueprint', ctx.find('blueprint', r'Neon'), 'Neon is on the leaderboard')
    r = ctx.find('andon', r'Google released the best model in the world, Gemini 4 Neon')
    return ctx.ok('andon', r, 'no "Neon" anywhere in the leaderboard page; "newly released" comes from a reply in the @andonlabs thread') if r else ctx.need('andon', None, 'release not sourced')


if __name__ == '__main__':
    run_cli(CLAIM, check)
