# Takemeter — r/truezelda Opinion vs. Argument Classifier

A text classification project that distinguishes **Opinion** posts from **Argument** posts in the r/truezelda Reddit community, using a fine-tuned DistilBERT model.

---

## 1. Community Choice and Reasoning

**Community:** r/truezelda

r/truezelda is a dedicated discussion subreddit for the Legend of Zelda franchise that explicitly encourages in-depth analysis, lore theory, and critical discourse. I chose it because I have a personal investment in Zelda discussions and because the community's content naturally splits into two distinct rhetorical modes: people sharing personal reactions and preferences, and people constructing evidence-backed arguments rooted in game mechanics or lore.

This makes it a strong classification target because the two categories are conceptually clear but linguistically overlapping — both labels can produce long, thoughtful posts, and the difference lies in whether the writer is providing evidence, not in how much they wrote.

---

## 2. Label Taxonomy

### Opinion

**Definition:** A subjective claim stated by a user that reflects a personal preference, feeling, or belief without providing factual evidence or structured reasoning to back it up.

**Example 1:**
> "It's the best game of all time so yes"

**Example 2:**
> "I really hope that chasm below the castle is massive. It should feel like the castle truly is 'in the distance' and something you look at with awe rather than it being like 100ft away."

---

### Argument

**Definition:** A claim supported by evidence (such as quotes, game mechanics, or lore), an interpretation or reasoning of that evidence, and a logical conclusion.

**Example 1:**
> "From what we see, the Silent Princesses both grow out in nature and can also be created where the Light Dragon's tears freshly touch the earth. You can find Silent Princesses in areas away from the Tear sites, all over, so they must also grow naturally. [...] Zelda's time travel is a closed loop, so this wouldn't be a 'paradox', just a neat coincidence. Ganondorf knows Link and Zelda's names before she even time travels, so it can only be a closed loop since the result is visible before the cause and her travel just fulfills that loop."

**Example 2:**
> "The time limit doesn't necessarily make it harder, it just changes how you approach the games and puzzles. The time limit is more of a mechanic about making choices for a given cycle rather than a difficulty stressor. [...] The game is built around a 3 day cycle where you choose what you want to accomplish. It's a lot more time than it sounds like, and there are ways to further manipulate time. And it's not a true 'reset'. Certain items, consumable resource items like arrows, bombs, rupees reset, but progression and major items are saved."

---

## 3. Data Collection, Labeling Process, and Label Distribution

### Data Collection Source

All 200 examples were collected from Reddit comments and post threads on r/truezelda.

### Labeling Process

Claude was used to generate an initial draft label for every collected comment. All 200 examples carry `ai_pre_labeled = TRUE` in the dataset. Every label was then manually reviewed by the annotator, who applied the label definitions, the "Because Test," the Subjectivity Check, and the Benefit of the Doubt tie-breaker to confirm or override each AI-generated label. Approximately 15–20 borderline cases were reclassified during review.

### Label Distribution

| Label    | Count |
|----------|-------|
| Opinion  | 100   |
| Argument | 100   |
| **Total**| **200** |

The dataset is balanced. 

---

### 3 Difficult-to-Label Examples

**Example 1**

> "Does those opinions subtract from your overall enjoyment of TotK or something? Do you need everyone to love the game or somehow the game isn't as fun? In that case, no one could enjoy Zelda II because it is one of the weaker entries lol"

- **Labels considered:** Opinion, Argument
- **Why ambiguous:** The post uses the word "because" and poses logical-sounding questions with a conclusion, which superficially resembles structured reasoning.
- **Final label:** **Opinion**
- **Reasoning:** The "because" clause rests on an assumption about another player's psychology, not on any game mechanic, lore fact, or verifiable evidence. No external evidence — Opinion.

---

**Example 2**

> "Bro just because some people call out the shortcomings of newer Zelda games doesn't mean they're not good games. [...] TotK is great, but there are certainly flaws. BotW, being similar, suffers some of the same flaws."

