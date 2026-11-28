import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't10-release-cause', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GGUF scan', 'quote': 'prompting the release of the open-source scanner gguf-radar'}


def check(ctx):
    q = ctx.find('framing', r'Open-source MIT-licensed scanner and sanitizer repository published by the Malspark author')
    if q and ctx.absent('gguf', r'(?:in response to|because of|prompted by).*gguf-radar|gguf-radar.*(?:in response to|because of)'): return ctx.fail('framing', q, 'Publication and common authorship are documented; the claimed causal sequence is not.')
    return ctx.require('gguf', r'open-source tool gguf-radar', r'(?:in response to|because of|prompted by).*gguf-radar|gguf-radar.*(?:in response to|because of)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
