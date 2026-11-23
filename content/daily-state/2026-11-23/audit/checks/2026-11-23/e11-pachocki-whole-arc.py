import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-pachocki-whole-arc', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'Pachocki argues that this single curve explains the whole arc of modern AI'}


def check(ctx):
    s = ctx.find('openai', r'key to understanding the arc of advances in AI')
    return ctx.need('openai', s, 'Source says tracking better compressors is "key to understanding the arc" and "largely described" by perplexity, while noting it omits post-training; human check needed on "whole arc"')


if __name__ == '__main__':
    run_cli(CLAIM, check)