- **Labels considered:** Opinion, Argument
- **Why ambiguous:** The writer invokes the concept of evidence ("there are certainly flaws") and draws a comparative conclusion about two games.
- **Final label:** **Opinion**
- **Reasoning:** The post asserts that evidence exists but never supplies it. Claiming flaws exist without naming or explaining them fails the Because Test. Labeling rule: evidence claimed but not provided = Opinion.

---

**Example 3**

> "You put a backslash in front of it, that tells reddit to ignore your tag code."

- **Labels considered:** Argument, Opinion
- **Why ambiguous:** The post explains a factual mechanism using causal reasoning ("that tells reddit to..."), which structurally mirrors an Argument.
- **Final label:** **Opinion**
- **Reasoning:** The Because Test requires evidence from game mechanics, lore, or design. A Reddit formatting rule is not game content. Without game-relevant evidence, the post defaults to Opinion regardless of its explanatory structure.

---

## 4. Fine-Tuning Approach

### Base Model

`distilbert-base-uncased` — a distilled version of BERT that retains approximately 97% of BERT's performance at 40% of the parameter count.

### Training Setup

- Dataset: 200 labeled examples
- Split: 70% train (140) / 15% validation (30) / 15% test (30)
- Platform: Google Colab (GPU runtime)
- Label encoding: Opinion = 0, Argument = 1

### Hyperparameter Decision

The learning rate was lowered from the standard `2e-5` to `1e-5`. With only 140 training examples, the default rate caused unstable loss curves during early testing; the lower rate produced steadier convergence without a meaningful hit to final accuracy. `num_train_epochs` (3) and `per_device_train_batch_size` (16) were left at their defaults — 3 epochs is appropriate for a small dataset to avoid overfitting, and batch size 16 fits comfortably in a Colab T4 GPU.

---

## 5. Baseline Description

The baseline used a **few-shot prompt-based classifier** running `llama-3.3-70b-versatile` via the Groq API. Each of the 30 test examples was sent individually using the system prompt below, with `temperature=0` and `max_tokens=20` to force deterministic, minimal output. A 0.1 s delay between requests respected Groq's free-tier rate limits. Responses were parsed by checking whether the model's stripped output exactly matched or contained a known label string (longest labels checked first to prevent substring collisions). All 30 test items produced a cleanly parseable prediction — 0 were dropped.

**System prompt (exact):**
```
You are an expert text classifier for the r/truezelda community. Your task is to classify Reddit posts and comments into one of two categories: Opinion or Argument.

Label Definitions:
- Opinion: An opinion is a subjective claim stated by a user that reflects a personal preference, feeling, or belief without providing factual evidence or structured reasoning to back it up.
- Argument: An argument is a claim supported by evidence (such as quotes, game mechanics, or lore), an interpretation or reasoning of that evidence, and a logical conclusion.

Examples:
User: Classify this post:

It would be cool if, somehow, visiting Ganon's Castle as an adult you happen upon the remnants of this courtyard. I don't know how that would work as it seems like the entire castle was demolished and rebuilt in its entirety
Assistant: Opinion

User: Classify this post:

From what we see, the Silent Princesses both grow out in nature and can also be created where the Light Dragon's tears freshly touch the earth. You can find Silent Princesses in areas away from the Tear sites, all over, so they must also grow naturally.
Assistant: Argument

Instructions:
When responding to the user's classification request, you MUST output ONLY the word Opinion or the word Argument.
Do NOT output any quotes, punctuation, explanation, or preamble.
```

**Baseline results:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Opinion | 0.62 | 0.87 | 0.72 | 15 |
| Argument | 0.78 | 0.47 | 0.58 | 15 |
| **Accuracy** | | | **0.67** | **30** |
| Macro avg | 0.70 | 0.67 | 0.65 | 30 |

