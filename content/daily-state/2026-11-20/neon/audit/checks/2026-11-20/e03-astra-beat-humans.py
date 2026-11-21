import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-astra-beat-humans', 'artifact': 'episode', 'type': 'comparison', 'story': 'Blueprint', 'quote': 'GPT-6.2 Astra beat humans at 3D spatial reasoning'}


def check(ctx):
    # Framed as a feed headline. Leaderboard: Astra 0.614 vs human 0.586 (human on 12 of 50 apartments).
    a = ctx.find('blueprint', r'GPT-6\.2 Astra 0\.614'); h = ctx.find('blueprint', r'Human\* 0\.586')
    g = ctx.find('gdb', r'exceeding human baseline')
    if a and h and g: return ctx.ok('blueprint', a + ' … ' + h, 'headline framing matches @gdb: "' + g + '"; caveat (12-apartment subset) is checked in o-e4')
    return ctx.need('blueprint', a, 'scores not found')


if __name__ == '__main__':
    run_cli(CLAIM, check)
