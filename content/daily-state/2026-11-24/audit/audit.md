# Executable audit, Daily State of AI 2026-11-24

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 33 | 2 | 11 | 0 |
| takeaways | 17 | 1 | 0 | 0 |

## Sources
- `primary-openai-cisco-shirudo-ebpf-shields`: [Judge the cyber apocalypse by the data, not the headlines](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/) (sha256 7982037dea61…)
- `x-openai`: [X post by @OpenAI (OpenAI)](https://x.com/OpenAI/status/2125007927098699827) (sha256 ad2ef2abf0f0…)
- `x-ramez`: [X post by @ramez (Ramez Naam)](https://x.com/ramez/status/2125004190032552392) (sha256 27441a435714…)
- `primary-deepmind-gemini4-agents-lean-quantum-cir`: [Finding faster quantum algorithms with agents and formal verification](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/) (sha256 4c737e1c416b…)
- `x-googledeepmind`: [X post by @GoogleDeepMind (Google DeepMind)](https://x.com/GoogleDeepMind/status/2124911073266413634) (sha256 bab36410b7b9…)
- `primary-anthropic-working-with-ai-enterprise-int`: [Working with AI](https://www.anthropic.com/research/working-with-ai) (sha256 5ea4613e2812…)
- `x-emollick`: [X post by @emollick (Ethan Mollick)](https://x.com/emollick/status/2125098309928812898) (sha256 884f518234e8…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt) (sha256 77740be10a3c…)

## episode

### FAIL · oe2-openai-no-independent-audit (objection, Linux Cybersecurity)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (OpenAI): Company-reported launch and controlled test; no independent evaluation yet."

Note: Episode omits caveat that OpenAI/Cisco Shirudo and GPT-6 Cyber results are company-reported with no independent evaluation or audit

```python
def check(ctx):
    s = ctx.find('framing', r'no independent evaluation yet|not independently audited')
    if not ctx.art_has(r'(?:company[- ]reported|self[- ]reported|not independently|no independent|unverified|OpenAI.s own (?:counts|figures|numbers))'):
        return ctx.fail('framing', s, 'Episode omits caveat that OpenAI/Cisco Shirudo and GPT-6 Cyber results are company-reported with no independent evaluation or audit')
    return ctx.ok('framing', s)
```

### FAIL · oe4-anthropic-nonrepresentative-sample (objection, Anthropic Enterprise Study)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (Anthropic): Qualitative interviews with Anthropic's own enterprise customers; company-reported and not a representative sample."

Note: Episode omits caveat that Anthropic study consists of qualitative interviews with its own customers and is not a representative sample

```python
def check(ctx):
    s = ctx.find('framing', r'not a representative sample')
    if not (ctx.art_has(r'own (?:business|enterprise) customers') and ctx.art_has(r'(?:not (?:a )?representative|non-representative|qualitative)')):
        return ctx.fail('framing', s, 'Episode omits caveat that Anthropic study consists of qualitative interviews with its own customers and is not a representative sample')
    return ctx.ok('framing', s)
```

### NEEDS-HUMAN · e01-intro-date (number, Intro)
> Claim: Tuesday, November 24, 2026

Note: Episode date Tuesday, November 24, 2026 is not stated in source texts (primary articles are dated Nov 23, 2026)

```python
def check(ctx):
    return ctx.need(None, None, 'Episode date Tuesday, November 24, 2026 is not stated in source texts (primary articles are dated Nov 23, 2026)')
```

### NEEDS-HUMAN · e14-zero-operational-risk (qualifier, Quantum Circuits)
> Claim: zero operational risk

Note: no source sentence matches /operational risk/. Editorial framing not stated in DeepMind source

```python
def check(ctx):
    return ctx.require('deepmind', r'operational risk', note='Editorial framing not stated in DeepMind source')
```

### NEEDS-HUMAN · e16-run-cost-1-2m (number, Linux Cybersecurity)
> Claim: in a single run costing 1.2 million dollars in API credits

Note: no source sentence matches /1\.2\s*million/. Primary OpenAI research post not in snapshot; cost not in openai2

```python
def check(ctx):
    return ctx.require('openai2', r'1\.2\s*million', r'API credits', note='Primary OpenAI research post not in snapshot; cost not in openai2')
```

### NEEDS-HUMAN · e19-cost-1280-per-exploit (number, Linux Cybersecurity)
> Claim: averaging about 1,280 dollars per root exploit

Note: no source sentence matches /1,?280/. Per-exploit cost figure not in available OpenAI snapshot

```python
def check(ctx):
    return ctx.require('openai2', r'1,?280', note='Per-exploit cost figure not in available OpenAI snapshot')
```

### NEEDS-HUMAN · e20-ten-novel-techniques (number, Linux Cybersecurity)
> Claim: inventing at least ten novel exploitation techniques

Note: no source sentence matches /(?:10|ten)\s+novel\s+exploit/. Novel exploitation techniques count not in available OpenAI snapshot

```python
def check(ctx):
    return ctx.require('openai2', r'(?:10|ten)\s+novel\s+exploit', note='Novel exploitation techniques count not in available OpenAI snapshot')
```

### NEEDS-HUMAN · e21-openai-cisco-shirudo (attribution, Linux Cybersecurity)
> Claim: OpenAI and Cisco open-sourced Shirudo

Note: no source sentence matches /Cisco.*Shirudo/. Primary OpenAI/Cisco Shirudo source missing from snapshot (openai alias holds CSET article)

```python
def check(ctx):
    return ctx.require('openai', r'Cisco.*Shirudo', note='Primary OpenAI/Cisco Shirudo source missing from snapshot (openai alias holds CSET article)')
```

### NEEDS-HUMAN · e22-shirudo-japanese-shield (qualifier, Linux Cybersecurity)
> Claim: Shirudo, Japanese for shield

Note: no source sentence matches /Shirudo.*Japanese.*shield/. Shirudo etymology not in available source snapshots

```python
def check(ctx):
    return ctx.require('openai', r'Shirudo.*Japanese.*shield', note='Shirudo etymology not in available source snapshots')
```

### NEEDS-HUMAN · e23-shirudo-ebpf-runtime (attribution, Linux Cybersecurity)
> Claim: a Linux runtime that lets agents write temporary, cryptographically signed eBPF shields to block exploits on running servers without a restart

Note: no source sentence matches /eBPF shields/. Primary Shirudo source not in snapshot

```python
def check(ctx):
    return ctx.require('openai', r'eBPF shields', r'cryptographically signed', note='Primary Shirudo source not in snapshot')
```

### NEEDS-HUMAN · e24-hardware-verification (qualifier, Linux Cybersecurity)
> Claim: backed by hardware verification

Note: no source sentence matches /hardware verification/. Primary Shirudo source not in snapshot

```python
def check(ctx):
    return ctx.require('openai', r'hardware verification', note='Primary Shirudo source not in snapshot')
```

### NEEDS-HUMAN · e25-operator-approval (qualifier, Linux Cybersecurity)
> Claim: an operator still has to approve each shield and make sure it does not break legitimate traffic

Note: no source sentence matches /operator.*approve.*shield/. Primary Shirudo source not in snapshot

```python
def check(ctx):
    return ctx.require('openai', r'operator.*approve.*shield', note='Primary Shirudo source not in snapshot')
```

### NEEDS-HUMAN · e34-attackers-limited-by-incentives (opinion, CSET Cyber Report)
> Claim: That could just be reporting lag, or it could mean something deeper: attackers are not limited by technical capability

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "If the limiting factor constraining cyber attacks was the threat of jail and missiles, then the real-world impacts of cyber attacks may not change nearly as dramatically as the underlying technologies do."

Note: Opinion/hypothesis in CSET report; check whether episode overstates conditional framing as settled fact

```python
def check(ctx):
    s = ctx.find('openai', r'If the limiting factor constraining cyber attacks was the threat of jail and missiles')
    return ctx.need('openai', s, 'Opinion/hypothesis in CSET report; check whether episode overstates conditional framing as settled fact')
```

### PASS · e02-deepmind-quantum-attribution (attribution, Quantum Circuits)
> Claim: Google DeepMind and Google Quantum AI announced that teams of Gemini 4 agents discovered significantly cheaper quantum circuits for future hardware

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "This research was a collaboration between Google DeepMind and Google Quantum AI. … In a new paper, we used teams of Gemini 4 agents to improve well-known quantum algorithms, creating highly efficient quantum circuits."

```python
def check(ctx):
    return ctx.require('deepmind', r'collaboration between Google DeepMind and Google Quantum AI', r'teams of Gemini 4 agents.*quantum circuits')
```

### PASS · e03-significantly-cheaper-circuits (comparison, Quantum Circuits)
> Claim: significantly cheaper quantum circuits

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits. … Running these algorithms in scientific simulations would still demand more computational resources than the first error-corrected quantum computers are likely to provide, but these improvements are significant."

```python
def check(ctx):
    return ctx.require('deepmind', r'8× cheaper|cut the required computing cost.*11\.8×', r'improvements are significant')
```

### PASS · e04-four-hour-virtual-conferences (number, Quantum Circuits)
> Claim: Every four hours, separate agent teams met in virtual conferences to debate and trade ideas

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Improving quantum algorithms using agentic teams For each problem, we tasked separate, independent agent teams with finding algorithmic improvements. … Every four hours, agents from each team met at a virtual conference to trade, debate and compare ideas."

```python
def check(ctx):
    return ctx.require('deepmind', r'separate, independent agent teams', r'Every four hours, agents from each team met at a virtual conference to trade, debate')
```

### PASS · e05-lab-reports-cutting-costs (attribution, Quantum Circuits)
> Claim: The lab reports cutting computing costs

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits."

```python
def check(ctx):
    return ctx.require('deepmind', r'cut the required computing cost')
```

### PASS · e06-fusion-nearly-12x (number, Quantum Circuits)
> Claim: nearly 12 times for an inertial confinement fusion simulation

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "- We found a quantum circuit that helps calculate an important property of inertial confinement fusion, a fusion reaction method that uses lasers to compress hydrogen fuel until ignition. … Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits."

```python
def check(ctx):
    return ctx.require('deepmind', r'inertial confinement fusion', r'computing cost.*11\.8×')
```

### PASS · e07-light-sensitive-molecule-8x (number, Quantum Circuits)
> Claim: 8 times for simulating a light-sensitive molecule

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "For a common light-sensitive molecule, the agent teams made quantum simulation 8× cheaper, simplifying how the algorithm tracks particle positions and electric forces."

```python
def check(ctx):
    return ctx.require('deepmind', r'light-sensitive molecule.*8× cheaper')
```

### PASS · e08-cytochrome-p450-2-5x (number, Quantum Circuits)
> Claim: two and a half times for Cytochrome P450

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "For Cytochrome P450, an enzyme that breaks down most human medicines and is important for drug design, they found a 2.5× improvement and lowered memory from 481 to 333 qubits, by replacing bulky memory lookups."

```python
def check(ctx):
    return ctx.require('deepmind', r'Cytochrome P450.*2\.5× improvement')
```

### PASS · e09-arcsin-290x (number, Quantum Circuits)
> Claim: 290 times for arcsin

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "We found a 2.57x speedup for a specific implementation of Grover's algorithm, a foundational quantum operation that searches through an unsorted list, and a 290x speedup for arcsin, a common routine that is used by many other quantum algorithms to load numbers into quantum states."

```python
def check(ctx):
    return ctx.require('deepmind', r'290x speedup for arcsin')
```

### PASS · e10-hundreds-to-thousands-qubits (number, Quantum Circuits)
> Claim: hundreds to thousands of error-corrected qubits

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits. … For Cytochrome P450, an enzyme that breaks down most human medicines and is important for drug design, they found a 2.5× improvement and lowered memory from 481 to 333 qubits, by replacing bulky memory lookups."

```python
def check(ctx):
    return ctx.require('deepmind', r'4,338 error-corrected qubits', r'481 to 333 qubits')
```

### PASS · e11-no-quantum-computer-today (qualifier, Quantum Circuits)
> Claim: no quantum computer on earth can run them today

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Because we cannot test resource-intensive quantum circuits on classical computers or today's small quantum processors, we have to prove that they work mathematically. … Running these algorithms in scientific simulations would still demand more computational resources than the first error-corrected quantum computers are likely to provide, but these improvements are significant."

```python
def check(ctx):
    return ctx.require('deepmind', r"cannot test resource-intensive quantum circuits on.*today's small quantum processors", r'more computational resources than the first error-corrected quantum computers')
```

### PASS · e12-proved-using-lean (attribution, Quantum Circuits)
> Claim: every single circuit was mathematically proved using Lean

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams proved each result using Lean, a formal theorem prover."

```python
def check(ctx):
    return ctx.require('deepmind', r'proved each result using Lean')
```

### PASS · e13-open-sourced-lean-library (attribution, Quantum Circuits)
> Claim: DeepMind open-sourced the Lean library and proofs for outside checking

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "To help the community build on this work, we are open-sourcing our Lean library, problem specifications, and verified solutions on GitHub."

```python
def check(ctx):
    return ctx.require('deepmind', r'open-sourcing our Lean library, problem specifications, and verified solutions')
```

### PASS · e15-openai-highlighted-research (attribution, Linux Cybersecurity)
> Claim: OpenAI highlighted research

Source ([x-openai](https://x.com/OpenAI/status/2125007927098699827)): "@OpenAI: In one run, GPT-6 Cyber helped us validate 948 Linux kernel bugs that could grant local root access and generate patches for review. … Read the research: https://t.co/wFfTbqet4H"

```python
def check(ctx):
    return ctx.require('openai2', r'@OpenAI:', r'Read the research')
```

### PASS · e17-gpt6-cyber-patches (attribution, Linux Cybersecurity)
> Claim: its GPT-6 Cyber pipeline validated and generated patches

Source ([x-openai](https://x.com/OpenAI/status/2125007927098699827)): "@OpenAI: In one run, GPT-6 Cyber helped us validate 948 Linux kernel bugs that could grant local root access and generate patches for review."

```python
def check(ctx):
    return ctx.require('openai2', r'GPT-6 Cyber helped us validate.*generate patches')
```

### PASS · e18-948-linux-kernel-bugs (number, Linux Cybersecurity)
> Claim: 948 Linux kernel local privilege escalation bugs

Source ([x-openai](https://x.com/OpenAI/status/2125007927098699827)): "@OpenAI: In one run, GPT-6 Cyber helped us validate 948 Linux kernel bugs that could grant local root access and generate patches for review."

```python
def check(ctx):
    return ctx.require('openai2', r'948 Linux kernel bugs that could grant local root access')
```

### PASS · e26-cset-report-attribution (attribution, CSET Cyber Report)
> Claim: an independent report from Georgetown's Center for Security and Emerging Technology

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "Judge the Cyber Apocalypse by the Data, Not the Headlines | Center for Security and Emerging Technology … Page image: https://cset.georgetown.edu/wp-content/uploads/Blog-Dark-Blue.png"

```python
def check(ctx):
    return ctx.require('openai', r'Center for Security and Emerging Technology', r'georgetown\.edu')
```

### PASS · e27-author-andrew-lohn (attribution, CSET Cyber Report)
> Claim: Author Andrew Lohn points out

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "Andrew Lohn"

```python
def check(ctx):
    return ctx.require('openai', r'Andrew Lohn')
```

### PASS · e28-cves-tripling-jan-sep (comparison, CSET Cyber Report)
> Claim: monthly vulnerability counts tripling between January and September

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "Monthly counts have already tripled from January to September."

```python
def check(ctx):
    return ctx.require('openai', r'Monthly counts have already tripled from January to September')
```

### PASS · e29-patching-slowing-down (comparison, CSET Cyber Report)
> Claim: patching slowing down

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "On the defensive side, patching is getting slower, and it is taking longer to identify and to contain breaches."

```python
def check(ctx):
    return ctx.require('openai', r'patching is getting slower')
```

### PASS · e30-real-world-damage-not-spiking (comparison, CSET Cyber Report)
> Claim: real-world cyber damage is not spiking

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "This is in line with daily news stories on the "vulnpocalypse" and "Black October." Surprisingly though, data on real-world impacts of cyber attacks tells a less dire story."

```python
def check(ctx):
    return ctx.require('openai', r'data on real-world impacts of cyber attacks tells a less dire story')
```

### PASS · e31-ransomware-payouts-falling (comparison, CSET Cyber Report)
> Claim: Ransomware payouts are falling

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "The number of ransomware attacks is up somewhat, but the payouts caused by those attacks are down."

```python
def check(ctx):
    return ctx.require('openai', r'ransomware attacks.*payouts.*(?:down|shrinking)')
```

### PASS · e32-healthcare-breach-impacts-down (comparison, CSET Cyber Report)
> Claim: healthcare breach impacts are down

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "The number of health care breaches is stable, and the number of people affected by those breaches was down in 2025 and again in 2026."

```python
def check(ctx):
    return ctx.require('openai', r'health care breaches.*number of people affected.*down in 2025 and again in 2026')
```

### PASS · e33-zero-days-six-year-low (number, CSET Cyber Report)
> Claim: zero-days exploited in the wild are on pace for a six-year low

Source ([primary-openai-cisco-shirudo-ebpf-shields](https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/)): "Surprisingly though, the number of vulnerabilities that attackers find and use before defenders find them (known as zero-day vulnerabilities) is on a downward trend, with 2026 on pace to be the lowest in six years."

```python
def check(ctx):
    return ctx.require('openai', r'zero-day vulnerabilities.*2026 on pace to be the lowest in six years')
```

### PASS · e35-anthropic-published-study (attribution, Anthropic Enterprise Study)
> Claim: Anthropic published a study

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Working with AI \ Anthropic … To understand businesses' experiences better, we conducted 66 interviews with 58 of Anthropic's enterprise customers."

```python
def check(ctx):
    return ctx.require('anthropic', r'Working with AI.*Anthropic', r'we conducted 66 interviews')
```

### PASS · e36-66-interviews-58-customers (number, Anthropic Enterprise Study)
> Claim: 66 interviews across 58 of its own business customers

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "To understand businesses' experiences better, we conducted 66 interviews with 58 of Anthropic's enterprise customers."

```python
def check(ctx):
    return ctx.require('anthropic', r'66 interviews with 58 of Anthropic.s enterprise customers')
```

### PASS · e37-coding-agents-beyond-engineering (comparison, Anthropic Enterprise Study)
> Claim: Coding agents are spreading far beyond engineering

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "In particular, they are increasingly using coding agents to bring software capabilities to nontechnical roles."

```python
def check(ctx):
    return ctx.require('anthropic', r'using coding agents to bring software capabilities to nontechnical roles')
```

### PASS · e38-domestic-layoffs-rare (qualifier, Anthropic Enterprise Study)
> Claim: domestic layoffs are still rare

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Across our interviews, we saw very few examples of domestic layoffs that were driven by AI automation."

```python
def check(ctx):
    return ctx.require('anthropic', r'very few examples of domestic layoffs')
```

### PASS · e39-two-thirds-hiring-less (number, Anthropic Enterprise Study)
> Claim: two-thirds of these companies say they are hiring less because of AI

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "People at two-thirds of the companies we spoke to reported reduced hiring due to AI: as one person put it, "We may not be firing, but we're not hiring." A third of these hiring declines were due to companies actively shrinking functions through attrition without backfilling the roles."

```python
def check(ctx):
    return ctx.require('anthropic', r'two-thirds of the companies we spoke to reported reduced hiring due to AI')
```

### PASS · e40-cutting-offshore-contractors (qualifier, Anthropic Enterprise Study)
> Claim: many are cutting offshore contractors

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Many also reported reducing their use of contractors, particularly offshore ones."

```python
def check(ctx):
    return ctx.require('anthropic', r'Many also reported reducing their use of contractors, particularly offshore ones')
```

### PASS · e41-quote-claude-grenades (quote, Anthropic Enterprise Study)
> Claim: what one interviewee called Claude grenades

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Power users lob "Claude grenades" and shoot "Claude cannons" at the rest of the organization, while AI skeptics respond, "Guys, I'm not reading your AI email." In one case, an AI agent put together a set of profit and loss projections that a Chief Investment Officer realized were based on outdated assumptions."

```python
def check(ctx):
    return ctx.require('anthropic', r'Claude grenades')
```

### PASS · e42-quote-building-own-coffin (quote, Anthropic Enterprise Study)
> Claim: as one put it, like they are building their own coffin

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "One software engineer, who we'll call Ellen, described her first encounter with automated coding: "I don't think that my job is secure… software engineers are going to be obsolete." Another employee put it even more bluntly: "If I'm open to this, I'm essentially building my own coffin.""

```python
def check(ctx):
    return ctx.require('anthropic', r'building my own coffin')
```

### PASS · oe1-deepmind-future-hardware-caveat (objection, Quantum Circuits)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (Google DeepMind): Company-reported results; each circuit is machine-checked in Lean and the library is open-sourced, but resource savings are estimates for hardware that does not exist yet."

Note: Episode notes that quantum circuit savings are for future hardware / no quantum computer can run them today

```python
def check(ctx):
    s = ctx.find('framing', r'resource savings are estimates for hardware that does not exist yet')
    if not ctx.art_has(r'(?:hardware that does not exist|future hardware|no quantum computer.*today|cannot run.*today)'):
        return ctx.fail('framing', s, 'Episode omits caveat that quantum circuit savings are estimates for hardware that does not exist yet')
    return ctx.ok('framing', s, 'Episode notes that quantum circuit savings are for future hardware / no quantum computer can run them today')
```

### PASS · oe3-cset-data-lag-caveat (objection, CSET Cyber Report)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (Georgetown CSET): Third-party analysis of attack-impact data; interpretive, and its authors note data may lag."

Note: Episode notes that CSET attack-impact data may lag

```python
def check(ctx):
    s = ctx.find('framing', r'interpretive, and its authors note data may lag')
    if not ctx.art_has(r'(?:lag|lagging|too early|hypothesis|interpretive|may not hold)'):
        return ctx.fail('framing', s, 'Episode omits caveat that CSET attack-impact analysis is interpretive and data may lag')
    return ctx.ok('framing', s, 'Episode notes that CSET attack-impact data may lag')
```

## takeaways

### FAIL · ot2-anthropic-nonrepresentative-sample (objection, Anthropic customer study)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (Anthropic): Qualitative interviews with Anthropic's own enterprise customers; company-reported and not a representative sample."

Note: Takeaways omit caveat that Anthropic study consists of qualitative interviews with its own customers and is not a representative sample

```python
def check(ctx):
    s = ctx.find('framing', r'not a representative sample')
    if not (ctx.art_has(r'own (?:business|enterprise) customers') and ctx.art_has(r'(?:not (?:a )?representative|non-representative|qualitative)')):
        return ctx.fail('framing', s, 'Takeaways omit caveat that Anthropic study consists of qualitative interviews with its own customers and is not a representative sample')
    return ctx.ok('framing', s)
```

### PASS · ot1-deepmind-future-hardware-caveat (objection, Google DeepMind quantum circuits)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-24/audit/sources/2026-11-24/scan-framing.txt)): "framing (Google DeepMind): Company-reported results; each circuit is machine-checked in Lean and the library is open-sourced, but resource savings are estimates for hardware that does not exist yet."

Note: Takeaways note that no quantum computer today can run these circuits

```python
def check(ctx):
    s = ctx.find('framing', r'resource savings are estimates for hardware that does not exist yet')
    if not ctx.art_has(r'(?:hardware that does not exist|future hardware|no quantum computer.*today|cannot run.*today)'):
        return ctx.fail('framing', s, 'Takeaways omit caveat that quantum circuit savings are estimates for hardware that does not exist yet')
    return ctx.ok('framing', s, 'Takeaways note that no quantum computer today can run these circuits')
```

### PASS · t01-deepmind-reports-cheaper-circuits (attribution, Google DeepMind quantum circuits)
> Claim: Google DeepMind reports Gemini 4 agent teams found cheaper quantum circuits

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Finding faster quantum algorithms with agents and formal verification - Google DeepMind … In a new paper, we used teams of Gemini 4 agents to improve well-known quantum algorithms, creating highly efficient quantum circuits."

```python
def check(ctx):
    return ctx.require('deepmind', r'Google DeepMind', r'teams of Gemini 4 agents.*quantum circuits')
```

### PASS · t02-cheaper-quantum-circuits (comparison, Google DeepMind quantum circuits)
> Claim: cheaper quantum circuits

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits."

```python
def check(ctx):
    return ctx.require('deepmind', r'8× cheaper|cut the required computing cost')
```

### PASS · t03-fusion-nearly-12x (number, Google DeepMind quantum circuits)
> Claim: costs cut by nearly 12 times for an inertial confinement fusion simulation

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "- We found a quantum circuit that helps calculate an important property of inertial confinement fusion, a fusion reaction method that uses lasers to compress hydrogen fuel until ignition. … Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits."

```python
def check(ctx):
    return ctx.require('deepmind', r'inertial confinement fusion', r'computing cost.*11\.8×')
```

### PASS · t04-qualifier-nearly-12x (qualifier, Google DeepMind quantum circuits)
> Claim: nearly 12 times

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits."

```python
def check(ctx):
    return ctx.require('deepmind', r'11\.8×')
```

### PASS · t05-proved-in-lean (qualifier, Google DeepMind quantum circuits)
> Claim: every circuit was mathematically proved in Lean

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams proved each result using Lean, a formal theorem prover."

```python
def check(ctx):
    return ctx.require('deepmind', r'proved each result using Lean')
```

### PASS · t06-no-quantum-computer-today-qubits (qualifier, Google DeepMind quantum circuits)
> Claim: no quantum computer today can run the hundreds to thousands of error-corrected qubits they require

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Because we cannot test resource-intensive quantum circuits on classical computers or today's small quantum processors, we have to prove that they work mathematically. … Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits. … For Cytochrome P450, an enzyme that breaks down most human medicines and is important for drug design, they found a 2.5× improvement and lowered memory from 481 to 333 qubits, by replacing bulky memory lookups."

```python
def check(ctx):
    return ctx.require('deepmind', r"today's small quantum processors", r'4,338 error-corrected qubits', r'481 to 333 qubits')
```

### PASS · t07-hundreds-to-thousands-qubits (number, Google DeepMind quantum circuits)
> Claim: hundreds to thousands of error-corrected qubits

Source ([primary-deepmind-gemini4-agents-lean-quantum-cir](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)): "Our agent teams cut the required computing cost (a metric that combines required qubits and operations) by 11.8×, and lowered required memory from 5,650 to 4,338 error-corrected qubits. … For Cytochrome P450, an enzyme that breaks down most human medicines and is important for drug design, they found a 2.5× improvement and lowered memory from 481 to 333 qubits, by replacing bulky memory lookups."

```python
def check(ctx):
    return ctx.require('deepmind', r'4,338 error-corrected qubits', r'481 to 333 qubits')
```

### PASS · t08-anthropic-study-attribution (attribution, Anthropic customer study)
> Claim: Anthropic's study

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Working with AI \ Anthropic"

```python
def check(ctx):
    return ctx.require('anthropic', r'Working with AI.*Anthropic')
```

### PASS · t09-66-interviews (number, Anthropic customer study)
> Claim: 66 interviews

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "To understand businesses' experiences better, we conducted 66 interviews with 58 of Anthropic's enterprise customers."

```python
def check(ctx):
    return ctx.require('anthropic', r'66 interviews')
```

### PASS · t10-58-own-business-customers (number, Anthropic customer study)
> Claim: 58 of its own business customers

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "To understand businesses' experiences better, we conducted 66 interviews with 58 of Anthropic's enterprise customers."

```python
def check(ctx):
    return ctx.require('anthropic', r'58 of Anthropic.s enterprise customers')
```

### PASS · t11-own-business-customers-qualifier (qualifier, Anthropic customer study)
> Claim: its own business customers

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "To understand businesses' experiences better, we conducted 66 interviews with 58 of Anthropic's enterprise customers."

```python
def check(ctx):
    return ctx.require('anthropic', r'58 of Anthropic.s enterprise customers|They.re all Anthropic customers')
```

### PASS · t12-two-thirds-hiring-less (number, Anthropic customer study)
> Claim: two-thirds said they are hiring less because of AI

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "People at two-thirds of the companies we spoke to reported reduced hiring due to AI: as one person put it, "We may not be firing, but we're not hiring." A third of these hiring declines were due to companies actively shrinking functions through attrition without backfilling the roles."

```python
def check(ctx):
    return ctx.require('anthropic', r'two-thirds of the companies we spoke to reported reduced hiring due to AI')
```

### PASS · t13-hiring-less-because-of-ai (comparison, Anthropic customer study)
> Claim: hiring less because of AI

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Although some companies reported hiring more due to AI, most companies reported hiring less due to AI."

```python
def check(ctx):
    return ctx.require('anthropic', r'hiring less due to AI|reduced hiring due to AI')
```

### PASS · t14-reorganizing-roles-workflows (comparison, Anthropic customer study)
> Claim: the companies capturing real value were those reorganizing roles and workflows rather than simply handing out tools

Source ([primary-anthropic-working-with-ai-enterprise-int](https://www.anthropic.com/research/working-with-ai)): "Interviewees described the highest-value uses as involving meaningful reorganization. … Some companies are experimenting with complementary organizational changes in response to AI rather than just automating existing workflows or handing out AI tools."

```python
def check(ctx):
    return ctx.require('anthropic', r'highest-value uses as involving meaningful reorganization', r'rather than just automating existing workflows or handing out AI tools')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://www.anthropic.com/research/working-with-ai, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
