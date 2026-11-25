import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-same-model', 'artifact': 'episode', 'type': 'comparison', 'story': 'Discovery vs. reliability', 'quote': 'the same frontier AI model crack a 218-year-old historical mystery in twenty-two minutes and design new proteins that actually bind in a wet lab, yet still miscount a handful of objects in a simple picture'}


def check(ctx):
    q = ctx.find('openai', r'structures designed by a pre-released version of GPT.6\.2')
    v = ctx.find('deepmind', r'GPT.6\.2 Astra.*miscount(?:ed|s).*objects')
    if q and not v: return ctx.fail('openai', q, 'The lab report identifies a prerelease GPT-6.2, not the same Astra configuration; the counting-error breakdown is pooled, not an Astra-specific incident.')
    return ctx.need('deepmind', v, 'Verify model identity and the individual visual failure across all three reports.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
