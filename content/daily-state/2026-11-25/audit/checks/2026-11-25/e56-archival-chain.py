import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e56-archival-chain', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': "In twenty-two minutes, the model linked a Montreal fur trader's diary, a century-old letter, and a 2014 thesis footnote to identify an obscure French aristocrat, vicomte de Chabot"}


def check(ctx):
    q = ctx.find('gpt62', r'century-old book of letters|published in a document collection nearly a hundred years ago')
    if q: return ctx.fail('gpt62', q, 'The collection, not the letter, was about a century old. The thesis footnote was traced as a lead to the journal.')
    return ctx.require('gpt62', r'22 minutes and 1 second later.*vicomte de Chabot', r'diary of Joseph Frobisher.*fur trader.*Montreal', r'(?:century-old|hundred-year-old) letter\b', r'single footnote in a 2014 PhD thesis', r'minor French aristocrat')


if __name__ == '__main__':
    run_cli(CLAIM, check)
