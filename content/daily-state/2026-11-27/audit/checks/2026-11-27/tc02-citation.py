import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc02-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 2', 'quote': None}
URL = 'https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback'
ALLOWED = ['https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/', 'https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/', 'https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback', 'https://www.anthropic.com/claude-fable-and-mythos-5-2', 'https://x.com/RealAstropulse/status/2126119408997466389', 'https://x.com/capital_vmv/status/2126025365017801155', 'https://x.com/ibab/status/2126077013857538266', 'https://x.com/ptrCast/status/2126021553116881326', 'https://x.com/ramez/status/2126112326172442974', 'https://x.com/ramez/status/2126112999978995910', 'https://x.com/tobyordoxford/status/2126063832518852763']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
