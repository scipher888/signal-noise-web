import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-scan-author', 'artifact': 'episode', 'type': 'attribution', 'story': 'GGUF scan', 'quote': 'Security researcher Root0ne at Malspark published the first scan of all 3.27 million public repositories on Hugging Face'}


def check(ctx):
    q = ctx.find('gguf', r'all 3273389 public Hugging Face model repositories')
    if q and ctx.absent('gguf', r'first scan of all .*public (?:repositories on Hugging Face|Hugging Face repositories)'): return ctx.fail('gguf', q, 'The Malspark author scanned model repositories; neither priority nor coverage of all repository types follows.')
    return ctx.require('framing', r'Root0ne.*published by the Malspark author')


if __name__ == '__main__':
    run_cli(CLAIM, check)
