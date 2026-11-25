import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e54-humphries-test', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': "historian Mark Humphries describes giving GPT-6.2 Astra an anonymous 1808 sketchbook from Yale's Beinecke Library"}


def check(ctx):
    if not ctx.find('emollick', r'Historian Mark Humphries asked GPT-6\.2 Astra to look at an anonymous 1808 sketchbook at Yale'): return ctx.need('emollick', None, 'Verify attribution.')
    return ctx.require('gpt62', r'GPT-6\.2 Astra.*anonymous 1808 sketchbook held at Yale.s Beinecke Library', r'I gave GPT-6\.2 Astra access to the images of the sketchbook')


if __name__ == '__main__':
    run_cli(CLAIM, check)
