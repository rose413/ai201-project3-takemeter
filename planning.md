# Takemeter - planning.md

> Complete this document before collecting data or training your classifier.
> Update this document if your labels, annotation process, or evaluation strategy changes.

---

# Community Selection

## Community

**Chosen community:** r/truezelda

<!-- Name the subreddit, forum, Discord channel, support community, review site, etc. -->

**Why I chose this community:**

<!-- Explain why this community interests you and why its content is suitable for classification. -->
This community interests me because I am a huge Legend of Zelda fan and am highly interested in hearing people's thoughts, arguments, and opinions on the different games. The discussions here are often lengthy and thoughtful, making it an ideal source for text data.

**Why this is a good classification task:**

<!-- Explain what makes the discourse diverse enough to support multiple labels.
     Discuss variation in post types, user goals, topics, tone, or intent. -->
It is a great classification task because the discourse naturally splits between two distinct styles of communication: subjective personal opinions and structured arguments rooted in game lore or design principles.

# Label Definitions

## Label 1: Opinion

**Definition:**

<!-- Write a complete sentence defining this label. -->
An opinion is a subjective claim stated by a user that reflects a personal preference, feeling, or belief without providing factual evidence or structured reasoning to back it up.

**Example Post 1:**

> [It would be cool if, somehow, visiting Ganon's Castle as an adult you happen upon the remnants of this courtyard. I don't know how that would work as it seems like the entire castle was demolished and rebuilt in its entirety]

**Example Post 2:**

> [I really hope that chasm below the castle is massive. It should feel like the castle truly is "in the distance" and something you look at with awe rather than it being like 100ft away.]

---

## Label 2: Argument

**Definition:**

<!-- Write a complete sentence defining this label. -->
An argument is a claim supported by evidence (such as quotes, game mechanics, or lore), an interpretation or reasoning of that evidence, and a logical conclusion.

**Example Post 1:**

