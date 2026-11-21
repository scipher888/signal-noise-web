import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-null-results', 'artifact': 'episode', 'type': 'comparison', 'story': 'Society', 'quote': 'published null results as often as positive ones'}


def check(ctx):
    # Claim: PUBLISHED nulls as often as positives. Source: CITED / ACKNOWLEDGED negatives as often.
    return ctx.support_or_contradict('society', r'publish\w* (null|negative)[^.]{0,40}as often as positive',
        r'(cited|acknowledge) negative (results|findings) as often as positive',
        'source says negative results were cited/acknowledged as often as positive ones, not published as often')


if __name__ == '__main__':
    run_cli(CLAIM, check)
