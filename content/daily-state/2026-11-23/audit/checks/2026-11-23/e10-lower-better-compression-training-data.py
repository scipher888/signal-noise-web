import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-lower-better-compression-training-data', 'artifact': 'episode', 'type': 'comparison', 'story': 'OpenAI Perplexity', 'quote': 'Lower numbers mean better compression of the training data'}


def check(ctx):
    s_train = ctx.find('openai', r'compression of (?:the )?training data')
    if s_train:
        return ctx.ok('openai', s_train)
    s_lower = ctx.find('openai', r'lower perplexity means better (predictions|compression)')
    s_held = ctx.find('openai', r'held-out dataset|predicting unseen data')
    if s_lower and s_held:
        return ctx.need(
            'openai',
            ' … '.join([s_lower, s_held]),
            'Source ties lower perplexity to better predictions and to compression by predicting unseen or held-out data, not to compression of the training data',
        )
    if s_lower:
        return ctx.ok('openai', s_lower)
    return ctx.need('openai', None, 'Could not find source support for lower numbers meaning better compression')


if __name__ == '__main__':
    run_cli(CLAIM, check)