> [From what we see, the Silent Princesses both grow out in nature and can also be created where the Light Dragon's tears freshly touch the earth. You can find Silent Princesses in areas away from the Tear sites, all over, so they must also grow naturally. The dragon could be responsible for their existence, then they reproduce naturally after that?

Zelda's time travel is a closed loop, so this wouldn't be a "paradox", just a neat coincidence. Ganondorf knows Link and Zelda's names before she even time travels, so it can only be a closed loop since the result is visible before the cause and her travel just fulfills that loop. ]

**Example Post 2:**

> [Deliberate fixed camera angles - I actually feel like OoT makes a lot of great artistic/directional choices with how and when its fixed shots are implemented. It doesn’t inhibit the gameplay in places where it already exists (maybe aside from inside houses?) and I don’t see why it shouldn’t return. The multi-shot sequence approaching the Temple of Time is a perfect example. Combined with complete quiet, there’s a special emphasis on the scale of the architecture, symbolizing the weight of the remaining journey looming over you, dwarfing Link. It makes you feel physically and narratively small in a way that I feel can’t be equally conveyed with a traditional camera following Link. It often serves to curate the player's experience and emphasize an intended mood.]

---

# Hard Edge Cases

## Ambiguous Cases

**What types of posts may fit multiple labels?**

<!-- Describe genuine boundary cases between labels. -->
Boundary cases often occur when a user states an opinion but backs it up with very weak, emotional reasoning, or when a user frames a detailed lore argument around a purely subjective premise.

### Edge Case 1
Does those opinions substract from your overall enjoyment of TotK or something? Do you need everyone to love the game or somehow the game isn't as fun? In that case, no one could enjoy Zelda II because it is one of the weaker entries lol


**Possible labels:**

* Opinion
* Argument

**Why it is ambiguous:**
<!-- Explain. -->
It contains rhetorical questions and uses logical connectors like "because," but the reasoning relies on assumptions about other players' feelings rather than concrete game evidence.

**Annotation rule:**
<!-- State exactly how you will label these cases. -->
If the post relies purely on rhetorical questions and lacks external evidence (game facts, lore, quotes), it will be labeled as an Opinion.

### Edge Case 2
Bro just because some people call out the shortcomings of newer Zelda games doesn’t mean they’re not good games. Nor should someone else’s opinion have any direct bearing on your own, unless they’re introducing you to valid information which further informs your own.

Totk is great, but there are certainly flaws. Botw, being similar, suffers some of the same flaws.



**Possible labels:**

* Opinion
* Argument

**Why it is ambiguous:**

<!-- Explain. -->
The user is trying to make a logical point about how opinions work, but they do not provide specific examples of the "flaws" in TotK or BotW to back up their final claim.

**Annotation rule:**

<!-- State exactly how you will label these cases. -->
If the claim mentions evidence exists (e.g., "there are certainly flaws") but fails to actually provide or explain that evidence, it will be labeled as an Opinion.

### General Tie-Breaking Rules

1. The "Because" Test: Does the user attempt to answer why they hold their stance using game mechanics, lore, or development history? If yes, Argument.  

2. The Subjectivity Check: If the entire post can be summarized as "I liked this" or "I hated this," regardless of length, it is an Opinion.

3. Benefit of the Doubt: If a post sits perfectly on the fence and contains at least one piece of verifiable game evidence attached to a claim, default to Argument.

---

# Data Collection Plan

## Data Sources

**Where will examples come from?**

<!-- List subreddit(s), forums, websites, archives, etc. -->
Reddit posts and comments from r/truezelda.

## Target Dataset Size

| Label              | Target Count |
| ------------------ | ------------ |
| Label 1            | 100          |
| Label 2            | 100          |
| Total              | 200          |

## Collection Process

1. Navigate to the r/truezelda subreddit.
2. Extract comments and manually review them for label fit.
3. Record the text and assigned label in a CSV file.
4. Repeat until 200 balanced items are collected.

## Handling Class Imbalance

**What if a label is underrepresented after 200 examples?**

<!-- Explain your strategy. Possible approaches:
     - Collect more examples from specific sources
     - Expand search keywords
     - Continue sampling until minimum count reached
     - Merge labels only if conceptually justified -->
If one label (e.g., Arguments) is underrepresented, I will specifically target threads tagged as "Theory" or "Lore" to find more evidence-based posts. If Opinions are lacking, I will target threads discussing "Favorite games" or "Hot takes." I will continue sampling until the 100/100 split is reached.

---

# Annotation Guidelines

## Annotation Process

**Who will annotate the data?**

<!-- Yourself, team members, etc. -->
I will manually annotate the data.

**How will labels be assigned?**

<!-- Explain the decision process. -->
Labels will be assigned based strictly on the presence or absence of evidence-backed reasoning, referencing the definitions and tie-breaking rules above.

## Consistency Rules

1. Ignore the length of the post; a long post can still be a pure Opinion, and a short post can be a concise Argument.
2. Ignore toxicity or tone; an aggressive Argument is still an Argument.
3. Evaluate the primary intent of the post if it contains a mix of both (e.g., if it starts with an opinion but spends 3 paragraphs proving it with lore, label it as an Argument).

## Difficult Examples Log

<!-- Keep a running list of posts that were difficult to classify and note how you resolved them. -->

| Example | Labels Considered | Final Label | Reason |
| ------- | ----------------- | ----------- | ------ |
| You put a backslash in front of it, that tells reddit to ignore your tag code. | Argument vs. Opinion | Opinion | The 'Because' Test: Explains how Reddit markdown mechanics work as evidence. |
| yeah we bought the Nintendo Power Official Strategy Guide instead. great book | Argument vs. Opinion | Argument | The Subjectivity Check: Personal anecdote and preference. |
| Yeah hopefully not, I haven't played the 3DS and doubt I ever will. LA was my first ever Z… | Argument vs. Opinion | Argument | The Subjectivity Check: Summarizes personal gaming history and hopes without structured argument. |
| Overall I really like this theory. A few details like the length of the 3 day cycle being … | Argument vs. Opinion | Argument | The Subjectivity Check: Evaluates the theory subjectively without adding independent lore or mechanics. |
| It's the best game of all time so yes | Opinion | Opinion | The Subjectivity Check: Purely a statement of personal belief. |
| Hopefully they don't bastardize it like the 3DS remake | Opinion | Opinion | The Subjectivity Check: A subjective feeling about the previous remake. |
| Oh i heard that I just hope the time loop resetting isn't that bad as people told me | Opinion | Opinion | The Subjectivity Check: Expresses a personal hope/feeling about a mechanic. |
| When I played it as a kid I needed a guide just for one section. It's definitely worth pla… | Opinion | Opinion | The Subjectivity Check: Personal anecdote with no game evidence attached. |
| Is better than Tears of the kingdom... Is the best Zelda of all the franchise. It's worth … | Opinion | Opinion | The Subjectivity Check: Purely a statement of personal preference. |
| It is a pretty great game but damn is it hard without any help. I also played it as my sec… | Opinion | Opinion | The Subjectivity Check: Describes personal difficulty without explaining why with mechanics. |
| Very unique experience that complements OOT, they're Zelda's Yin and Yang. Playing them wa… | Opinion | Opinion | The Subjectivity Check: States personal feelings about the experience. |
| It's worth playing if you like feeling lost in a dream, and you enjoy waiting, repeating, … | Opinion | Opinion | The Subjectivity Check: Summarizes the vibe subjectively. |
| Beating the main story without a guide is easy. 100% is a pain. I would never be able to. | Opinion | Opinion | The Subjectivity Check: States personal capability and feelings. |
| Considering it's one of the best pieces of art in the history of our planet, yes. | Opinion | Opinion | The Subjectivity Check: Pure hyperbole and subjective claim. |
| I think OOT will be incredible, the LA remake was flawless imo. If OOT is anything less th… | Opinion | Opinion | The Subjectivity Check: Mostly expressions of hope and personal feelings about the remake. |
| It truly is, where do you sit with the obvious upcoming remake that will undoubtedly follo… | Opinion | Opinion | The Subjectivity Check: Expresses excitement and personal feelings without providing evidence. |
| if majoras mask is worth playing and going in without a guide at all. yes and yes 10 year … | Argument | Argument | The 'Because' Test: Uses historical player base and lack of internet as reasoning. |
| The game contains its own guide | Argument | Argument | Benefit of the Doubt: Refers to an in-game mechanic (the Bomber's Notebook/Tatl). |
| I'm not yet convinced that they'll do it. Depends really on what OOT will be like. If they… | Argument | Argument | The 'Because' Test: Uses development themes (western vs eastern reading) and art style transitions as reasoning. |
| It's an added challenge, sure, but just like any hard game the rewards feel greater. Still… | Argument | Argument | The 'Because' Test: Uses the comparison to Ocarina and the historical context of beating it as kids to justify the stance on difficulty. |
| It's a gameplay mechanic. Just like any other game, it will become second nature and not a… | Argument | Argument | The 'Because' Test: Explains why it isn't bad by breaking down how the gameplay mechanic becomes second nature. |
| I found the time loop really engaging. The part I had a harder time with was some of the c… | Argument | Argument | The 'Because' Test: Cites N64 controls and the strategic layer of time resets to back up the claim. |
| The game gives you tools to make it work. Do not start a dungeon on the second or third da… | Argument | Argument | The 'Because' Test: Directly uses the day cycle game mechanic as evidence. |
| It's not 'modern day friendly' where it makes everything a convenience. But the system is … | Argument | Argument | The 'Because' Test: Mentions restarting days and specific thematic narrative elements (loss and hope) as evidence. |
| Even then, messing up is relative. There's always something achievable in every cycle. Gri… | Argument | Argument | The 'Because' Test: Uses specific gameplay elements (bank, bomber's notebook, NPC schedules) to prove the point. |
| If you have NSO on switch it has save states which makes it less daunting | Argument | Argument | Benefit of the Doubt: Uses the NSO save state feature as verifiable evidence. |
| Just use the reverse song of time and it is never an issue like ever. | Argument | Argument | The 'Because' Test: Specifically cites the reverse song of time mechanic. |
| The time limit doesn't necessarily make it harder, it just changes how you approach the ga… | Argument | Argument | The 'Because' Test: Provides an extensive breakdown of the 3-day cycle, items, and progression mechanics. |
| It's a great game, but you should go into it with the right headspace: There is a time lim… | Argument | Argument | The 'Because' Test: Cites ocarina songs, stray faeries, and the mailman quest to support the advice. |
| Yes. It's definitely denser than OoT. During your first set of quests, you'll come across … | Argument | Argument | The 'Because' Test: Mentions the scarecrow and time manipulation songs as mechanical evidence. |
| did you like the mask quests in oot? do you want like 40 of them with all kinds of differe… | Argument | Argument | Benefit of the Doubt: Mentions the specific number of mask quests as a verifiable feature. |
| You're asking a community of Zelda fans if you should play a Zelda game. They'll only tell… | Argument | Argument | The 'Because' Test: Uses the lore connection to Ocarina of Time as the reasoning for why it's fine to play blind. |
| You can play it without a guide, that's what Tatl is for. She's your guiding companion. | Argument | Argument | Benefit of the Doubt: Cites Tatl as the in-game companion/mechanic. |
| People who love this game are telling you it's amazing and the best game ever. As a big Ze… | Argument | Argument | The 'Because' Test: Backs up their stance by citing the slow down time song, the swamp area, and the quest reset mechanics. |
| I can agree with the Jöhatsu, I was doing research on three days in Japan and came across … | Argument | Argument | Benefit of the Doubt: Refers to real-world historical research as evidence to back up their stance on the theory. |
| No, because we literally don't have any point of reference as any of the games happen... C… | Argument | Argument | The 'Because' Test: Uses 'Creating a Champion' lore book as evidence to answer why. |
---

# Evaluation Metrics

## Primary Metrics

### Accuracy

**Why it matters:**

<!-- Explain. -->
Accuracy is important to show a general overview of the model's quality. It helps answer the simple question of how many total predictions the model got correct out of the whole dataset.

### Precision

**Why it matters:**
<!-- Explain why false positives matter for this task. -->
Precision measures how many of the items that the model stated as positive were actually correct. In this context, if the model labels a post as an Argument, precision tells us how likely it is to truly contain evidence and reasoning.

### Recall

**Why it matters:**
<!-- Explain why false negatives matter for this task. -->
Recall measures how many of the actual positive cases were correctly identified by the model. This is critical to ensure the model isn't missing well-structured arguments and accidentally throwing them into the Opinion bucket.

### F1 Score

**Why it matters:**
<!-- Explain why balancing precision and recall is important. -->
The F1 Score acts as a balance between precision and recall. It is essential because a model could easily achieve high accuracy just by guessing the majority class. F1 ensures the classifier performs well across both Opinions and Arguments.

## Additional Evaluation

### Confusion Matrix

**Why it matters:**

<!-- Explain how it helps identify commonly confused labels. -->
It helps evaluate the performance of the classification model by comparing its predictions against the actual ground truth. It will specifically reveal if the model is heavily biased toward misclassifying Opinions as Arguments, or vice versa.

### Per-Class Performance

**Why it matters:**

<!-- Explain why average accuracy alone is insufficient. -->
It evaluates how well the model predicts each specific label. Average accuracy is insufficient since the model might be 95% accurate at identifying Opinions but only 40% accurate at identifying Arguments.

---

# Definition of Success

## Minimum Acceptable Performance

**Accuracy Target:**

<!-- Example: 80%+ -->
80% or higher.

**F1 Target:**

<!-- Example: Macro F1 ≥ 0.75 -->
Macro F1 score >= 0.75.

**Lowest Acceptable Recall for Any Label:**
<!-- Example: No label below 0.65 recall -->
No label below 0.70 recall.

## What Would Make This Useful?
<!-- Describe what level of performance would make the classifier genuinely useful to a real user or moderator. -->
If the classifier maintains an 80% accuracy rate, F1 score that is greater than or equal to 0.75, and a recall of at least 0.70, it would be highly useful for community moderators wanting to automatically tag posts as "Argument" versus "Opinion" to help users filter content.

## What Would Be "Good Enough" for Deployment?
<!-- Explain your practical deployment threshold. -->
The model is "good enough" for real-world deployment if it hits the 0.75 Macro F1 score and maintains a recall of at least 0.70 for the "Argument" class, ensuring high-effort posts aren't accidentally hidden or miscategorized.
---

# AI Tool Plan

This project focuses on dataset design, annotation, and evaluation rather than code generation. AI tools will be used to improve label quality and evaluation rigor.

## 1. Label Stress-Testing

**AI Tool:**

<!-- ChatGPT, Claude, Gemini, etc. -->
Claude

**Inputs I will provide:**

* Label definitions
* Edge case descriptions
* Annotation rules

**Prompt goal:**
Ask the AI to generate 5–10 posts that intentionally sit between two labels.

**How I will use the results:**

* Attempt to classify each generated post.
* If classification is difficult or inconsistent, revise label definitions.
* Update annotation rules before collecting the full dataset.

**Success criteria:**
<!-- Example: Every stress-test example can be classified confidently using written rules. -->
Every stress-test example generated by the AI can be confidently classified using only the written rules provided in this document.

---

## 2. Annotation Assistance

**Will I use AI to pre-label examples?**
Yes
<!-- Yes or No -->

### If Yes

**AI Tool:**
Claude
<!-- Tool name -->

**Process:**

1. AI generates an initial label.
2. I manually review every example.
3. I correct any incorrect labels.
4. Final labels remain human-approved.

**Tracking Method:**
<!-- Explain how you'll record which examples were AI-assisted. -->
I will include a dedicated metadata column in my final dataset (ai_pre_labeled) containing a boolean value (TRUE) for every row generated by the AI, so I have a clear record of which examples received AI assistance prior to my human review.

**Disclosure Plan:**

<!-- Explain how you'll report AI-assisted annotation in your project writeup. -->
In the methodology section of my final project write-up, I will include a clear sub-section dedicated to data annotation. I will explicitly disclose that Claude was used to generate initial draft labels to accelerate the process. I will provide the prompt used to guide the AI, state the exact percentage of the dataset that utilized this method, and detail the rigorous manual review process (steps 2-4 above) used to guarantee that all final labels are human-verified and accurate.

---

## 3. Failure Analysis

**AI Tool:**
<!-- ChatGPT, Claude, etc. -->
Claude

**Inputs I will provide:**

* Model predictions
* Ground-truth labels
* Misclassified examples
* Confusion matrix

**Questions I will ask:**

* Which labels are most commonly confused?
* Are there recurring linguistic patterns?
* Are certain keywords causing mistakes?
* Are annotation rules contributing to errors?

**Verification Plan:**

<!-- Explain how you'll verify any patterns suggested by the AI rather than accepting them automatically. -->
I will not blindly accept the AI's analysis. I will take the specific keywords or patterns the AI suggests (e.g., "The model struggles with posts containing question marks") and manually cross-reference them against my dataset to confirm if that pattern actually exists before writing my final evaluation report.

---

# Final Review Checklist

Before training:

* [X] Community selected and justified
* [X] Labels clearly defined
* [X] Two examples included for every label
* [X] Edge cases documented
* [X] Annotation rules established
* [X] Data collection plan complete
* [X] Target counts specified
* [X] Evaluation metrics justified
* [X] Success criteria defined
* [X] AI tool plan completed

Before submission:

* [X] Dataset collected
* [X] Labels reviewed for consistency
* [X] Model evaluated
* [X] Failure analysis completed
* [X] Results compared to success criteria
* [X] AI usage documented

🎯 Baseline accuracy: 0.667  (evaluated on 30/30 parseable responses)

Per-class metrics (baseline):
              precision    recall  f1-score   support

     Opinion       0.62      0.87      0.72        15
    Argument       0.78      0.47      0.58        15

    accuracy                           0.67        30
   macro avg       0.70      0.67      0.65        30
weighted avg       0.70      0.67      0.65        30

Running inference on test set...

🎯 Fine-tuned model accuracy: 0.833

Per-class metrics (fine-tuned model):
              precision    recall  f1-score   support

     Opinion       0.86      0.80      0.83        15
    Argument       0.81      0.87      0.84        15

    accuracy                           0.83        30
   macro avg       0.83      0.83      0.83        30
weighted avg       0.83      0.83      0.83        30