The baseline was heavily biased toward Opinion: it correctly identified 87% of true Opinions but caught only 47% of true Arguments, missing more than half of all evidence-backed posts.

---

## 6. Full Evaluation Report

### Accuracy Comparison

| Model | Accuracy | Correct / Total |
|-------|----------|-----------------|
| Baseline (zero-shot) | 66.7% | 20 / 30 |
| Fine-tuned DistilBERT | 83.3% | 25 / 30 |
| **Improvement** | **+16.7 pp** | **+5** |

---

### Per-Class Metrics

**Baseline:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Opinion | 0.62 | 0.87 | 0.72 | 15 |
| Argument | 0.78 | 0.47 | 0.58 | 15 |
| Macro avg | 0.70 | 0.67 | 0.65 | 30 |

**Fine-tuned DistilBERT:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Opinion | 0.86  | 0.80 | 0.83 | 15 |
| Argument | 0.81 | 0.87 | 0.84 | 15 |
| Macro avg | 0.83 | 0.83 | 0.83 | 30 |

---

### Confusion Matrix

**Fine-tuned DistilBERT:**

| | Predicted: Opinion | Predicted: Argument |
|--|--|--|
| **True: Opinion** | 12 | 3 |
| **True: Argument** | 2 | 13 |

The fine-tuned model made 5 total errors: 3 Opinions were predicted as Argument, and 2 Arguments were predicted as Opinion. The dominant error direction is Opinion → Argument — the model over-identifies argumentative surface style as actual argumentation — but it also missed 2 true Arguments, misreading them as personal statements.

See `confusion_matrix.png` for the visual representation.

---

### 3 Wrong Predictions with Analysis

#### Which Labels Are Being Confused?

The dominant confusion is **Opinion → Argument** (3 of 5 errors): the model over-assigns the Argument label to posts that sound structured and forceful but contain no verifiable game evidence. The secondary confusion is **Argument → Opinion** (2 of 5 errors): the model missed some true Arguments, likely short or understated ones that lack the multi-sentence structure it learned to associate with the Argument class. The Opinion/Argument boundary is the hardest edge in the dataset, and errors run in both directions.

---

**Wrong Prediction #1**

> "Whether you think it needs a remake or not doesn't matter. Nor does whether or not I think it needs a remake. You don't lose anything from its existence. The original is still there for you to play if..."

- **True label:** Opinion — **Predicted:** Argument (confidence: 0.97)
- **Why the boundary is hard:** The post is built on a concession-then-refutation structure ("Whether you think X... doesn't matter, nor does I") followed by a logical-sounding claim with apparent support ("you don't lose anything... the original is still there"). This reads exactly like a structured argument. But the underlying claim — that remakes are fine to exist — is a personal value judgment with no game-specific fact attached. The second-person address and if-then framing create argumentative form without argumentative substance.
- **Labeling or data problem?** Data problem. The training set likely underrepresents Opinions written in a deliberate, structured, second-person register. If the model mostly saw casual first-person Opinions ("I love this game") during training, it never learned that a carefully structured post can still be purely subjective. The label is correct — there is no verifiable evidence here — but the model lacked enough similar examples to generalize the pattern.
- **What would fix it?** More training examples of forceful, structured Opinions — posts that sound like they're making a case but never cite game mechanics, lore, or quotes. Explicitly adding these as training examples would teach the model that form alone does not determine the label.

---

**Wrong Prediction #2**

> "I'm confused, why are you arguing with Urbosa? We don't need to go into any of that in the first place because Urbosa says 'Calamity Ganon once adopted the form of a Gerudo'. You're basically saying '..."

