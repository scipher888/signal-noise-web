import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-recursive-research-oversight-2027', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'recursive AI research could outrun human oversight by 2027'}


def check(ctx):
    s = ctx.find('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements')
    return ctx.need('openai', s, 'OpenAI warns of 2027 pretraining breakthroughs outpacing alignment/monitoring, while distinguishing this from full recursive self-improvement with no human oversight')


if __name__ == '__main__':
    run_cli(CLAIM, check)
