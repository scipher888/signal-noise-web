import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-blog-commenters', 'artifact': 'episode', 'type': 'attribution', 'story': 'Proof verification', 'quote': "As commenters noted on Aaronson's blog, machine-checked proofs can span hundreds of thousands or millions of lines"}


def check(ctx):
    return ctx.require('framing', r'commenters.{0,60}Aaronson.s blog.{0,120}hundreds of thousands or millions of lines')


if __name__ == '__main__':
    run_cli(CLAIM, check)
