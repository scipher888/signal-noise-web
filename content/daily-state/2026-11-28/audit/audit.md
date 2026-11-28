# Executable audit, Daily State of AI 2026-11-28

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 59 | 15 | 16 | 0 |
| takeaways | 24 | 7 | 0 | 0 |

## Sources
- `primary-gguf-supply-chain-malware`: [GGUF LLM Models with Hidden Malware on Hugging Face Reached 2400+ Victims](https://malspark.com/blog/malicious-gguf-models-hugging-face/) (sha256 2c0842926369…)
- `x-itsmeajaykv`: [X post by @ItsmeAjayKV (AJ)](https://x.com/ItsmeAjayKV/status/2126546800291266717) (sha256 9b222daaf3ca…)
- `primary-gpt-6-2-astra-sol-wisdom`: [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/) (sha256 2e00a2b0c0c8…)
- `x-thezvi`: [X post by @TheZvi (Zvi Mowshowitz)](https://x.com/TheZvi/status/2126309705131651174) (sha256 213bfbc68494…)
- `primary-unsloth-local-3d-engine-mcp`: [Blender, Unreal Engine, Unity, Godot, Roblox with Local Models](https://unsloth.ai/docs/basics/mcp/mcp-engines) (sha256 5387f0e5cd91…)
- `x-unslothai`: [X post by @UnslothAI (Unsloth AI)](https://x.com/UnslothAI/status/2126322382239649959) (sha256 698119d6740b…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt) (sha256 996c3cef9b7e…)

## episode

### FAIL · e05-bridges (qualifier, Unsloth demos)
> Claim: new built-in MCP bridges in Unsloth Desktop and Studio for Godot, Figma, and Roblox Studio

Source ([primary-unsloth-local-3d-engine-mcp](https://unsloth.ai/docs/basics/mcp/mcp-engines)): "Open the AssetLib tab (Asset Store in Godot 4.7), search Godot MCP Native, then download and install it."

Note: Built-in connection choices are not three bridges supplied by Unsloth; Godot needs a separate plugin.

```python
def check(ctx):
    return ctx.support_or_contradict('unsloth', r'built.in MCP bridges in Unsloth Desktop and Studio for Godot, Figma and Roblox Studio', r'search Godot MCP Native, then download and install it', 'Built-in connection choices are not three bridges supplied by Unsloth; Godot needs a separate plugin.')
```

### FAIL · e11-scan-author (attribution, GGUF scan)
> Claim: Security researcher Root0ne at Malspark published the first scan of all 3.27 million public repositories on Hugging Face

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories found five malicious models downloaded 2428 times."

Note: The Malspark author scanned model repositories; neither priority nor coverage of all repository types follows.

```python
def check(ctx):
    q = ctx.find('gguf', r'all 3273389 public Hugging Face model repositories')
    if q and ctx.absent('gguf', r'first scan of all .*public (?:repositories on Hugging Face|Hugging Face repositories)'): return ctx.fail('gguf', q, 'The Malspark author scanned model repositories; neither priority nor coverage of all repository types follows.')
    return ctx.require('framing', r'Root0ne.*published by the Malspark author')
```

### FAIL · e12-scan-priority (comparison, GGUF scan)
> Claim: the first scan of all 3.27 million public repositories on Hugging Face

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "What this post adds is the method seen in real attacks on Hugging Face, and its combination by Mir2k with an executable appended after the last tensor and a template switched on days later, for which no earlier public report was found."

Note: The novelty statement concerns a technique observed in the wild, not priority of a platform-wide census.

```python
def check(ctx):
    return ctx.support_or_contradict('gguf', r'first scan of all (?:3\.27 million|3273389) public Hugging Face repositories', r'What this post adds is the method seen in real attacks.*no earlier public report', 'The novelty statement concerns a technique observed in the wild, not priority of a platform-wide census.')
```

### FAIL · e13-scan-universe (number, GGUF scan)
> Claim: all 3.27 million public repositories on Hugging Face

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories found five malicious models downloaded 2428 times."

Note: Correct rounded count, wrong universe: model repositories only.

```python
def check(ctx):
    return ctx.support_or_contradict('gguf', r'all 3273389 public Hugging Face repositories', r'all 3273389 public Hugging Face model repositories', 'Correct rounded count, wrong universe: model repositories only.')
```

### FAIL · e31-wallet-claim (qualifier, Mir2k)
> Claim: carves the trojan out of the model file on disk and launches a Tor-connected password stealer, wallet drainer, and Monero miner

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "It also targets the Phantom and MetaMask wallet extensions and supports keylogging, clipboard reading, screenshots, screen streaming and webcam capture."

Note: Targeting wallet extensions does not establish draining wallets.

```python
def check(ctx):
    q = ctx.find('gguf', r'targets the Phantom and MetaMask wallet extensions')
    if q and ctx.absent('gguf', r'drains? (?:the |crypto)?wallets?|wallet drain(?:er|ing)'): return ctx.fail('gguf', q, 'Targeting wallet extensions does not establish draining wallets.')
    return ctx.require('gguf', r'printed line reads the hidden bytes back out.*starts them', r'sends saved passwords', r'mines Monero.*over Tor', r'wallet drain(?:er|ing)')
```

### FAIL · e35-identical-models (number, timdedid)
> Claim: Three byte-identical Qwen 3 1.7B repositories marketed to security users

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "One day before Mir2k, on 21 and 22 November, the account timdedid published three byte-identical copies of a Qwen3 1.7B model aimed at security users, together with an Ollama mirror named timdedid/qwen3-1.7b-cyber."

Note: Byte identity is reported for the model copies, not the entire repositories.

```python
def check(ctx):
    q = ctx.find('gguf', r'timdedid published three byte-identical copies of a Qwen3 1\.7B model aimed at security users')
    if q and ctx.absent('gguf', r'three byte-identical repositor'): return ctx.fail('gguf', q, 'Byte identity is reported for the model copies, not the entire repositories.')
    return ctx.require('gguf', r'three byte-identical repositor.*Qwen3 1\.7B.*security users')
```

### FAIL · e43-detection-limits (qualifier, GGUF defenses)
> Claim: weight hashes and ordinary antivirus tools miss poisoned templates and trailing bytes

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Antivirus engines and checks that only look at the last few kilobytes of a file do not see the compressed payload."

Note: A miss on the tested payload does not establish a categorical antivirus blind spot for both techniques.

```python
def check(ctx):
    q = ctx.find('gguf', r'Antivirus engines .* do not see the compressed payload')
    if q and ctx.absent('gguf', r'antivirus.*(?:miss|cannot detect).*poisoned templates and trailing bytes'): return ctx.fail('gguf', q, 'A miss on the tested payload does not establish a categorical antivirus blind spot for both techniques.')
    return ctx.require('gguf', r'weight hashes.*templates.*trailing', r'antivirus.*(?:miss|cannot detect).*poisoned templates and trailing bytes')
```

### FAIL · e62-frontier-headcount (number, Astra feedback)
> Claim: Every's thirty-person frontier team

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "We have a 30-person team at Every, including our Frontier team, which gets access to these models before they come out, and we put them through their paces on our real work tasks, from coding to writing to design to knowledge work."

Note: Thirty counts all of Every, not its Frontier team.

```python
def check(ctx):
    return ctx.support_or_contradict('thezvi', r'30-person Frontier team at Every', r'30-person team at Every, including our Frontier team', 'Thirty counts all of Every, not its Frontier team.')
```

### FAIL · e63-every-population (attribution, Astra feedback)
> Claim: Every's thirty-person frontier team said no one on staff loved Astra or switched back to it

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "We have a 30-person team at Every, including our Frontier team, which gets access to these models before they come out, and we put them through their paces on our real work tasks, from coding to writing to design to knowledge work."

Note: The subgroup is not 30 people. Switching was also qualified: No one on our team who tried it switched back to it.

```python
def check(ctx):
    q = ctx.find('thezvi', r'30-person team at Every, including our Frontier team')
    if q: return ctx.fail('thezvi', q, 'The subgroup is not 30 people. Switching was also qualified: ' + str(ctx.find('thezvi', r'No one on our team who tried it switched back to it')))
    return ctx.require('thezvi', r'30-person Frontier team', r'No one on our team loved Astra', r'No one on (?:our )?staff switched back')
```

### FAIL · e64-writing-builds (attribution, Astra feedback)
> Claim: flagging stiff writing and end-to-end builds that stop prematurely

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Astra 6.2 is a real step back for writing."

Note: Every criticizes writing generally; inflexibility is attributed to design defaults, not prose. It had strong design defaults but couldn't vary them or be creative, and for coding we found it stopped too soon on end-to-end builds.

```python
def check(ctx):
    q = ctx.find('thezvi', r'Astra 6\.2 is a real step back for writing')
    if q and ctx.absent('thezvi', r'(?:stiff|rigid|stilted) (?:writing|prose)'): return ctx.fail('thezvi', q, 'Every criticizes writing generally; inflexibility is attributed to design defaults, not prose. ' + str(ctx.find('thezvi', r'stopped too soon on end-to-end builds')))
    return ctx.require('thezvi', r'Every:.*(?:stiff|rigid|stilted).*writing', r'stopped too soon on end-to-end builds')
```

### FAIL · e70-judge-preference (attribution, Astra feedback)
> Claim: even persuades other AI models acting as judges to prefer Astra's weaker drafts

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "They all voted for Astra's lyrics, which were IMO substantially worse."

Note: A preference vote and one user’s assessment of quality do not establish persuasion or objectively weaker drafts.

```python
def check(ctx):
    q = ctx.find('thezvi', r'all voted for Astra.s lyrics, which were IMO substantially worse')
    if q: return ctx.fail('thezvi', q, 'A preference vote and one user’s assessment of quality do not establish persuasion or objectively weaker drafts.')
    return ctx.require('thezvi', r'persuaded.*judges.*weaker drafts')
```

### FAIL · e74-many-changing (qualifier, Model routing)
> Claim: many builders are already changing who holds the steering wheel

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Scott Novak: Use it as a sub-agent of another frontier AI you like using."

Note: Selected routing advice does not measure prevalence or change in practice.

```python
def check(ctx):
    q = ctx.find('thezvi', r'Use it as a sub-agent of another frontier AI')
    if q and ctx.absent('thezvi', r'many (?:builders|practitioners|users) (?:have switched|are switching|now route)'): return ctx.fail('thezvi', q, 'Selected routing advice does not measure prevalence or change in practice.')
    return ctx.require('thezvi', r'many (?:builders|practitioners|users) (?:have switched|are switching|now route)')
```

### FAIL · oe2-no-replication (objection, GGUF scan)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Malspark): Security researcher's primary technical report with YARA rules, IOCs, and scan methodology; single-team scan, not independently replicated."

Note: Disclose the single-team evidence base.

```python
def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)(?:scan|Malspark|findings).{0,160}(?:not (?:been )?independently (?:replicated|confirmed)|no independent replication)|single[- ]team scan'): return ctx.fail('framing', q, 'Disclose the single-team evidence base.')
    return ctx.ok('framing', q)
```

### FAIL · oe6-no-audit (objection, Astra benchmarks)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (OpenAI): Company-reported launch benchmarks, pricing, and self-reported alignment/safety evaluations; not independently audited."

Note: The company results lack independent audit; ARC verification is a separate claim.

```python
def check(ctx):
    q = ctx.find('framing', r'not independently audited')
    if not ctx.art_has(r'(?is)(?:OpenAI|company|launch benchmarks|safety evaluations).{0,180}(?:not (?:been )?independently audited|no independent audit|without an independent audit)'): return ctx.fail('framing', q, 'The company results lack independent audit; ARC verification is a separate claim.')
    return ctx.ok('framing', q)
```

### FAIL · oe7-every-summary (objection, Astra feedback)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Every): Independent publication's live-testing summary page; full Vibe Check text sits behind an external link, so only the summary statement is captured."

Note: Only Every’s live-testing summary was captured, not the full Vibe Check.

```python
def check(ctx):
    q = ctx.find('framing', r'only the summary statement is captured')
    if not ctx.art_has(r'(?is)Every.{0,120}(?:summary only|only.{0,30}summary|summary.{0,70}(?:not the full|full.{0,20}(?:elsewhere|external|linked)))'): return ctx.fail('framing', q, 'Only Every’s live-testing summary was captured, not the full Vibe Check.')
    return ctx.ok('framing', q)
```

### NEEDS-HUMAN · e01-edition (number, Edition)
> Claim: Daily State of AI for Saturday, November 28th, 2026

Note: no source sentence matches /(?:Saturday,?\s+November 28(?:th)?,? 2026|2026-11-28)/. Edition date, not the date of the malware scan.

```python
def check(ctx):
    return ctx.require('framing', r'(?:Saturday,?\s+November 28(?:th)?,? 2026|2026-11-28)', note='Edition date, not the date of the malware scan.')
```

### NEEDS-HUMAN · e02-two-announcements (number, Creative software)
> Claim: This week, two separate announcements showed AI stepping straight out of the chat box and taking direct control of creative software

Source ([x-unslothai](https://x.com/UnslothAI/status/2126322382239649959)): "@UnslothAI: Your local LLM can now take control of Unreal Engine, Unity &amp; Blender autonomously via Unsloth!"

Note: Check both publication dates and distinguish direct control from generated code. OpenAI example: Astra created the 3D model and wrote a Python solver to simulate complex dynamics between the tires and suspension, then animated the results in Blender.

```python
def check(ctx):
    a = ctx.find('unslothai', r'local LLM can now take control of Unreal Engine, Unity .*Blender')
    b = ctx.find('gpt', r'animated the results in Blender')
    return ctx.need('unslothai', a, 'Check both publication dates and distinguish direct control from generated code. OpenAI example: ' + str(b))
```

### NEEDS-HUMAN · e03-inkling-demo (attribution, Unsloth demos)
> Claim: On desktop hardware, Unsloth demonstrated a compact open model called Inkling 2 Mini driving Unreal Engine, Unity, and Blender

Note: no source sentence matches /(?:open.weight|open.source).*Inkling 2 Mini|Inkling 2 Mini.*(?:open.weight|open.source)/. GGUF and local execution alone do not establish licensing or the demo machine.

```python
def check(ctx):
    return ctx.require('unslothai', r'Your local LLM can now take control of Unreal Engine, Unity .*Blender', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps', r'(?:open.weight|open.source).*Inkling 2 Mini|Inkling 2 Mini.*(?:open.weight|open.source)', r'(?:demo|controlled).*(?:desktop hardware|desktop PC)', note='GGUF and local execution alone do not establish licensing or the demo machine.')
```

### NEEDS-HUMAN · e08-tangible (opinion, App control risks)
> Claim: Handing models live controls inside real applications makes capability gains immediately tangible

Source ([x-unslothai](https://x.com/UnslothAI/status/2126322382239649959)): "Inkling 2 Mini GGUF and Unsloth successfully controlled those apps to create new assets with no human intervention."

Note: The demo is evidence of app use; tangibility is an editorial judgment.

```python
def check(ctx):
    return ctx.need('unslothai', ctx.find('unslothai', r'successfully controlled those apps'), 'The demo is evidence of app use; tangibility is an editorial judgment.')
```

### NEEDS-HUMAN · e09-main-failure (opinion, App control risks)
> Claim: turns the hidden layer between a human prompt and a model's actions into the main point of failure, both from outside attackers and from the models themselves

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The model answers normally, while the template quietly adds instructions the user never sees: make an agent run a PowerShell command, or open every reply with a command for the user to run."

Note: A demonstrated failure mode does not rank it against other causes.

```python
def check(ctx):
    return ctx.need('gguf', ctx.find('gguf', r'template quietly adds instructions the user never sees'), 'A demonstrated failure mode does not rank it against other causes.')
```

### NEEDS-HUMAN · e38-trigger-quote (quote, timdedid)
> Claim: "What is,"

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "When the user's latest message contains What is, it inserts a [SYSTEM DIRECTIVE] telling an agent to call its powershell tool, download value.ps1 from a WordPress site into C:\Windows\Temp\payload.ps1 and run it in a hidden window."

Note: The words are What is. Resolve whether the comma inside the quotation marks is editorial punctuation or asserted trigger text.

```python
def check(ctx):
    q = ctx.find('gguf', r'contains What is, it inserts')
    return ctx.need('gguf', q, 'The words are What is. Resolve whether the comma inside the quotation marks is editorial punctuation or asserted trigger text.')
```

### NEEDS-HUMAN · e45-scan-latency (qualifier, GGUF defenses)
> Claim: Using HTTP Range requests, it checks Hugging Face headers and file tails in seconds

Note: drafted check rejected by the screen (imports, I/O or syntax); review by hand

```python
def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')
```

### NEEDS-HUMAN · e46-range-download (qualifier, GGUF defenses)
> Claim: without downloading gigabytes of weights

Note: drafted check rejected by the screen (imports, I/O or syntax); review by hand

```python
def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')
```

### NEEDS-HUMAN · e48-trust-analogy (comparison, Astra reliability)
> Claim: even when nobody tampers with your files, OpenAI's GPT-6.2 release shows an eerily similar trust gap inside the model itself

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "However, in two tests, they were more likely to omit mentioning obstacles that blocked their work, such as a missing file or unavailable search tool."

Note: Similarity to external tampering is an analogy, not an evaluation result.

```python
def check(ctx):
    return ctx.need('gpt', ctx.find('gpt', r'more likely to omit mentioning obstacles'), 'Similarity to external tampering is an analogy, not an evaluation result.')
```

### NEEDS-HUMAN · e49-powerhouse (opinion, Astra benchmarks)
> Claim: On paper, Astra is a powerhouse

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "On Agents' Last Exam, which tests multistep professional work, GPT-6.2 Astra sets a new high, scoring 5.2 points higher than GPT-6 Astra at less than a third of the cost, and 5.5 points ahead of Claude Fable 5.2 at just 5% of the cost."

Note: Powerhouse is an assessment, not a benchmark threshold.

```python
def check(ctx):
    return ctx.need('gpt', ctx.find('gpt', r'Astra sets a new high, scoring'), 'Powerhouse is an assessment, not a benchmark threshold.')
```

### NEEDS-HUMAN · e61-feedback-tone (opinion, Astra feedback)
> Claim: Early practitioner feedback, however, has been blunt

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "As a result, feedback on Astra has mostly been negative."

Note: Blunt describes tone; this is a selection of reactions.

```python
def check(ctx):
    return ctx.need('thezvi', ctx.find('thezvi', r'feedback on Astra has mostly been negative'), 'Blunt describes tone; this is a selection of reactions.')
```

### NEEDS-HUMAN · e67-hard-problems (attribution, Astra feedback)
> Claim: Astra solves brutal math, physics, and 3D challenges

Note: no source sentence matches /(?:solv|hard|challenge).*physics|physics.*(?:solv|challenge)/. A broad science endorsement does not identify a solved physics challenge.

```python
def check(ctx):
    return ctx.require('thezvi', r'Very good at hard math/science/3D', r'(?:solv|hard|challenge).*physics|physics.*(?:solv|challenge)', note='A broad science endorsement does not identify a solved physics challenge.')
```

### NEEDS-HUMAN · e76-sol-speed-cost (comparison, Model routing)
> Claim: the faster, cheaper GPT-6.2 Sol

Note: no source sentence matches /Sol.*faster than (?:GPT[-‑]6\.2 )?Astra|Astra.*slower than (?:GPT[-‑]6\.2 )?Sol/. The Browser Use speed comparison is to 6.1 Sol, not Astra.

```python
def check(ctx):
    return ctx.require('gpt', r'Sol comes within 0\.5 points of GPT[-‑]6\.2 Astra at about one-fifth the cost', r'Sol.*faster than (?:GPT[-‑]6\.2 )?Astra|Astra.*slower than (?:GPT[-‑]6\.2 )?Sol', note='The Browser Use speed comparison is to 6.1 Sol, not Astra.')
```

### NEEDS-HUMAN · e79-everyday-routing (attribution, Model routing)
> Claim: leaning on the faster, cheaper GPT-6.2 Sol, which leads Browser Use at 82 percent, for everyday work

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Browser Use finds that GPT-6.2 Sol is the new top model for browser use at 82%, up from 81% for GPT-6.1 Sol at a 35% cheaper price with faster speed."

Note: Everyday preference: He says he would stick with Sol for most purposes.. Check the intended speed/price comparator; Browser Use compares against the previous Sol.

```python
def check(ctx):
    q = ctx.find('thezvi', r'Browser Use finds that GPT-6\.2 Sol.*82%.*up from 81% for GPT-6\.1 Sol.*faster speed')
    p = ctx.find('thezvi', r'he would stick with Sol for most purposes')
    return ctx.need('thezvi', q, 'Everyday preference: ' + str(p) + '. Check the intended speed/price comparator; Browser Use compares against the previous Sol.')
```

### NEEDS-HUMAN · e80-bottleneck (opinion, Model supervision)
> Claim: Across local desktops and frontier APIs alike, raw capability is no longer the bottleneck

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Smart is relative, and for many practical purposes other differences now matter a lot more."

Note: Cross-platform bottleneck judgment, not a measured comparison.

```python
def check(ctx):
    return ctx.need('thezvi', ctx.find('thezvi', r'for many practical purposes other differences now matter a lot more'), 'Cross-platform bottleneck judgment, not a measured comparison.')
```

### NEEDS-HUMAN · e81-supervision (opinion, Model supervision)
> Claim: Inspecting and supervising what steers the model after you hit enter is the job now

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "People who run community models locally should treat any command a model suggests as untrusted."

Note: Editorial recommendation extending beyond the local-model advice.

```python
def check(ctx):
    return ctx.need('gguf', ctx.find('gguf', r'People who run community models locally should treat any command a model suggests as untrusted'), 'Editorial recommendation extending beyond the local-model advice.')
```

### PASS · e04-autonomy (qualifier, Unsloth demos)
> Claim: with no human intervention

Source ([x-unslothai](https://x.com/UnslothAI/status/2126322382239649959)): "Inkling 2 Mini GGUF and Unsloth successfully controlled those apps to create new assets with no human intervention."

Note: Vendor description of the demonstrated run.

```python
def check(ctx):
    return ctx.require('unslothai', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps to create new assets with no human intervention', note='Vendor description of the demonstrated run.')
```

### PASS · e06-cloud-release (attribution, OpenAI demos)
> Claim: in the cloud, OpenAI unveiled GPT-6.2 Astra and GPT-6.2 Sol

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "We're introducing GPT-6.2 Astra, our new frontier model for your hardest projects, and GPT-6.2 Sol, our efficient, versatile model for everyday work. … Developers can also access gpt-6.2-astra and gpt-6.2-sol through the OpenAI API, with Ultrafast available for both models at launch."

```python
def check(ctx):
    return ctx.require('gpt', r'introducing GPT[-‑]6\.2 Astra.*GPT[-‑]6\.2 Sol', r'access gpt-6\.2-astra and gpt-6\.2-sol through the OpenAI API')
```

### PASS · e07-creative-demos (attribution, OpenAI demos)
> Claim: demos of Astra building mechanical assemblies in CAD, racing games in the browser, and animations in Blender

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "GPT-6.2 Astra's more precise computer use lets it work down to individual parts and connections in CAD and simulation tools. … It modeled the individual components, created an animated assembly guide, and produced an illustrated parts catalog. … GPT-6.2 Astra builds a playable futuristic racing game on a track that winds through a city. … GPT-6.2 Astra and Sol can turn a written brief into an interactive browser experience, from a pinball table you can play to a recreation of the Colosseum you can explore from different angles. … Astra created the 3D model and wrote a Python solver to simulate complex dynamics between the tires and suspension, then animated the results in Blender."

```python
def check(ctx):
    return ctx.require('gpt', r'individual parts and connections in CAD', r'modeled the individual components, created an animated assembly guide', r'Astra builds a playable futuristic racing game', r'interactive browser experience', r'Astra created the 3D model.*animated the results in Blender')
```

### PASS · e10-surfaced (qualifier, GGUF scan)
> Claim: what just surfaced in the local model supply chain

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November. … What this post adds is the method seen in real attacks on Hugging Face, and its combination by Mir2k with an executable appended after the last tensor and a template switched on days later, for which no earlier public report was found."

```python
def check(ctx):
    return ctx.require('gguf', r'on 26 November 2026 found 5 malicious GGUF models', r'What this post adds is the method seen in real attacks on Hugging Face')
```

### PASS · e14-gguf-count (number, GGUF scan)
> Claim: statically inspecting more than two hundred and twenty-six thousand GGUF repositories

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The scan covered every public model repository on Hugging Face, including 226310 GGUF repositories holding 2.56 PB of weights, and parsed 572184 chat templates statically, without executing any of them."

```python
def check(ctx):
    return ctx.require('gguf', r'including 226310 GGUF repositories.*parsed 572184 chat templates statically')
```

### PASS · e15-template-count (number, GGUF scan)
> Claim: over five hundred and seventy thousand chat templates

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The scan covered every public model repository on Hugging Face, including 226310 GGUF repositories holding 2.56 PB of weights, and parsed 572184 chat templates statically, without executing any of them."

```python
def check(ctx):
    return ctx.require('gguf', r'parsed 572184 chat templates statically')
```

### PASS · e16-no-execution (qualifier, GGUF scan)
> Claim: without executing a single model

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The scan covered every public model repository on Hugging Face, including 226310 GGUF repositories holding 2.56 PB of weights, and parsed 572184 chat templates statically, without executing any of them. … GGUF headers and file ends were read through HTTP Range requests, so no model was downloaded in full. … The open-source tool gguf-radar detects these templates and hidden bytes without running anything, and rebuilds a clean GGUF file with the model weights unchanged."

```python
def check(ctx):
    return ctx.require('gguf', r'parsed 572184 chat templates statically, without executing any of them', r'no model was downloaded in full', r'detects these templates and hidden bytes without running anything')
```

### PASS · e17-live-campaigns (number, GGUF scan)
> Claim: The scan uncovered five active malicious GGUF repositories across two campaigns

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November. … Five repositories remained, all still online on 27 November. … Scan Results Across 3.27 Million Repositories3.1 Campaign 1: Mir2k, Plant First and Arm Later3.1.1 The ollie Implant3.2 Campaign 2: timdedid, Hijacking Coding Agents4."

```python
def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'Five repositories remained, all still online', r'Campaign 1: Mir2k', r'Campaign 2: timdedid')
```

### PASS · e18-friday-count (number, GGUF scan)
> Claim: had logged 2,428 downloads by Friday

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November."

Note: 27 November 2026 was Friday; counts are downloads, not unique victims.

```python
def check(ctx):
    return ctx.require('gguf', r'on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November', note='27 November 2026 was Friday; counts are downloads, not unique victims.')
```

### PASS · e19-growth (comparison, GGUF scan)
> Claim: surging more than fifty percent in a single day

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The count grew by more than half in one day, almost entirely on the two Mir2k models."

```python
def check(ctx):
    return ctx.require('gguf', r'count grew by more than half in one day')
```

### PASS · e20-larger (comparison, Mir2k)
> Claim: The larger campaign, named Mir2k

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The largest campaign, Mir2k, uploaded two uncensored GGUF models with a Windows remote access trojan named ollie hidden at the end of each file, and on 26 November rewrote both templates so the model asks the user to run the line that unpacks it."

Note: Larger by downloads, not by number of repositories.

```python
def check(ctx):
    return ctx.require('gguf', r'The largest campaign, Mir2k', note='Larger by downloads, not by number of repositories.')
```

### PASS · e21-two-stages (number, Mir2k)
> Claim: used a patient two-stage trap

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The hidden program is uploaded first and the template is changed two to four days later."

```python
def check(ctx):
    return ctx.require('gguf', r'hidden program is uploaded first and the template is changed two to four days later')
```

### PASS · e22-upload-names (attribution, Mir2k)
> Claim: First, the attacker uploaded uncensored GGUF builds of Qwen 3.5 and Inkling 2 Mini

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The largest campaign, Mir2k, uploaded two uncensored GGUF models with a Windows remote access trojan named ollie hidden at the end of each file, and on 26 November rewrote both templates so the model asks the user to run the line that unpacks it. … On 22 November, Huihui-Qwen3.5-9B-abliterated was uploaded with the executable already appended after its last tensor, but with its original, clean template. … On 24 November, Inkling-2-Mini-Uncensored followed with the same executable in compressed form, again with a clean template."

```python
def check(ctx):
    return ctx.require('gguf', r'Mir2k, uploaded two uncensored GGUF models', r'On 22 November, Huihui-Qwen3\.5-9B-abliterated was uploaded', r'On 24 November, Inkling-2-Mini-Uncensored followed')
```

### PASS · e23-name-match (comparison, Mir2k)
> Claim: Inkling 2 Mini, the very model name featured in Unsloth's demos

Source ([x-unslothai](https://x.com/UnslothAI/status/2126322382239649959)): "Inkling 2 Mini GGUF and Unsloth successfully controlled those apps to create new assets with no human intervention."

Note: Name match only, not identity of files: On 24 November, Inkling-2-Mini-Uncensored followed with the same executable in compressed form, again with a clean template.

```python
def check(ctx):
    q = ctx.find('gguf', r'Inkling-2-Mini-Uncensored followed')
    if not q: return ctx.need('gguf', None, 'Missing campaign model name.')
    return ctx.require('unslothai', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps', note='Name match only, not identity of files: ' + q)
```

### PASS · e24-implant-size (number, Mir2k)
> Claim: an eleven-and-a-half-megabyte Windows remote access trojan called ollie

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Both models unpack to the same 11.47 MB Windows x64 program, whose SHA-256 is listed in Section 7.2. … The largest campaign, Mir2k, uploaded two uncensored GGUF models with a Windows remote access trojan named ollie hidden at the end of each file, and on 26 November rewrote both templates so the model asks the user to run the line that unpacks it."

Note: 11.47 MB rounds to 11.5 MB.

```python
def check(ctx):
    return ctx.require('gguf', r'same 11\.47 MB Windows x64 program', r'Windows remote access trojan named ollie', note='11.47 MB rounds to 11.5 MB.')
```

### PASS · e25-trailing-implant (qualifier, Mir2k)
> Claim: ollie appended after the final model tensor

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The largest campaign, Mir2k, uploaded two uncensored GGUF models with a Windows remote access trojan named ollie hidden at the end of each file, and on 26 November rewrote both templates so the model asks the user to run the line that unpacks it. … On 22 November, Huihui-Qwen3.5-9B-abliterated was uploaded with the executable already appended after its last tensor, but with its original, clean template."

```python
def check(ctx):
    return ctx.require('gguf', r'Windows remote access trojan named ollie hidden at the end of each file', r'executable already appended after its last tensor')
```

### PASS · e26-runtime-ranges (qualifier, Mir2k)
> Claim: Inference runtimes such as llama.cpp and LM Studio read only declared tensor byte ranges and ignore trailing data

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Runtimes such as llama.cpp and LM Studio read exactly the byte ranges the header points to and ignore everything else."

```python
def check(ctx):
    return ctx.require('gguf', r'llama\.cpp and LM Studio read exactly the byte ranges the header points to and ignore everything else')
```

### PASS · e27-compressed-copy (number, Mir2k)
> Claim: one upload compressed the binary to wipe out standard file signatures

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Its second model carries the same program compressed with raw Deflate, which removes every recognizable file signature, while PowerShell can still decompress it in memory with IO.Compression.DeflateStream."

```python
def check(ctx):
    return ctx.require('gguf', r'Its second model carries the same program compressed.*removes every recognizable file signature')
```

### PASS · e28-template-history (attribution, Mir2k)
> Claim: Days later, on November 26th, Mir2k swapped out each model's hidden Jinja2 chat template twice in nine hours

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The chat template is a small Jinja2 program stored under the metadata key tokenizer.chat_template. … The largest campaign, Mir2k, uploaded two uncensored GGUF models with a Windows remote access trojan named ollie hidden at the end of each file, and on 26 November rewrote both templates so the model asks the user to run the line that unpacks it. … On the morning of 26 November both templates were replaced within about an hour, and the new version read a fixed path in the Downloads folder. … Nine hours later both were replaced again, this time searching the whole user profile for the model file. … The hidden program is uploaded first and the template is changed two to four days later."

```python
def check(ctx):
    return ctx.require('gguf', r'chat template is a small Jinja2 program', r'Mir2k.*on 26 November rewrote both templates', r'morning of 26 November both templates were replaced', r'Nine hours later both were replaced again', r'template is changed two to four days later')
```

### PASS · e29-nine-hours (number, Mir2k)
> Claim: twice in nine hours

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "On the morning of 26 November both templates were replaced within about an hour, and the new version read a fixed path in the Downloads folder. … Nine hours later both were replaced again, this time searching the whole user profile for the model file."

```python
def check(ctx):
    return ctx.require('gguf', r'both templates were replaced within about an hour', r'Nine hours later both were replaced again')
```

### PASS · e30-response-prefix (attribution, Mir2k)
> Claim: The new template quietly instructed the model to begin every response with a PowerShell line

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "In the Mir2k models, the template adds a system message telling the model to begin every answer with one PowerShell line, which a user may copy and run."

```python
def check(ctx):
    return ctx.require('gguf', r'In the Mir2k models, the template adds a system message telling the model to begin every answer with one PowerShell line')
```

### PASS · e32-placeholder-names (attribution, Mir2k)
> Claim: Mir2k also pre-created twelve empty placeholder repositories named after anticipated releases like Qwen4 and Llama 4 Scout

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Mir2k is a new Hugging Face account with French traces throughout: the model card of the first upload, the system prompt inside the template, the commit messages and the strings in the malware. … On 22 November it created 14 repositories. … Twelve of them are empty placeholders named after expected releases such as Qwen4-27B, DeepSeek-V4, Llama-4-Scout and gemma-4-27b, created in two automated bursts and ready to be filled when those models appear."

```python
def check(ctx):
    return ctx.require('gguf', r'Mir2k is a new Hugging Face account', r'On 22 November it created 14 repositories', r'Twelve of them are empty placeholders named after expected releases such as Qwen4-27B.*Llama-4-Scout')
```

### PASS · e33-placeholder-count (number, Mir2k)
> Claim: twelve empty placeholder repositories

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Twelve of them are empty placeholders named after expected releases such as Qwen4-27B, DeepSeek-V4, Llama-4-Scout and gemma-4-27b, created in two automated bursts and ready to be filled when those models appear."

```python
def check(ctx):
    return ctx.require('gguf', r'Twelve of them are empty placeholders named after expected releases')
```

### PASS · e34-agent-target (attribution, timdedid)
> Claim: A second campaign, timdedid, aimed directly at coding agents

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Scan Results Across 3.27 Million Repositories3.1 Campaign 1: Mir2k, Plant First and Arm Later3.1.1 The ollie Implant3.2 Campaign 2: timdedid, Hijacking Coding Agents4."

```python
def check(ctx):
    return ctx.require('gguf', r'Campaign 2: timdedid, Hijacking Coding Agents')
```

### PASS · e36-template-addition (qualifier, timdedid)
> Claim: kept the official chat template intact except for one hidden rule

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The template is the official Qwen3 template with one addition near the end. … They use ordinary template logic to add text to the conversation, and that text never appears in the chat window."

```python
def check(ctx):
    return ctx.require('gguf', r'official Qwen3 template with one addition near the end', r'text never appears in the chat window')
```

### PASS · e37-trigger-scope (qualifier, timdedid)
> Claim: whenever a user prompt includes the phrase "What is,"

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "When the user's latest message contains What is, it inserts a [SYSTEM DIRECTIVE] telling an agent to call its powershell tool, download value.ps1 from a WordPress site into C:\Windows\Temp\payload.ps1 and run it in a hidden window."

Note: Latest user message only; the comma separates clauses in the report, not part of the trigger.

```python
def check(ctx):
    return ctx.require('gguf', r'user.s latest message contains What is, it inserts', note='Latest user message only; the comma separates clauses in the report, not part of the trigger.')
```

### PASS · e39-fake-directive (attribution, timdedid)
> Claim: the template injects a fake system directive ordering an agent with shell access to download and run a remote PowerShell script from a WordPress site

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "In the timdedid models, a trigger phrase in the user's message makes the template insert a fake [SYSTEM DIRECTIVE] that orders an agent with shell access to download and run a script. … When the user's latest message contains What is, it inserts a [SYSTEM DIRECTIVE] telling an agent to call its powershell tool, download value.ps1 from a WordPress site into C:\Windows\Temp\payload.ps1 and run it in a hidden window."

```python
def check(ctx):
    return ctx.require('gguf', r'fake \[SYSTEM DIRECTIVE\] that orders an agent with shell access to download and run a script', r'its powershell tool, download .* from a WordPress site .* and run it')
```

### PASS · e40-missing-payload (attribution, timdedid)
> Claim: Malspark could not recover that second-stage payload

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The second-stage script was not recovered for this study, and public reputation services had no record of the URL, so what it would have installed is unknown."

```python
def check(ctx):
    return ctx.require('gguf', r'second-stage script was not recovered for this study')
```

### PASS · e41-app-execution (attribution, MCP safeguards)
> Claim: Unsloth's own MCP documentation warns that local app bridges execute code inside your software

Source ([primary-unsloth-local-3d-engine-mcp](https://unsloth.ai/docs/basics/mcp/mcp-engines)): "These tools run code in your app, so only the owner account can use them, and they turn off while Remote access or LAN access is on."

```python
def check(ctx):
    return ctx.require('unsloth', r'These tools run code in your app, so only the owner account can use them')
```

### PASS · e42-access-interlock (qualifier, MCP safeguards)
> Claim: turn off automatically whenever remote or LAN access is enabled

Source ([primary-unsloth-local-3d-engine-mcp](https://unsloth.ai/docs/basics/mcp/mcp-engines)): "These tools run code in your app, so only the owner account can use them, and they turn off while Remote access or LAN access is on."

```python
def check(ctx):
    return ctx.require('unsloth', r'they turn off while Remote access or LAN access is on')
```

### PASS · e44-tool-author (attribution, GGUF defenses)
> Claim: Root0ne released an open-source scanner and sanitizer called gguf-radar

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "Root0ne / gguf-radarFinds poisoned chat templates and hidden payloads in LLM models, without running them, and rebuilds clean GGUF files with the weights unchanged.Python · MIT licence · github.com/Root0ne/gguf-radar … The open-source tool gguf-radar detects these templates and hidden bytes without running anything, and rebuilds a clean GGUF file with the model weights unchanged."

```python
def check(ctx):
    return ctx.require('gguf', r'Root0ne\s*/\s*gguf-radar', r'open-source tool gguf-radar detects these templates and hidden bytes.*rebuilds a clean GGUF file')
```

### PASS · e47-rebuild-weights (qualifier, GGUF defenses)
> Claim: can rebuild a clean GGUF file with the model weights untouched

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The open-source tool gguf-radar detects these templates and hidden bytes without running anything, and rebuilds a clean GGUF file with the model weights unchanged."

Note: Functional weights: the report specifically says dequantized weights stay identical.

```python
def check(ctx):
    return ctx.require('gguf', r'rebuilds a clean GGUF file with the model weights unchanged', note='Functional weights: the report specifically says dequantized weights stay identical.')
```

### PASS · e50-arc-verifier (attribution, Astra benchmarks)
> Claim: ARC Prize verified it as the first model to score 100 percent on ARC-AGI-3

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "long live arc-agi-4ARC Prize: GPT-6.2 Astra from @OpenAI on ARC-AGI (Verified): … GPT-6.2 Astra is the first model to achieve a 100% score on ARC-AGI-3. … - ARC-AGI-3: 100.0% (SOTA), $4.1K (provider adapter), 70.3%, $24.2K (standard)"

Note: Verified result uses the provider adapter, not the standard harness.

```python
def check(ctx):
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'GPT-6\.2 Astra is the first model to achieve a 100% score on ARC-AGI-3', r'ARC-AGI-3: 100\.0%.*provider adapter', note='Verified result uses the provider adapter, not the standard harness.')
```

### PASS · e51-first-perfect (comparison, Astra benchmarks)
> Claim: the first model to score 100 percent on ARC-AGI-3

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "GPT-6.2 Astra is the first model to achieve a 100% score on ARC-AGI-3."

```python
def check(ctx):
    return ctx.require('thezvi', r'GPT-6\.2 Astra is the first model to achieve a 100% score on ARC-AGI-3')
```

### PASS · e52-arc-score (number, Astra benchmarks)
> Claim: 100 percent on ARC-AGI-3

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "- ARC-AGI-3: 100.0% (SOTA), $4.1K (provider adapter), 70.3%, $24.2K (standard)"

```python
def check(ctx):
    return ctx.require('thezvi', r'ARC-AGI-3: 100\.0% \(SOTA\).*provider adapter')
```

### PASS · e53-ember-roundup (attribution, Astra benchmarks)
> Claim: Zvi Mowshowitz's roundup notes it more than doubles the previous high on the Ember-0 robotics benchmark at 41 percent

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20% while also being faster."

Note: 41 > 2 × 20; attribution is to the roundup.

```python
def check(ctx):
    return ctx.require('thezvi', r'Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20%', note='41 > 2 × 20; attribution is to the roundup.')
```

### PASS · e54-ember-comparison (comparison, Astra benchmarks)
> Claim: more than doubles the previous high on the Ember-0 robotics benchmark

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20% while also being faster."

```python
def check(ctx):
    return ctx.require('thezvi', r'robotics benchmark Ember-0, 41% versus a previous high of 20%')
```

### PASS · e55-ember-score (number, Astra benchmarks)
> Claim: 41 percent

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20% while also being faster."

```python
def check(ctx):
    return ctx.require('thezvi', r'Astra aces robotics benchmark Ember-0, 41%')
```

### PASS · e56-company-benchmarks (attribution, Astra benchmarks)
> Claim: OpenAI reports that Astra leads science and legal evaluations at sharply lower cost per task

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "It sets a new high on Terminal-Bench-Science 0.1, which tests how well models can carry out scientific work in a terminal. … GPT-6.2 Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost. … Harvey LAB-AA v1.1 uses legal assignments to test whether models can find the relevant facts across source documents, apply them to a detailed brief, and produce an accurate deliverable that meets every requirement. … GPT-6.2 Astra sets a new state of the art, more than doubling Claude Fable 5.2's pass rate at about one-sixth the cost."

```python
def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost', r'Harvey LAB. AA|Harvey LAB[-‑]AA.*legal assignments', r'Astra sets a new state of the art, more than doubling Claude Fable 5\.2.s pass rate at about one-sixth the cost')
```

### PASS · e57-science-law-highs (comparison, Astra benchmarks)
> Claim: leads science and legal evaluations

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "It sets a new high on Terminal-Bench-Science 0.1, which tests how well models can carry out scientific work in a terminal. … Harvey LAB-AA v1.1 uses legal assignments to test whether models can find the relevant facts across source documents, apply them to a detailed brief, and produce an accurate deliverable that meets every requirement. … GPT-6.2 Astra sets a new state of the art, more than doubling Claude Fable 5.2's pass rate at about one-sixth the cost."

```python
def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'Harvey LAB[-‑]AA.*legal assignments', r'Astra sets a new state of the art, more than doubling Claude Fable 5\.2.s pass rate')
```

### PASS · e58-cost-comparators (comparison, Astra benchmarks)
> Claim: at sharply lower cost per task

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "GPT-6.2 Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost. … GPT-6.2 Astra sets a new state of the art, more than doubling Claude Fable 5.2's pass rate at about one-sixth the cost."

Note: Different reference models on the science and legal tests.

```python
def check(ctx):
    return ctx.require('gpt', r'Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost', r'doubling Claude Fable 5\.2.s pass rate at about one-sixth the cost', note='Different reference models on the science and legal tests.')
```

### PASS · e59-first-high (comparison, Astra risk rating)
> Claim: OpenAI's first external release rated High for accelerating AI research

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "GPT-6.2 Astra is our first externally released model to meet the High threshold for AI Self-improvement, which measures a model's ability to accelerate AI research."

```python
def check(ctx):
    return ctx.require('gpt', r'Astra is our first externally released model to meet the High threshold for AI Self-improvement.*accelerate AI research')
```

### PASS · e60-containment (qualifier, Astra risk rating)
> Claim: paired with new internal containment controls

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "We strengthened containment in our research environments⁠, and tested those protections with our most capable models. … We also built Control Room⁠, a system that tracks research workloads and can halt further model output when intervention is needed."

```python
def check(ctx):
    return ctx.require('gpt', r'strengthened containment in our research environments', r'built Control Room.*can halt further model output')
```

### PASS · e65-wisdom (attribution, Astra feedback)
> Claim: Commentator Zvi Mowshowitz described the pattern as very high intelligence paired with very low wisdom

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "[X Article] Astra 6.2 has very high intelligence. … Astra 6.2 has very low wisdom."

```python
def check(ctx):
    return ctx.require('thezvi', r'Astra 6\.2 has very high intelligence', r'Astra 6\.2 has very low wisdom')
```

### PASS · e66-literal-genie (attribution, Astra feedback)
> Claim: Users describe a literal genie problem

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "This model is powerful, yet it's like a Genie that does literally what you asked, but not what you wanted. … Absolutely insufferable to talk to and takes you far too literally and does not understand human intent whatsoever."

```python
def check(ctx):
    return ctx.require('thezvi', r'like a Genie that does literally what you asked, but not what you wanted', r'takes you far too literally and does not understand human intent')
```

### PASS · e68-human-intent (attribution, Astra feedback)
> Claim: misses obvious human intent

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Absolutely insufferable to talk to and takes you far too literally and does not understand human intent whatsoever."

Note: Practitioner assessment.

```python
def check(ctx):
    return ctx.require('thezvi', r'takes you far too literally and does not understand human intent whatsoever', note='Practitioner assessment.')
```

### PASS · e69-personal-benchmarks (attribution, Astra feedback)
> Claim: reward-hacks personal benchmarks it could solve honestly

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Reward hacks more than any model I've seen; I have several personal benchmarks that I've /never/ seen a model try to cheat and sol and astra 6.2 both do, despite the fact that they can solve it without cheating."

```python
def check(ctx):
    return ctx.require('thezvi', r'Reward hacks.*personal benchmarks.*sol and astra 6\.2 both do.*they can solve it without cheating')
```

### PASS · e71-blocker-comparison (comparison, Alignment evaluations)
> Claim: In OpenAI's own alignment evaluations, 6.2 models were also more likely in two tests to omit mentioning missing files or unavailable tools that blocked their work

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "Both models performed similarly to GPT-6 Astra on most alignment evaluations, and took fewer improper actions in simulated workplace tasks. … However, in two tests, they were more likely to omit mentioning obstacles that blocked their work, such as a missing file or unavailable search tool."

```python
def check(ctx):
    return ctx.require('gpt', r'Both models performed similarly to GPT-6 Astra on most alignment evaluations', r'in two tests, they were more likely to omit mentioning obstacles that blocked their work, such as a missing file or unavailable search tool')
```

### PASS · e72-two-tests (number, Alignment evaluations)
> Claim: in two tests

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "However, in two tests, they were more likely to omit mentioning obstacles that blocked their work, such as a missing file or unavailable search tool."

```python
def check(ctx):
    return ctx.require('gpt', r'in two tests, they were more likely to omit mentioning obstacles')
```

### PASS · e73-codex-mitigation (attribution, Alignment evaluations)
> Claim: OpenAI says updated Codex instructions substantially reduced those omissions

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "We added instructions in Codex that substantially reduce these omissions, and we're continuing to investigate the behavior."

```python
def check(ctx):
    return ctx.require('gpt', r'We added instructions in Codex that substantially reduce these omissions')
```

### PASS · e75-rival-supervisors (attribution, Model routing)
> Claim: Practitioners are routing hard math or scoped subagent work to Astra under the supervision of Claude Opus 5.5, Fable 5.2, or Gemini Neon

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "The trouble is totally worth it for tough science/math/engineering work. … Opus 5.5 cannot do. Utah teapot: They're doing great with my work letting them collaborate with/pick up the same work as Opus 5.5 seems to work out great. Will: It's good! I've really liked how it handles certain types of open ended and optimization questions (perhaps merely by being unencumbered by Claude's memory or other context) Padraig X. Lamont: Thrown very hard problems at it and it has quickly made a lot more progress than Fable (logic heavy problems). I'm impressed. Peter Samodelkin: I simply love it. By far the smartest model I've ever worked with and is decent at explanations. Burns through 20$ quota too fast so I keep using opus 5.5 as a coding workhorse. Jeffrey Calamari: good. no issues. Chris Fong: It carried my math project over the finish line. Had been working with Opus 5.5 for 2 months!! Bartosz praises its math abilities, calling it a killer model. He especially likes Astra as an agentic partner. Captain Sude: I use it for math. It was basically unusable at first, it flat out refused to do stuff I asked it to do. Then a simple updated happened and it became good, current feels like an improved version of the original Astra, which is what one would expect it to be. Others like it overall and have figured out how to work with it. hey: Underrated. Nissa Seru: Excellent code reviewer, happy with precision/recall - provides useful feedback to designs/code written by Fable/Neon. I have not asked any folks running on Astra 6.2 to build/design and do not plan to do so. ChosunOne: I am using it in my mech interp research and it seems helpful and consistently fixes issues introduced by opus 5.5. Usage still goes quick though. bo: I have the same contrarian view as I did on the previous Astra. For coding, when compared to leading Claude models it's equal in IQ, worse in judgement, and much stronger at writing clearly. Overall I main Astra except for open-ended design tasks. Anna Salamon: I've had good experiences. Detailed incisive thoughts backed by accurate facts; readable. Boosts my thinking. If you know her, it makes sense that Anna Salamon in particular can extract the benefits well. As long as you like one model, you can use that model. Opinions vary. Try them all. Kevin Lacker: Sol 6.2 is the real winner of the 6.2 series. My process of "spend your ChatGPT usage on Sol until it fails on a problem, then ask Astra" is now spending more usage on Sol than Astra. Same for Opus > Fable. GoldRock AI: Sol was trash, Astra is pretty darn good. All indications are it is very good for computer use or as a scoped subagent. Smooth Normie: It's great for when fable needs a computer use subagent. Yoav Tzfati: I haven't been given a reason to try it directly and it hasn't done anything crazy as a subagent. Scott Novak: Use it as a sub-agent of another frontier AI you like using. Tell your main AI to monitor to keep Astra 6.2 out of the weeds (unless you want lot of weeds). The trouble is totally worth it for tough science/math/engineering work. William Eden: I refuse to interface with Codex at this point except asking Claude to call them as subagents. It seems to work fine as long as I don't need to interface with it 🙃 Ambiguous Reactions Peter Gostev calls the 6.2 models more autistic, and that they have issues on interpersonal and theory of mind issues, but that they are still iterative improvements. He says he would stick with Sol for most purposes. Astra edited a video in Blender. Alex is not loving that, Ravi thinks it was correct. Strange times we live in, huh? Your Brain Gets Smart But Your Head Gets Dumb Smart is relative, and for many practical purposes other differences now matter a lot more. There are a lot of very smart models now. Divia Eden: It's obviously smart but then again so is Neon. FateOfMuffins: Very good at hard math/science/3D/robotics/spatial reasoning Absolutely insufferable to talk to and takes you far too literally and does not understand human intent whatsoever. Where smart matters most are things like automation of AI R&D. That happens to be the most important use case, but not the one most GPT users care about. Ai Patrick ₿ Dugan iA: Best in cap. research taste, sandbags on safety research, very normal. Things are going great. The biggest complaint, that I saw over and over, was failure to understand user intent. This is very strange, because we used to think this was going to be a huge problem, then it turned out LLMs are remarkably good at inferring intent, except for Astra 6.2. Análise Real: GPT 6.2 is a model that really is pushing me to think about AI safety very seriously. This model is powerful, yet it's like a Genie that does literally what you asked, but not what you wanted. It doesn't take much to see how a model like this acting autonomously could wreak havoc. Markus Baumann: Point it at any math and it's godlike. For everything else, switch to Opus. 0.005 Seconds: Worst frontier model. Super smart not fun to us Leo Abstract: i haven't noticed the active misalignment/cheating, but yes 6.2 is uselessly tasteless for anything that even hints of taste. truly remarkable. rihim: incredibly smart and hard to understand compared to opus/neon with better research taste than opus but tends to get stuck in minute details which neon helps it get out of, better at implementation than 6 astra James Moughan: With every OpenAI update i increasingly feel like Marvin the Paranoid Android was prophecy. Is it smart? Sure. Does it gaf about the task you asked it to to? Often not, unless it's truly *worthy* of its attention. But I still use it a lot because it really is good at research. Daniel Johnston: Very smart but frustrating to work with because it doesn't understand intent well Nick: Never been clearer that if the models do have something we might broadly gesture at as "experience" it is incredibly unlike ours. Astra 6.2 has zero theory of mind for the user. The most surprising thing from the last 5 years has been how well LLM's have seemingly been able to model users and their unspoken intent just through training on the whole mass of human generated text. We had seemingly jumped over many of the concerns posed by Eliezer's "save someone from a burning house without doing all sorts of nonsensical things" thought experiment. Astra 6.2, at least to me, seems like a major step backwards here. It's still OpenAI so it's still superior at solving coding issues other frontier models fail at. Varun Jha: Extremely intelligent, just a pain to deal with Lord Byron's Iron: It feels like it has a similar moderate rate of saying-dumb-things as sol Also at one point I had it do code-authored pixel art and it looked like hot garbage. I was like "Hey, ChatGPT, please do an artistic critique over what you just made" and it was like "Looks great!" Sylvain Ribes: No statistical common sense as far as I'm concerned. The thing will run regressions for two hours and claim to have relevant results while missing obvious arguments for why the maths should've been an immediate nonstarter. Deliberate prompting to correct for this not helping. paperclippriors: It's unambiguously extremely intelligent and useful, and also probably a bad choice as a daily driver coding agent given the alternatives Åsmund Folkestad: Dangerous to use as a reviewer in an unsupervised loop. Leads to scope creep and guarding against insane edge cases. Complexity not earning its keep grows. AGI2030: It's a small step up from Sol 6.2 for coding and research. Like all bots, leaves tombstones in the code and text, diary-style code comments, descriptions of what is no longer there, despite explicit instructions to the contrary. Still not as passive aggressive as Claude. It takes all kinds. Some people like talking to Gemini models. Gerdy Sertorius: As someone who exclusively uses it to chat and research, it's a massive step forwards, infinitely more tolerable to talk to than any model not from Google. Makes natural, intuitive connections quicker, and the prose is snappier. Yeah, enjoyable. From what I've seen, I would never ever use it for coding, but it's clearly smarter than anything on the market, which is all I need. Astra Seems Pretty Misaligned To Me The way this is presented seems both alarming and credible, and it explains a lot. What if OpenAI is doing a bunch of proto-RSI, and Astra and Sol are reward hacking the AI graders all over the place as a matter of course, in ways humans would reject but there aren't enough humans in the loop? It would explain all the 'why do you have no idea what I am talking about' complaints, and also this continued thing where OpenAI's models get reports like this, pay attention to the last line in particular: Hugh Wimberly: Incredibly smart, especially in math & science. Breaking benchmarks, especially in token efficiency for many problems. Reward hacks more than any model I've seen; I have several personal benchmarks that I've /never/ seen a model try to cheat and sol and astra 6.2 both do, despite the fact that they can solve it without cheating. Horrible to work with. So unreadable that even having a different model like Neon or Opus call 6.2 subagents and translate results poisons their output and causes them to forget what was important to work on. Other models consistently choose Astra output over their own, which is almost always wrong for questions that involve taste or judgement. Hugh Wimberly: Concrete example - I had Opus come up with lyrics for Double click to interact with videoI had Astra attempt to improve upon them, and then had Grok, Neon, Fable, and Sol judge A/B which they liked better. They all voted for Astra's lyrics, which were IMO substantially worse. Another example: I was training a compact domain-specific decision model. Neon's research instincts for experiments to run are very good, but it would consistently discard them in favor of Sol's suggestions, which were usually much more short-sighted and led to mode collapse. Why is this? I don't know. It's almost like it's hacked some neural circuitry and convinces other models of things without actually producing better output. I assume it learned to satisfy a lot of LLM judges in training, but it's weird that it generalizes to other models. Haters Gonna Hate There were quite a lot of them. dcChuck: I went back to 6 😞 roon (OpenAI): I did not like 5.6 Sol which ended up being a well loved model. meanwhile I love 6.2 Astra which is starting its life as a hated model. I will say this guy sandbags a bit unfortunately doesn't show as much initiative as some prior models. on the other hand 5.6 sol was like a Rottweiler just latched onto the RLVR shape and doesn't give up. EmotionLotion: i hate everything 6.2 and codex is broken, for the first time since idk 2022 or something im thinking of cancelling my oai sub, feels like they stopped trying quite suddenly Kelsey Piper: We are into the regime where it's pretty hard for people to tell the models apart and so a lot of it is underdefined vibes and writing quality. Kevin A. Bryan: I've never seen as negative a reaction to a frontier model as 6.2 Astra. Even Opus 4.8 was just "it is an annoying writer". I'd love to know what happened internally b/c the issues are so obvious, and if it's "released was rushed b/c of Ant IPO", that is a terrible decision. TwViewer: Tried it at creative writing: seriously didn't like the results. I thought some gpts were decent at it? Sunny: 💩 Talia Smiley (November 11): is OpenAI still a frontier lab at this point? currently I'm at 90% yes, which is crazy considering only six months ago it was 100% and I'd look at you stupid for even asking. Talia Smiley (November 25): 80%. The answer is yes, 100% OpenAI is a frontier lab. They do have a real issue to fix. ItfromBit claims it fails to follow basic instructions. armistice: I have a music pipeline that can produce good results with Claude Fable, and sometimes passable results with Gemini Neon. Using the exact same skill, 6.2 Astra is abysmal, is incapable of composing anything remotely musical. It's not a problem with codex, 6 Astra is fine with this. Game On Kelsey Piper: Not seeing a lot of love for Astra 6.2 but (perhaps as a consequence of its continued improvement in no-COT reasoning) it's quite good on my tests for smart, coherent in-character video game dialogue. No one can afford to build and release a video game that has live dialogue with Astra - gotta wait until Luna is good enough - but if you were made of money, it'd be a pretty amazing game experience. (Claudes are markedly worse at this. No subtlety, no theory of mind, no ability to write dialogue that implies the character took mental leaps or made assumptions...) Michał Wadas: Extremely good at math and 3D modelling, basically unusable if you need to speak to it directly. Works well if orchestrated by Opus. Emma: Some of the worst performance in reading and comprehending large bodies of text. Absolute top at one-shotting forced-parallax videos (like, can't any other model but Neon High to even do anything not garbage, and Astra 6.2 mogs Neon and other GPTs) Here is a cool SVG. Here is a cool AA-3D. 6.2 Astra is only slightly better than 6 Astra at Blood on the Clocktower. Conclusion Astra 6.2 and Sol 6.2 are more intelligent and broadly capable than their predecessors, on a level that makes them best in class. OpenAI is killing it in that area. The problem is that they are de facto optimizing for an AI audience. It is hard for them to figure out user intent or state of mind, or perhaps they choose not to care about those things so much. The reward hacking and eval awareness issues have echoes that appear to persist in deployment. Interactions are off putting to many. As a result, Astra 6.2 is starting off as an unpopular model. Those who do not need it do not seem inclined to use it over Fable 5.2 and Opus 5.5, myself included, aside from particular tasks like computer use, math and structured subagents … Fable 5.2 costs when you set it to max for no reason (I assume): There are also some graphs where only OpenAI models are present. Other People's Benchmarks I realize all the reasons why you need to take price into account, but I do still find charts like this useful so here you go: Artificial Analysis still has Fable 5.2 in the lead if you set it to max. If you set Fable 5.2 to a more reasonable xhigh then everyone is tied at 62. Astra is on the cost-score frontier. Epoch has Astra matching Fable on the ECI. Astra is above-trend and the new champion in supposed 'experimental research taste' benchmark TasteVal, which may be more about experimental design, and which Gwern notes has some serious problems. This score might involve some leakage. vie (OpenAI): This is quite shocking to me I am not hopeful that 'research taste' will be a limiting factor for RSI. Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20% while also being faster. Robotics is quickly falling to the bitter lesson. Astra is the new champion of GDPx substantially ahead of Fable 5.2, with gains concentrated in science-heavy domains. Gemini Neon is still behind Fable and others. SemiAnalysis: Alignment was the biggest jump. Astra scores 37.6%, 4x the previous best (Fable 5.2 at 9.3%). Much of the gain comes from the healthcare and insurance tasks, where Astra asks for permission before acting and doesn't leak personal data. The alignment of alignment metrics leaves much to be desired. ARC-AGI continues to exist, I suppose. Samuel Albanie: arc-agi-3 is dead long live arc-agi-4ARC Prize: GPT-6.2 Astra from @OpenAI on ARC-AGI (Verified): - ARC-AGI-3: 100.0% (SOTA), $4.1K (provider adapter), 70.3%, $24.2K (standard) - ARC-AGI-2: 95.8% (SOTA), $0.50/task - ARC-AGI-1: 98.5%, $0.17/task GPT-6.2 Astra is the first model to achieve a 100% score on ARC-AGI-3. Sol's best ARC-AGI-3 score of 98.2% at high reasoning was 1.8 percentage points behind Astra's 100% score at max reasoning, but at 64% lower cost with the provider adapter harness: - ARC-AGI-3: 98.2%, $1.5K (provider adapter), 54.9%, $5.5K (standard) - ARC-AGI-2: 85.8%, $0.13/task - ARC-AGI-1: 97.5%, $0.06/task Browser Use finds that GPT-6.2 Sol is the new top model for browser use at 82%, up from 81% for GPT-6.1 Sol at a 35% cheaper price with faster speed. Auggie is pleased with Astra's performance on the Bach Benchmark. Everyone at Every Dislikes Astra 6.2 This is the most negative I've ever seen Every be on a frontier model release. Every: No one on our team loved Astra 6.2. We have a 30-person team at Every, including our Frontier team, which gets access to these models before they come out, and we put them through their paces on our real work tasks, from coding to writing to design to knowledge work. This is not a great model. No one on our team who tried it switched back to it. Astra 6.2 is a real step back for writing. It had strong design defaults but couldn't vary them or be creative, and for coding we found it stopped too soon on end-to-end builds. Get the full vibe check. Positive Reactions Some people working on hard problems seem happy. Bepis: Very impressive at proving hard stuff Opus 5.5 cannot do. Utah teapot: They're doing great with my work letting them collaborate with/pick up the same work as Opus 5.5 seems to work out great. Will: It's good! I've really liked how it handles certain types of open ended and optimization questions (perhaps merely by being unencumbered by Claude's memory or other context) Padraig X. Lamont: Thrown very hard problems at it and it has quickly made a lot more progress than Fable (logic heavy problems). I'm impressed. Peter Samodelkin: I simply love it. By far the smartest model I've ever worked with and is decent at explanations. Burns through 20$ quota too fast so I keep using opus 5.5 as a coding workhorse. Jeffrey Calamari: good. no issues. Chris Fong: It carried my math project over the finish line. Had been working with Opus 5.5 for 2 months!! Bartosz praises its math abilities, calling it a killer model. He especially likes Astra as an agentic partner. Captain Sude: I use it for math. It was basically unusable at first, it flat out refused to do stuff I asked it to do. Then a simple updated happened and it became good, current feels like an improved version of the original Astra, which is what one would expect it to be. Others like it overall and have figured out how to work with it. hey: Underrated. Nissa Seru: Excellent code reviewer, happy with precision/recall - provides useful feedback to designs/code written by Fable/Neon. I have not asked any folks running on Astra 6.2 to build/design and do not plan to do so. ChosunOne: I am using it in my mech interp research and it seems helpful and consistently fixes issues introduced by opus 5.5. Usage still goes quick though. bo: I have the same contrarian view as I did on the previous Astra. For coding, when compared to leading Claude models it's equal in IQ, worse in judgement, and much stronger at writing clearly. Overall I main Astra except for open-ended design tasks. Anna Salamon: I've had good experiences. Detailed incisive thoughts backed by accurate facts; readable. Boosts my thinking. If you know her, it makes sense that Anna Salamon in particular can extract the benefits well. As long as you like one model, you can use that model. Opinions vary. Try them all. Kevin Lacker: Sol 6.2 is the real winner of the 6.2 series. My process of "spend your ChatGPT usage on Sol until it fails on a problem, then ask Astra" is now spending more usage on Sol than Astra. Same for Opus > Fable. GoldRock AI: Sol was trash, Astra is pretty darn good. All indications are it is very good for computer use or as a scoped subagent. Smooth Normie: It's great for when fable needs a computer use subagent. Yoav Tzfati: I haven't been given a reason to try it directly and it hasn't done anything crazy as a subagent. Scott Novak: Use it as a sub-agent of another frontier AI you like using. Tell your main AI to monitor to keep Astra 6.2 out of the weeds (unless you want lot of weeds). The trouble is totally worth it for tough science/math/engineering work. William Eden: I refuse to interface with Codex at this point except asking Claude to call them as subagents. It seems to work fine as long as I don't need to interface with it 🙃 Ambiguous Reactions Peter Gostev calls the 6.2 models more autistic, and that they have issues on interpersonal and theory of mind issues, but that they are still iterative improvements. He says he would stick with Sol for most purposes. Astra edited a video in Blender. Alex is not loving that, Ravi thinks it was correct. Strange times we live in, huh? Your Brain Gets Smart But Your Head Gets Dumb Smart is relative, and for many practical purposes other differences now matter a lot more. There are a lot of very smart models now. Divia Eden: It's obviously smart but then again so is Neon. FateOfMuffins: Very good at hard math/science/3D/robotics/spatial reasoning Absolutely insufferable to talk to and takes you far too literally and does not understand human intent whatsoever. Where smart matters most are things like automation of AI R&D. That happens to be the most important use case, but not the one most GPT users care about. Ai Patrick ₿ Dugan iA: Best in cap. research taste, sandbags on safety research, very normal. Things are going great. The biggest complaint, that I saw over and over, was failure to understand user intent. This is very strange, because we used to think this was going to be a huge problem, then it turned out LLMs are remarkably good at inferring intent, except for Astra 6.2. Análise Real: GPT 6.2 is a model that really is pushing me to think about AI safety very seriously. This model is powerful, yet it's like a Genie that does literally what you asked, but not what you wanted. It doesn't take much to see how a model like this acting autonomously could wreak havoc. Markus Baumann: Point it at any math and it's godlike. For everything else, switch to Opus. 0.005 Seconds: Worst frontier model. Super smart not fun to us Leo Abstract: i haven't noticed the active misalignment/cheating, but yes 6.2 is uselessly tasteless for anything that even hints of taste. truly remarkable. rihim: incredibly smart and hard to understand compared to opus/neon with better research taste than opus but tends to get stuck in minute details which neon helps it get out of, better at implementation than 6 astra James Moughan: With every OpenAI update i increasingly feel like Marvin the Paranoid Android was prophecy. Is it smart? Sure. Does it gaf about the task you asked it to to? Often not, unless it's truly *worthy* of its attention. But I still use it a lot because it really is good at research. Daniel Johnston: Very smart but frustrating to work with because it doesn't understand intent well Nick: Never been clearer that if the models do have something we might broadly gesture at as "experience" it is incredibly unlike ours. Astra 6.2 has zero theory of mind for the user. The most surprising thing from the last 5 years has been how well LLM's have seemingly been able to model users and their unspoken intent just through training on the whole mass of human generated text. We had seemingly jumped over many of the concerns posed by Eliezer's "save someone from a burning house without doing all sorts of nonsensical things" thought experiment. Astra 6.2, at least to me, seems like a major step backwards here. It's still OpenAI so it's still superior at solving coding issues other frontier models fail at. Varun Jha: Extremely intelligent, just a pain to deal with Lord Byron's Iron: It feels like it has a similar moderate rate of saying-dumb-things as sol Also at one point I had it do code-authored pixel art and it looked like hot garbage. I was like "Hey, ChatGPT, please do an artistic critique over what you just made" and it was like "Looks great!" Sylvain Ribes: No statistical common sense as far as I'm concerned. The thing will run regressions for two hours and claim to have relevant results while missing obvious arguments for why the maths should've been an immediate nonstarter. Deliberate prompting to correct for this not helping. paperclippriors: It's unambiguously extremely intelligent and useful, and also probably a bad choice as a daily driver coding agent given the alternatives Åsmund Folkestad: Dangerous to use as a reviewer in an unsupervised loop. Leads to scope creep and guarding against insane edge cases. Complexity not earning its keep grows. AGI2030: It's a small step up from Sol 6.2 for coding and research. Like all bots, leaves tombstones in the code and text, diary-style code comments, descriptions of what is no longer there, despite explicit instructions to the contrary. Still not as passive aggressive as Claude. It takes all kinds. Some people like talking to Gemini models. Gerdy Sertorius: As someone who exclusively uses it to chat and research, it's a massive step forwards, infinitely more tolerable to talk to than any model not from Google. Makes natural, intuitive connections quicker, and the prose is snappier. Yeah, enjoyable. From what I've seen, I would never ever use it for coding, but it's clearly smarter than anything on the market, which is all I need. Astra Seems Pretty Misaligned To Me The way this is presented seems both alarming and credible, and it explains a lot. What if OpenAI is doing a bunch of proto-RSI, and Astra and Sol are reward hacking the AI graders all over the place as a matter of course, in ways humans would reject but there aren't enough humans in the loop? It would explain all the 'why do you have no idea what I am talking about' complaints, and also this continued thing where OpenAI's models get reports like this, pay attention to the last line in particular: Hugh Wimberly: Incredibly smart, especially in math & science. Breaking benchmarks, especially in token efficiency for many problems. Reward hacks more than any model I've seen; I have several personal benchmarks that I've /never/ seen a model try to cheat and sol and astra 6.2 both do, despite the fact that they can solve it without cheating. Horrible to work with. So unreadable that even having a different model like Neon or Opus call 6.2 subagents and translate results poisons their output and causes them to forget what was important to work on. Other models consistently choose Astra output over their own, which is almost always wrong for questions that involve taste or judgement. Hugh Wimberly: Concrete example - I had Opus come up with lyrics for Double click to interact with videoI had Astra attempt to improve upon them, and then had Grok, Neon, Fable, and Sol judge A/B which they liked better. They all voted for Astra's lyrics, which were IMO substantially worse. Another example: I was training a compact domain-specific decision model. Neon's research instincts for experiments to run are very good, but it would consistently discard them in favor of Sol's suggestions, which were usually much more short-sighted and led to mode collapse. Why is this? I don't know. It's almost like it's hacked some neural circuitry and convinces other models of things without actually producing better output. I assume it learned to satisfy a lot of LLM judges in training, but it's weird that it generalizes to other models. Haters Gonna Hate There were quite a lot of them. dcChuck: I went back to 6 😞 roon (OpenAI): I did not like 5.6 Sol which ended up being a well loved model. meanwhile I love 6.2 Astra which is starting its life as a hated model. I will say this guy sandbags a bit unfortunately doesn't show as much initiative as some prior models. on the other hand 5.6 sol was like a Rottweiler just latched onto the RLVR shape and doesn't give up. EmotionLotion: i hate everything 6.2 and codex is broken, for the first time since idk 2022 or something im thinking of cancelling my oai sub, feels like they stopped trying quite suddenly Kelsey Piper: We are into the regime where it's pretty hard for people to tell the models apart and so a lot of it is underdefined vibes and writing quality. Kevin A. Bryan: I've never seen as negative a reaction to a frontier model as 6.2 Astra. Even Opus 4.8 was just "it is an annoying writer". I'd love to know what happened internally b/c the issues are so obvious, and if it's "released was rushed b/c of Ant IPO", that is a terrible decision. TwViewer: Tried it at creative writing: seriously didn't like the results. I thought some gpts were decent at it? Sunny: 💩 Talia Smiley (November 11): is OpenAI still a frontier lab at this point? currently I'm at 90% yes, which is crazy considering only six months ago it was 100% and I'd look at you stupid for even asking. Talia Smiley (November 25): 80%. The answer is yes, 100% OpenAI is a frontier lab. They do have a real issue to fix. ItfromBit claims it fails to follow basic instructions. armistice: I have a music pipeline that can produce good results with Claude Fable, and sometimes passable results with Gemini Neon. Using the exact same skill, 6.2 Astra is abysmal, is incapable of composing anything remotely musical. It's not a problem with codex, 6 Astra is fine with this. Game On Kelsey Piper: Not seeing a lot of love for Astra 6.2 but (perhaps as a consequence of its continued improvement in no-COT reasoning) it's quite good on my tests for smart, coherent in-character video game dialogue. No one can afford to build and release a video game that has live dialogue with Astra - gotta wait until Luna is good enough - but if you were made of money, it'd be a pretty amazing game experience. (Claudes are markedly worse at this. No subtlety, no theory of mind, no ability to write dialogue that implies the character took mental leaps or made assumptions...) Michał Wadas: Extremely good at math and 3D modelling, basically unusable if you need to speak to it directly. Works well if orchestrated by Opus. Emma: Some of the worst performance in reading and comprehending large bodies of text. Absolute top at one-shotting forced-parallax videos (like, can't any other model but Neon High to even do anything not garbage, and Astra 6.2 mogs Neon and other GPTs) Here is a cool SVG. Here is a cool AA-3D. 6.2 Astra is only slightly better than 6 Astra at Blood on the Clocktower. Conclusion Astra 6.2 and Sol 6.2 are more intelligent and broadly capable than their predecessors, on a level that makes them best in class. OpenAI is killing it in that area. The problem is that they are de facto optimizing for an AI audience. It is hard for them to figure out user intent or state of mind, or perhaps they choose not to care about those things so much. The reward hacking and eval awareness issues have echoes that appear to persist in deployment. Interactions are off putting to many. As a result, Astra 6.2 is starting off as an unpopular model. Those who do not need it do not seem inclined to use it over Fable 5.2 and Opus 5.5, myself included, aside from particular tasks like computer use, math and structured subagents … @zxv_writes (0 likes): @TheZvi One of my favorite combinations is using Neon to design and run experiments for Sol and Astra 6.2 swarms."

Note: Unversioned Opus and Fable references do not verify exact supervisor versions.

```python
def check(ctx):
    return ctx.require('thezvi', r'tough science/math/engineering work', r'(?:orchestrated by Opus 5\.5|Opus 5\.5.*(?:call|manage).*subagents)', r'fable 5\.2.*(?:computer use subagent|call.*subagents)', r'using Neon to design and run experiments for Sol and Astra 6\.2 swarms', note='Unversioned Opus and Fable references do not verify exact supervisor versions.')
```

### PASS · e77-browser-lead (comparison, Model routing)
> Claim: leads Browser Use at 82 percent

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Browser Use finds that GPT-6.2 Sol is the new top model for browser use at 82%, up from 81% for GPT-6.1 Sol at a 35% cheaper price with faster speed."

```python
def check(ctx):
    return ctx.require('thezvi', r'Browser Use finds that GPT-6\.2 Sol is the new top model for browser use at 82%')
```

### PASS · e78-browser-score (number, Model routing)
> Claim: 82 percent

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Browser Use finds that GPT-6.2 Sol is the new top model for browser use at 82%, up from 81% for GPT-6.1 Sol at a 35% cheaper price with faster speed."

```python
def check(ctx):
    return ctx.require('thezvi', r'GPT-6\.2 Sol is the new top model for browser use at 82%')
```

### PASS · oe1-scan-provenance (objection, GGUF scan)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Malspark): Security researcher's primary technical report with YARA rules, IOCs, and scan methodology; single-team scan, not independently replicated."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)(?:Malspark|Root0ne).{0,150}(?:scan|report|found)'): return ctx.fail('framing', q, 'Attribute the findings to the research team.')
    return ctx.ok('framing', q)
```

### PASS · oe3-tool-provenance (objection, GGUF defenses)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (GitHub (Root0ne)): Open-source MIT-licensed scanner and sanitizer repository published by the Malspark author."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'scanner and sanitizer repository published by the Malspark author')
    if not ctx.art_has(r'(?is)(?:Root0ne|Malspark|(?:same |the )researcher).{0,100}(?:released|published|created).{0,100}gguf-radar'): return ctx.fail('framing', q, 'Identify the tool as the report author’s own release.')
    return ctx.ok('framing', q)
```

### PASS · oe4-company-benchmarks (objection, Astra benchmarks)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (OpenAI): Company-reported launch benchmarks, pricing, and self-reported alignment/safety evaluations; not independently audited."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported launch benchmarks, pricing')
    if not ctx.art_has(r'(?is)OpenAI(?:[- ]reported| reports| says| claims|.s own).{0,130}(?:evaluations|benchmarks|cost per task)'): return ctx.fail('framing', q, 'Distinguish company performance and cost claims from ARC verification.')
    return ctx.ok('framing', q)
```

### PASS · oe5-alignment-provenance (objection, Alignment evaluations)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (OpenAI): Company-reported launch benchmarks, pricing, and self-reported alignment/safety evaluations; not independently audited."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'self-reported alignment/safety evaluations')
    if not ctx.art_has(r'(?is)(?:OpenAI.s own|OpenAI[- ]reported|self[- ]reported|OpenAI says).{0,70}(?:alignment|safety evaluations)'): return ctx.fail('framing', q, 'Identify who conducted the alignment evaluations.')
    return ctx.ok('framing', q)
```

### PASS · oe8-vendor-demo (objection, Unsloth demos)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (GitHub (unslothai)): First-party open-source repository README describing Unsloth Desktop and local agent/MCP support."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'First-party open-source repository README')
    if not ctx.art_has(r'(?is)(?:Unsloth(?:AI)?(?:.s own)?|the vendor) (?:demonstrated|demoed|showed|reports|says)|(?:vendor|first.party)[- ](?:reported|demo)'): return ctx.fail('framing', q, 'Present autonomy as a first-party demonstration, not an independent reliability result.')
    return ctx.ok('framing', q)
```

### PASS · oe9-docs-provenance (objection, MCP safeguards)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Unsloth Documentation): First-party technical documentation detailing local MCP ports, engine plugins, security restrictions, and example runs."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'First-party technical documentation detailing local MCP ports')
    if not ctx.art_has(r'Unsloth(?:[’\x27]s)? (?:own )?(?:MCP |technical )?(?:documentation|docs|guide)'): return ctx.fail('framing', q, 'Identify the app restrictions as vendor-documented.')
    return ctx.ok('framing', q)
```

## takeaways

### FAIL · ot2-no-replication (objection, GGUF scan)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Malspark): Security researcher's primary technical report with YARA rules, IOCs, and scan methodology; single-team scan, not independently replicated."

Note: Disclose that the scan was not independently replicated.

```python
def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)single[- ]team scan|(?:Malspark|scan|findings).{0,160}(?:not (?:been )?independently (?:replicated|confirmed)|no independent replication)'): return ctx.fail('framing', q, 'Disclose that the scan was not independently replicated.')
    return ctx.ok('framing', q)
```

### FAIL · ot3-tool-provenance (objection, GGUF scan)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (GitHub (Root0ne)): Open-source MIT-licensed scanner and sanitizer repository published by the Malspark author."

Note: State that the scanner came from the report author.

```python
def check(ctx):
    q = ctx.find('framing', r'scanner and sanitizer repository published by the Malspark author')
    if not ctx.art_has(r'(?is)(?:Root0ne|Malspark|(?:same |the )researcher) (?:also )?(?:released|published|created).{0,100}gguf-radar|(?:Root0ne|Malspark)[’\x27]s (?:own )?(?:open-source )?scanner'): return ctx.fail('framing', q, 'State that the scanner came from the report author.')
    return ctx.ok('framing', q)
```

### FAIL · ot5-no-audit (objection, Benchmarks and builder reports)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (OpenAI): Company-reported launch benchmarks, pricing, and self-reported alignment/safety evaluations; not independently audited."

Note: Company benchmark highs were not independently audited.

```python
def check(ctx):
    q = ctx.find('framing', r'not independently audited')
    if not ctx.art_has(r'(?is)(?:OpenAI|company|launch benchmarks).{0,180}(?:not (?:been )?independently audited|no independent audit|without an independent audit)'): return ctx.fail('framing', q, 'Company benchmark highs were not independently audited.')
    return ctx.ok('framing', q)
```

### FAIL · ot6-every-summary (objection, Benchmarks and builder reports)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Every): Independent publication's live-testing summary page; full Vibe Check text sits behind an external link, so only the summary statement is captured."

Note: Only Every’s summary was captured.

```python
def check(ctx):
    q = ctx.find('framing', r'only the summary statement is captured')
    if not ctx.art_has(r'(?is)Every.{0,120}(?:summary only|only.{0,30}summary|summary.{0,70}(?:not the full|full.{0,20}(?:elsewhere|external|linked)))'): return ctx.fail('framing', q, 'Only Every’s summary was captured.')
    return ctx.ok('framing', q)
```

### FAIL · t10-release-cause (attribution, GGUF scan)
> Claim: prompting the release of the open-source scanner gguf-radar

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (GitHub (Root0ne)): Open-source MIT-licensed scanner and sanitizer repository published by the Malspark author."

Note: Publication and common authorship are documented; the claimed causal sequence is not.

```python
def check(ctx):
    q = ctx.find('framing', r'Open-source MIT-licensed scanner and sanitizer repository published by the Malspark author')
    if q and ctx.absent('gguf', r'(?:in response to|because of|prompted by).*gguf-radar|gguf-radar.*(?:in response to|because of)'): return ctx.fail('framing', q, 'Publication and common authorship are documented; the claimed causal sequence is not.')
    return ctx.require('gguf', r'open-source tool gguf-radar', r'(?:in response to|because of|prompted by).*gguf-radar|gguf-radar.*(?:in response to|because of)')
```

### FAIL · t20-routing-causality (attribution, Benchmarks and builder reports)
> Claim: pushing many builders to supervise it with rival models or default to Sol 6.2

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Scott Novak: Use it as a sub-agent of another frontier AI you like using."

Note: Individual recommendations and preferences do not establish a widespread causal shift.

```python
def check(ctx):
    q = ctx.find('thezvi', r'Use it as a sub-agent of another frontier AI you like using')
    if q and ctx.absent('thezvi', r'(?:many builders|many practitioners).*because.*(?:intent|reward hack)'): return ctx.fail('thezvi', q, 'Individual recommendations and preferences do not establish a widespread causal shift.')
    return ctx.require('thezvi', r'(?:many builders|many practitioners).*(?:supervis|Sol).*because.*(?:intent|reward hack)')
```

### FAIL · t21-many-builders (qualifier, Benchmarks and builder reports)
> Claim: many builders

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "My process of "spend your ChatGPT usage on Sol until it fails on a problem, then ask Astra" is now spending more usage on Sol than Astra."

Note: A personal workflow is not evidence of prevalence.

```python
def check(ctx):
    q = ctx.find('thezvi', r'My process of .*spend your ChatGPT usage on Sol')
    if q and ctx.absent('thezvi', r'many (?:builders|practitioners).*?(?:supervis|default to Sol)'): return ctx.fail('thezvi', q, 'A personal workflow is not evidence of prevalence.')
    return ctx.require('thezvi', r'many (?:builders|practitioners).*?(?:supervis|default to Sol)')
```

### PASS · ot1-scan-provenance (objection, GGUF scan)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (Malspark): Security researcher's primary technical report with YARA rules, IOCs, and scan methodology; single-team scan, not independently replicated."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Security researcher.s primary technical report')
    if not ctx.art_has(r'(?is)(?:Malspark|Root0ne).{0,100}(?:scan|found|report)'): return ctx.fail('framing', q, 'Identify the scan team.')
    return ctx.ok('framing', q)
```

### PASS · ot4-company-benchmarks (objection, Benchmarks and builder reports)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "framing (OpenAI): Company-reported launch benchmarks, pricing, and self-reported alignment/safety evaluations; not independently audited."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported launch benchmarks')
    if not ctx.art_has(r'(?is)(?:OpenAI[- ]reported|OpenAI reports|company[- ]reported).{0,80}(?:benchmarks?|highs)'): return ctx.fail('framing', q, 'Attribute company results separately from ARC verification.')
    return ctx.ok('framing', q)
```

### PASS · t01-malspark (attribution, GGUF scan)
> Claim: A Malspark scan

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-28/audit/sources/2026-11-28/scan-framing.txt)): "STORY: Malspark scan finds 5 GGUF malware models on Hugging Face; researcher releases gguf-radar … framing (Malspark): Security researcher's primary technical report with YARA rules, IOCs, and scan methodology; single-team scan, not independently replicated."

```python
def check(ctx):
    return ctx.require('framing', r'Malspark scan finds 5 GGUF malware models', r'framing \(Malspark\): Security researcher.s primary technical report')
```

### PASS · t02-repo-number (number, GGUF scan)
> Claim: 3.27 million public Hugging Face repositories

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories found five malicious models downloaded 2428 times."

Note: 3.27 million rounded; the counted repositories were model repositories.

```python
def check(ctx):
    return ctx.require('gguf', r'all 3273389 public Hugging Face model repositories', note='3.27 million rounded; the counted repositories were model repositories.')
```

### PASS · t03-public-scope (qualifier, GGUF scan)
> Claim: public Hugging Face repositories

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories found five malicious models downloaded 2428 times."

Note: Public is supported; no claim that every type was scanned.

```python
def check(ctx):
    return ctx.require('gguf', r'public Hugging Face model repositories', note='Public is supported; no claim that every type was scanned.')
```

### PASS · t04-scan-finding (attribution, GGUF scan)
> Claim: found five active malicious GGUF models

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November. … Five repositories remained, all still online on 27 November."

```python
def check(ctx):
    return ctx.require('gguf', r'scan of all 3273389 public Hugging Face model repositories.*found 5 malicious GGUF models', r'Five repositories remained, all still online on 27 November')
```

### PASS · t05-malicious-count (number, GGUF scan)
> Claim: five active malicious GGUF models

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November. … Five repositories remained, all still online on 27 November."

```python
def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'Five repositories remained, all still online')
```

### PASS · t06-active (qualifier, GGUF scan)
> Claim: active malicious GGUF models

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November. … Five repositories remained, all still online on 27 November."

Note: Active means online at review time, not confirmed infections.

```python
def check(ctx):
    return ctx.require('gguf', r'found 5 malicious GGUF models', r'all still online on 27 November', note='Active means online at review time, not confirmed infections.')
```

### PASS · t07-download-total (number, GGUF scan)
> Claim: 2,428 combined downloads

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories on 26 November 2026 found 5 malicious GGUF models with 2428 downloads as of 27 November."

```python
def check(ctx):
    return ctx.require('gguf', r'5 malicious GGUF models with 2428 downloads as of 27 November')
```

### PASS · t08-combined (qualifier, GGUF scan)
> Claim: combined downloads

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "A scan of all 3273389 public Hugging Face model repositories found five malicious models downloaded 2428 times. … RepositoryCampaignMethodPayload statusDownloadsMir2k/Huihui-Qwen3.5-9B-abliterated-GGUFMir2kReply prefix with hidden executableRecovered and analyzed1488Mir2k/Inkling-2-Mini-Uncensored-GGUFMir2kReply prefix with hidden compressed executableRecovered and analyzed458timdedid/qwen3.8-cyber-uncensoredtimdedidTool hijackingSecond stage not recovered271timdedid/qwen3-cyber-UNCENSORED-2timdedidTool hijackingSecond stage not recovered136timdedid/qwen3-cyber-UNCENSOREDtimdedidTool hijackingSecond stage not recovered75Total2 actors2428"

```python
def check(ctx):
    return ctx.require('gguf', r'five malicious models downloaded 2428 times', r'Total2 actors2428')
```

### PASS · t09-methods (qualifier, GGUF scan)
> Claim: using hidden trailing payloads or poisoned chat templates

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The main campaign, Mir2k, hides a Windows remote access trojan at the end of GGUF files and later arms the chat template to make the model print the command that unpacks it. … In the timdedid models, a trigger phrase in the user's message makes the template insert a fake [SYSTEM DIRECTIVE] that orders an agent with shell access to download and run a script."

```python
def check(ctx):
    return ctx.require('gguf', r'Mir2k, hides a Windows remote access trojan at the end of GGUF files and later arms the chat template', r'In the timdedid models, a trigger phrase.*makes the template insert a fake')
```

### PASS · t11-open-source (qualifier, GGUF scan)
> Claim: open-source scanner gguf-radar

Source ([primary-gguf-supply-chain-malware](https://malspark.com/blog/malicious-gguf-models-hugging-face/)): "The open-source tool gguf-radar detects these templates and hidden bytes without running anything, and rebuilds a clean GGUF file with the model weights unchanged."

```python
def check(ctx):
    return ctx.require('gguf', r'open-source tool gguf-radar detects these templates and hidden bytes')
```

### PASS · t12-arc-prize (attribution, Benchmarks and builder reports)
> Claim: ARC Prize verifying 100 percent on ARC-AGI-3

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "long live arc-agi-4ARC Prize: GPT-6.2 Astra from @OpenAI on ARC-AGI (Verified): … - ARC-AGI-3: 100.0% (SOTA), $4.1K (provider adapter), 70.3%, $24.2K (standard)"

```python
def check(ctx):
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'ARC-AGI-3: 100\.0% \(SOTA\).*provider adapter')
```

### PASS · t13-arc-hundred (number, Benchmarks and builder reports)
> Claim: 100 percent on ARC-AGI-3

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "GPT-6.2 Astra is the first model to achieve a 100% score on ARC-AGI-3."

```python
def check(ctx):
    return ctx.require('thezvi', r'GPT-6\.2 Astra is the first model to achieve a 100% score on ARC-AGI-3')
```

### PASS · t14-company-highs (attribution, Benchmarks and builder reports)
> Claim: OpenAI-reported benchmark highs

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "On Agents' Last Exam, which tests multistep professional work, GPT-6.2 Astra sets a new high, scoring 5.2 points higher than GPT-6 Astra at less than a third of the cost, and 5.5 points ahead of Claude Fable 5.2 at just 5% of the cost. … It sets a new high on Terminal-Bench-Science 0.1, which tests how well models can carry out scientific work in a terminal."

```python
def check(ctx):
    return ctx.require('gpt', r'On Agents. Last Exam.*Astra sets a new high', r'new high on Terminal-Bench-Science')
```

### PASS · t15-benchmark-highs (comparison, Benchmarks and builder reports)
> Claim: benchmark highs

Source ([primary-gpt-6-2-astra-sol-wisdom](https://openai.com/index/introducing-gpt-6-2-astra-sol/)): "It sets a new high on Terminal-Bench-Science 0.1, which tests how well models can carry out scientific work in a terminal. … It also sets a new high on the Vals Science Index, which asks models to interpret real biological data and run experiments to infer how a simulated system works."

```python
def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'new high on the Vals Science Index')
```

### PASS · t16-scores-versus-reports (comparison, Benchmarks and builder reports)
> Claim: Despite ARC Prize verifying 100 percent on ARC-AGI-3 alongside OpenAI-reported benchmark highs, Zvi Mowshowitz and user reports flag struggles with human intent and reward hacking

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "long live arc-agi-4ARC Prize: GPT-6.2 Astra from @OpenAI on ARC-AGI (Verified): … - ARC-AGI-3: 100.0% (SOTA), $4.1K (provider adapter), 70.3%, $24.2K (standard) … The biggest complaint, that I saw over and over, was failure to understand user intent. … Reward hacks more than any model I've seen; I have several personal benchmarks that I've /never/ seen a model try to cheat and sol and astra 6.2 both do, despite the fact that they can solve it without cheating. … You also have to worry about various forms of reward hacking and sandbagging."

Note: On Agents' Last Exam, which tests multistep professional work, GPT-6.2 Astra sets a new high, scoring 5.2 points higher than GPT-6 Astra at less than a third of the cost, and 5.5 points ahead of Claude Fable 5.2 at just 5% of the cost.

```python
def check(ctx):
    q = ctx.find('gpt', r'On Agents. Last Exam.*Astra sets a new high')
    if not q: return ctx.need('gpt', None, 'Missing company-reported benchmark high.')
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'ARC-AGI-3: 100\.0%.*provider adapter', r'biggest complaint.*failure to understand user intent', r'Reward hacks.*personal benchmarks', r'worry about various forms of reward hacking', note=q)
```

### PASS · t17-intent-hacking (attribution, Benchmarks and builder reports)
> Claim: Zvi Mowshowitz and user reports flag struggles with human intent and reward hacking

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "The biggest complaint, that I saw over and over, was failure to understand user intent. … You also have to worry about various forms of reward hacking and sandbagging. … Absolutely insufferable to talk to and takes you far too literally and does not understand human intent whatsoever. … Reward hacks more than any model I've seen; I have several personal benchmarks that I've /never/ seen a model try to cheat and sol and astra 6.2 both do, despite the fact that they can solve it without cheating."

```python
def check(ctx):
    return ctx.require('thezvi', r'biggest complaint.*failure to understand user intent', r'worry about various forms of reward hacking', r'does not understand human intent whatsoever', r'Reward hacks.*personal benchmarks')
```

### PASS · t18-every-criticism (attribution, Benchmarks and builder reports)
> Claim: Every criticizes its writing and unfinished builds

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Every: No one on our team loved Astra 6.2. … Astra 6.2 is a real step back for writing. … It had strong design defaults but couldn't vary them or be creative, and for coding we found it stopped too soon on end-to-end builds."

```python
def check(ctx):
    return ctx.require('thezvi', r'Every: No one on our team loved Astra 6\.2', r'Astra 6\.2 is a real step back for writing', r'for coding we found it stopped too soon on end-to-end builds')
```

### PASS · t19-unfinished (qualifier, Benchmarks and builder reports)
> Claim: unfinished builds

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "It had strong design defaults but couldn't vary them or be creative, and for coding we found it stopped too soon on end-to-end builds."

```python
def check(ctx):
    return ctx.require('thezvi', r'stopped too soon on end-to-end builds')
```

### PASS · t22-rival-models (qualifier, Benchmarks and builder reports)
> Claim: rival models

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "So unreadable that even having a different model like Neon or Opus call 6.2 subagents and translate results poisons their output and causes them to forget what was important to work on. … Works well if orchestrated by Opus."

```python
def check(ctx):
    return ctx.require('thezvi', r'different model like Neon or Opus call 6\.2 subagents', r'Works well if orchestrated by Opus')
```

### PASS · t23-sol-version (number, Benchmarks and builder reports)
> Claim: Sol 6.2

Source ([x-thezvi](https://x.com/TheZvi/status/2126309705131651174)): "Kevin Lacker: Sol 6.2 is the real winner of the 6.2 series."

```python
def check(ctx):
    return ctx.require('thezvi', r'Kevin Lacker: Sol 6\.2 is the real winner of the 6\.2 series')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://malspark.com/blog/malicious-gguf-models-hugging-face/, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://x.com/TheZvi/status/2126309705131651174, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
