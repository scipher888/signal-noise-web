import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-wallet-claim', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Mir2k', 'quote': 'carves the trojan out of the model file on disk and launches a Tor-connected password stealer, wallet drainer, and Monero miner'}


def check(ctx):
    q = ctx.find('gguf', r'targets the Phantom and MetaMask wallet extensions')
    if q and ctx.absent('gguf', r'drains? (?:the |crypto)?wallets?|wallet drain(?:er|ing)'): return ctx.fail('gguf', q, 'Targeting wallet extensions does not establish draining wallets.')
    return ctx.require('gguf', r'printed line reads the hidden bytes back out.*starts them', r'sends saved passwords', r'mines Monero.*over Tor', r'wallet drain(?:er|ing)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