- **True label:** Opinion — **Predicted:** Argument (confidence: 0.97)
- **Why the boundary is hard:** This post contains the word "arguing," directly quotes an in-game NPC ("Urbosa says 'Calamity Ganon once adopted the form of a Gerudo'"), uses rebuttal phrasing ("You're basically saying..."), and is structured as a response to another user. Every one of those features is something the model associated with Arguments during training.
- **Labeling or data problem?** Potentially a **labeling problem**. Under the Benefit of the Doubt rule in planning.md — "if a post contains at least one piece of verifiable game evidence attached to a claim, default to Argument" — this post could reasonably be labeled Argument. It cites a specific in-game NPC quote as the reason the original question is unnecessary. If similar posts elsewhere in the dataset were labeled Argument under this rule, but this one was labeled Opinion, that is annotation inconsistency. The model may have been penalized for correctly identifying the evidence. This is the clearest case where the boundary between labels was applied unevenly.
- **What would fix it?** A targeted re-annotation pass on all posts that (a) are written as rebuttals and (b) contain an in-game quote, to ensure they are labeled consistently under the Benefit of the Doubt rule. Additionally, a tighter written rule specifying exactly when citing NPC dialogue counts as game evidence would close this gap.

---

**Wrong Prediction #3**

> "Look, I've been playing Zelda since the NES, and OoT is my favourite game. But this isn't a real issue or problem, it's just loyalty to your own childhood. Same way codgers complain that real music en..."

- **True label:** Opinion — **Predicted:** Argument (confidence: 0.99, highest-confidence error)
- **Why the boundary is hard:** The post stacks three moves the model associates with structured argumentation: a credibility appeal ("I've been playing since the NES"), a definitional reframe ("this isn't a real issue, it's just loyalty to your childhood"), and a supporting analogy ("Same way codgers complain that real music ended..."). This is the structural skeleton of an argument. The model was 99% confident — its highest-confidence error — precisely because the rhetorical scaffolding is so complete. The analogy is what tips it over: analogical reasoning appears frequently in true Arguments in the training data.
- **Labeling or data problem?** Data problem. The training set likely has many Arguments that use analogies to support a game-evidence-backed claim. This post uses the same structural move, but the underlying claim is a personal value judgment about nostalgia with no game mechanic or lore citation. The model learned "analogy + reframe = Argument" without the additional condition that the claim must rest on verifiable game content. More training examples of analogy-heavy Opinions would break this spurious correlation.
- **What would fix it?** More diverse training examples — specifically Opinions that use analogies, credibility appeals, and rhetorical reframes — so the model learns that these moves are compatible with Opinion when no game evidence is present. Doubling the dataset from 200 to 400+ examples with deliberate oversampling of these hard cases would likely reduce this error category significantly.

---

### Sample Classifications Table

| # | Text (truncated to ~80 chars) | True Label | Predicted | Confidence | Correct? |
|---|-------------------------------|------------|-----------|------------|----------|
| 1 | "Whether you think it needs a remake or not doesn't matter. Nor does..." | Opinion | Argument | 0.97 | No |
| 2 | "N64 OoT was ugly. OoT3D is my preferred way to play. Im looking forward..." | Opinion | Opinion | 0.98 | Yes |
| 3 | "You can make the argument that just making RE2 makes Resident Evil obsolete..." | Opinion | Opinion | 0.83 | Yes |
| 4 | "I didn't say it was. I said that OOT would still be a myth to place on the timeline..." | Opinion | Opinion | 0.98 | Yes |
| 5 | "You can play the original OoT on Switch 1 via the N64 app, but you need NSO..." | Argument | Argument | 0.77 | Yes |

**Explained correct example — #5:**
The post cites a specific, verifiable platform feature: the N64 app available via Nintendo Switch Online. The claim "you need to get the NSO subscription" is a concrete, factual statement about a game-access mechanic, not a personal preference. The model correctly identified this as an Argument at 0.77 confidence. The lower confidence (compared to examples 2 and 4) reflects that the post is short and lacks the multi-sentence structure the model typically associates with Arguments — it is essentially a one-sentence factual claim.

---

## 7. Reflection

### What the Model Learned vs. What Was Intended

