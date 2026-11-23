import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-outside-commenters-tokenizers', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'as outside commenters quickly pointed out, different labs use different tokenizers and data mixtures'}


def check(ctx):
    s1 = ctx.find('sama', r'every lab tokenizes and trains differently')
    s2 = ctx.find('openai', r'different data mixtures')
    if s1 and s2:
        return ctx.ok('sama', s1, 'Outside reply cites different tokenizers/training and OpenAI notes different data mixtures')
    return ctx.need('sama', s1 or s2, 'Could not confirm both tokenizer and data-mixture points')


if __name__ == '__main__':
    run_cli(CLAIM, check)
