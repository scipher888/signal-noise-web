import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe5-rigor-llm-judges', 'artifact': 'episode', 'type': 'objection', 'story': 'Society', 'quote': None}


def check(ctx):
    # Objection: if the rigor score is cited, it must be framed as LLM ratings of prose, not human peer review.
    s = ctx.find('society', r'blinded LLM rubric ratings of prose, not expert human peer review')
    if not ctx.art_has(r'rigor'): return ctx.ok(None, None, 'rigor score not cited')
    return ctx.ok('society', s, 'framed as LLM judges') if ctx.art_has(r'LLM judges|language model judges') else ctx.fail('society', s, 'rigor score cited without LLM-judge caveat')


if __name__ == '__main__':
    run_cli(CLAIM, check)