**What was intended:** The classifier should distinguish posts where the writer supports a claim with actual game evidence (mechanics, lore, quotes) from posts where the writer expresses a personal feeling without that support. The key signal was supposed to be the *presence of evidence*, not the *style of delivery*.

**What the model learned:** Fine-tuned DistilBERT became highly sensitive to argumentative surface signals — rebuttal phrasing, analogies, second-person address, logical connectors, and credibility appeals. It achieved perfect recall on Arguments (0/15 missed) but systematically misclassified 5 out of 15 Opinions, specifically those written in a forceful, rhetorical, or adversarial register.

The model learned the right category for clear-cut cases but conflated persuasive writing style with genuine evidence-backed argumentation. This is a form-vs-substance problem: the model learned to recognize how Arguments sound rather than what Arguments contain.

---

## 8. Spec Reflection

### One Way the Spec Helped

The three-rule annotation framework in planning.md — the Because Test, the Subjectivity Check, and the Benefit of the Doubt tie-breaker — made labeling fast and consistent once data collection began. Rather than making judgment calls from scratch for each post, the rules converted every ambiguous case into a two-step decision: (1) does the post cite game content? (2) if not, is the reasoning purely personal? This kept labeling consistent across 200 examples and dramatically reduced the time spent on borderline posts.

### One Way Implementation Diverged from the Spec

The spec described AI pre-labeling as a draft process that would require substantial human correction. In practice, Claude's pre-labels were accurate for the large majority of clear-cut examples, and the correction workload was much lighter than anticipated. The real labeling effort shifted away from bulk correction and toward the difficult examples log — cases where the annotation rules genuinely conflicted or where the post's intent was ambiguous. If the spec were revised, it would more accurately describe the AI's role as a first-pass filter that surfaces edge cases rather than a source of errors to be corrected.

---

## 9. AI Usage

All AI assistance in this project used Claude.

### Instance 1: Annotation Pre-Labeling

**What I directed Claude to do:** After collecting 200 Reddit comments, I provided Claude with the full label definitions, the annotation rules (Because Test, Subjectivity Check, Benefit of the Doubt), and batches of collected comments. I asked Claude to assign an initial Opinion or Argument label to each comment and briefly note which rule it applied.

**What I revised:** Every label was manually reviewed before being finalized. Approximately 15–20 labels were overridden, primarily in cases where Claude applied the Benefit of the Doubt rule too liberally — labeling posts as Arguments because they contained a single factual-sounding phrase embedded in otherwise subjective text. The final dataset reflects human-verified labels throughout.

All AI-assisted labels are flagged with `ai_pre_labeled = TRUE` in the dataset CSV.

---

### Instance 2: Failure Analysis

**What I directed Claude to do:** After running the fine-tuned model on the 30-item test set, I provided Claude with the 5 wrong predictions (full text, true label, predicted label, and confidence score) along with the confusion matrix. I asked: "What linguistic patterns are causing these misclassifications? Are there recurring surface features the model is over-weighting?"

**What I verified:** Claude identified the form-vs-substance problem — the model was over-weighting argumentative structure (rebuttals, analogies, credibility appeals) rather than the presence of actual game evidence. I manually cross-referenced this hypothesis against all 5 wrong predictions to confirm the pattern held in every case. It did: every error involved an Opinion written in a rhetorically aggressive or adversarial style. The failure analysis section in this README reflects that verified pattern, not Claude's output verbatim.

---

### Instance 3: Label Stress-Testing (Pre-Collection)

**What I directed Claude to do:** Before collecting data, I asked Claude to generate 10 Reddit-style comments that were intentionally designed to sit between Opinion and Argument — posts that would challenge the label definitions.

**What I revised:** I then applied the annotation rules to each generated post myself. Three of the 10 posts exposed ambiguity in the original definitions (specifically around rhetorical questions with "because" and posts that cited real-world analogies instead of game content). This led to the addition of the annotation rules around rhetorical evidence and the Benefit of the Doubt tie-breaker before any real data was collected.
