# Create Lead Magnet Task

## Task Overview

```yaml
task_name: create-lead-magnet
version: 2.0
category: lead_generation
tier_0_required: true
minimum_output: 5 deliverables
estimated_time: 2-4 hours
```

## Purpose

Create high-converting lead magnets (iscas digitais) that transform cold visitors into engaged leads, using research-backed methodologies from Robert Collier, Robert Cialdini, Alex Hormozi, and Dan Kennedy.

A lead magnet is NOT just "free content" - it's a strategic VALUE EXCHANGE that begins the customer relationship and naturally bridges to your paid offer.

---

## TIER 0 DIAGNOSIS (SEMPRE PRIMEIRO)

Before creating ANY lead magnet, diagnose the market situation using Eugene Schwartz's framework.

### Awareness Level Diagnosis

| Level | Description | Lead Magnet Approach |
|-------|-------------|---------------------|
| **Unaware** | Doesn't know they have a problem | Educational content, "Did you know..." |
| **Problem Aware** | Knows problem, not solutions | Problem agitation, solution overview |
| **Solution Aware** | Knows solutions exist | Why YOUR solution is different |
| **Product Aware** | Knows your product | Comparison, case studies |
| **Most Aware** | Ready to buy | Trial, demo, discount |

### Market Sophistication Diagnosis

| Stage | Market State | Lead Magnet Strategy |
|-------|--------------|---------------------|
| **1** | First to market | Simple, direct promise |
| **2** | Second wave | Bigger promise |
| **3** | Mechanism era | Explain HOW it works |
| **4** | Enhanced mechanism | Better/unique mechanism |
| **5** | Saturated | Identity-based, story-driven |

### Diagnostic Questions

```yaml
awareness_diagnosis:
  - Does your audience know they have this problem?
  - Are they actively searching for solutions?
  - Do they know your type of solution exists?
  - Have they heard of you or competitors?
  - What triggered their current search?

sophistication_diagnosis:
  - How many similar lead magnets exist in your market?
  - What promises are competitors making?
  - What mechanisms are they highlighting?
  - How saturated is the conversation?
  - What's the dominant narrative in the market?
```

---

## INPUTS

### Required Information

```yaml
required:
  lead_magnet_type:
    options:
      - ebook
      - checklist
      - cheatsheet
      - template
      - swipe_file
      - video_training
      - webinar
      - quiz
      - calculator
      - challenge
      - free_trial
    guidance: "See Type Selection Matrix below"

  topic:
    description: "Core subject matter"
    example: "Email marketing for SaaS companies"

  target_avatar:
    description: "Specific audience"
    example: "B2B SaaS founders doing $1-10M ARR"

  primary_problem:
    description: "The #1 pain point this solves"
    example: "Low email open rates killing their marketing ROI"

  desired_outcome:
    description: "What success looks like for the user"
    example: "Increase email open rates from 15% to 35%"
```

### Optional Information

```yaml
optional:
  next_offer:
    description: "Paid product lead magnet bridges to"
    purpose: "Ensures alignment and natural progression"

  urgency_element:
    description: "Time-limited component if any"
    examples:
      - "Bonus expires in 48 hours"
      - "Only 100 copies available"

  delivery_method:
    options:
      - email_only
      - thank_you_page
      - both
    default: both

  copywriter_style:
    description: "Preferred copywriter approach"
    options:
      - collier (conversational, entering the dialogue)
      - kennedy (urgent, direct response)
      - hormozi (value-stacking, metrics-focused)
      - schwartz (awareness-matched)
```

---

## TYPE SELECTION MATRIX

### Choosing the Right Format

| If Audience Wants... | Best Format | Conversion Rate |
|---------------------|-------------|-----------------|
| Quick wins | Checklist, Cheatsheet | 27-34% |
| Time savings | Template, Swipe File | 23% |
| Deep learning | Ebook, Video Training | 20-24% |
| Self-discovery | Quiz, Assessment | 22% |
| Proof of concept | Calculator, Tool | 18-20% |
| Hands-on experience | Challenge, Free Trial | 15-18% |

### Format Deep Dives

#### 1. CHEATSHEET (Highest Conversion: 34%)

```yaml
ideal_for:
  - Quick reference needs
  - Complex processes simplified
  - Beginners wanting shortcuts

characteristics:
  length: 1 page (PDF)
  density: High information, minimal explanation
  design: Scannable, visual hierarchy

example_titles:
  - "The [Topic] Cheatsheet"
  - "[Number] [Actions] At a Glance"
  - "The Quick Reference Guide to [Topic]"

when_to_use:
  - Market is action-oriented
  - Audience values efficiency
  - Topic can be distilled to essentials
```

#### 2. CHECKLIST (High Conversion: 27%)

```yaml
ideal_for:
  - Process-based outcomes
  - Quality assurance
  - Step-by-step validation

characteristics:
  length: 1-3 pages
  format: Checkboxes with explanatory text
  structure: Sequential or categorical

example_titles:
  - "The Complete [Topic] Checklist"
  - "[Number] Steps to [Outcome] Checklist"
  - "Before You [Action]: The Essential Checklist"

when_to_use:
  - Audience fears missing steps
  - Process has critical sequence
  - Verification is valuable
```

#### 3. EBOOK/GUIDE (Solid Conversion: 24%)

```yaml
ideal_for:
  - Comprehensive education
  - Authority positioning
  - Complex topic coverage

characteristics:
  length: 10-50 pages
  format: Chapters, visuals, examples
  design: Professional, branded

example_titles:
  - "The Ultimate Guide to [Topic]"
  - "The Definitive [Topic] Handbook"
  - "[Topic] Mastery: From [A] to [B]"

when_to_use:
  - Audience wants deep understanding
  - Topic requires explanation
  - Authority building is priority
```

#### 4. TEMPLATE/SWIPE FILE (Good Conversion: 23%)

```yaml
ideal_for:
  - Time-strapped professionals
  - "Plug and play" needs
  - Proven formula seekers

characteristics:
  length: Varies
  format: Editable documents
  value: Immediate usability

example_titles:
  - "[Number] Proven [Type] Templates"
  - "The [Topic] Swipe File"
  - "Copy-and-Paste [Type] Collection"

when_to_use:
  - Audience values speed
  - Task is repetitive
  - Proven formulas exist
```

#### 5. QUIZ/ASSESSMENT (Engaging: 22%)

```yaml
ideal_for:
  - Self-discovery motivation
  - Lead segmentation
  - Personalized recommendations

characteristics:
  length: 5-15 questions
  format: Interactive (Typeform, Interact)
  outcome: Personalized result + resources

example_titles:
  - "What's Your [Topic] Type?"
  - "Discover Your [Metric] Score"
  - "Which [Category] Are You?"

when_to_use:
  - Personalization adds value
  - Segmentation is needed
  - Audience enjoys self-reflection
```

#### 6. VIDEO TRAINING (Moderate Conversion: 20%)

```yaml
ideal_for:
  - Demonstration-based learning
  - Personality-driven brands
  - Complex visual processes

characteristics:
  length: 10-30 minutes
  format: Screen share, talking head, slides
  delivery: Unlisted YouTube, Wistia, Vimeo

example_titles:
  - "[Topic] Masterclass (Free Training)"
  - "[Number] Minutes to Master [Skill]"
  - "Watch Me [Demonstrate Action]"

when_to_use:
  - Visual demonstration helps
  - Personal connection matters
  - Topic is best shown, not told
```

#### 7. CALCULATOR/TOOL (Utility: 18-20%)

```yaml
ideal_for:
  - Quantitative decisions
  - Custom projections
  - Ongoing utility

characteristics:
  format: Interactive web tool or spreadsheet
  value: Personalized calculations
  stickiness: Users return repeatedly

example_titles:
  - "The [Metric] Calculator"
  - "Calculate Your [Outcome]"
  - "[Topic] ROI Calculator"

when_to_use:
  - Numbers drive decisions
  - Personalization matters
  - Ongoing tool use benefits you
```

---

## THE COLLIER PRINCIPLE: ENTER THE CONVERSATION

### Foundation

Robert Collier's principle (1931):

> "Always enter the conversation already taking place in the customer's mind."

### Application Framework

```yaml
step_1_identify_conversation:
  questions:
    - "What is my prospect thinking about RIGHT NOW?"
    - "What problem is keeping them up at night?"
    - "What language do they use to describe this?"
    - "What have they already tried?"
    - "What do they believe about solutions?"

step_2_match_entry_point:
  techniques:
    - Start with their exact thought
    - Use their vocabulary, not yours
    - Acknowledge their current situation
    - Validate their frustration
    - Position lead magnet as natural next step

step_3_apply_6_motives:
  collier_motives:
    love: "Connection, belonging, relationships"
    gain: "Financial benefit, profit, savings"
    duty: "Obligation, responsibility, ethics"
    pride: "Status, achievement, recognition"
    self_indulgence: "Pleasure, comfort, convenience"
    self_preservation: "Safety, security, health"
```

### Headline Entry Points by Motive

```yaml
love_headlines:
  - "How to [Build/Strengthen] Your [Relationship] with [Group]"
  - "The Secret to [Connecting With/Winning Over] [Audience]"

gain_headlines:
  - "How to [Save/Make] [Specific Amount] on [Topic]"
  - "The [Number]-Step System to [Financial Outcome]"

duty_headlines:
  - "The [Professional's] Guide to [Responsible Action]"
  - "How to [Protect/Serve] [Those You're Responsible For]"

pride_headlines:
  - "Join the [Percentage] Who [Achievement]"
  - "How [Smart/Successful People] Approach [Topic]"

self_indulgence_headlines:
  - "The Lazy Person's Guide to [Result]"
  - "How to [Get Result] Without [Effort/Sacrifice]"

self_preservation_headlines:
  - "How to [Protect/Secure] Your [Asset/Health/Future]"
  - "[Number] Threats to Your [Asset] (And How to Stop Them)"
```

---

## THE CIALDINI FRAMEWORK: TRIGGER RECIPROCITY

### The Psychology of Free

From Robert Cialdini's research (1984):

> "When someone gives us something, we feel an internal obligation to give something back."

### Reciprocity Multipliers

```yaml
reciprocity_factors:
  unexpectedness:
    principle: "Unexpected gifts trigger stronger response"
    application: "Add surprise bonus to lead magnet"

  personalization:
    principle: "Personalized gifts feel more valuable"
    application: "Customize with their name, company, situation"

  significance:
    principle: "Higher perceived value = stronger obligation"
    application: "Stack value, quantify worth"

  timing:
    principle: "Giving first creates obligation"
    application: "Always lead with value, never ask first"
```

### Applying All 7 Principles

| Principle | Lead Magnet Application |
|-----------|------------------------|
| **Reciprocity** | Give genuine value, trigger obligation |
| **Commitment** | Small opt-in leads to bigger actions |
| **Social Proof** | "Join 50,000+ subscribers" |
| **Authority** | Expert credentials, "as seen in" |
| **Liking** | Personable copy, relatable stories |
| **Scarcity** | Limited time/availability |
| **Unity** | "For [specific group] only" |

---

## THE HORMOZI VALUE EQUATION

### The Formula

From Alex Hormozi's $100M Leads (2023):

```
Value = (Dream Outcome × Perceived Likelihood)
        ÷ (Time Delay × Effort Required)
```

### Maximizing Each Variable

```yaml
dream_outcome:
  maximize_by:
    - Be SPECIFIC about the result
    - Use numbers when possible
    - Paint the "after" picture
    - Connect to deeper desires
  examples:
    weak: "Improve your marketing"
    strong: "Generate 100 qualified leads in 30 days"

perceived_likelihood:
  maximize_by:
    - Include proof elements
    - Show case studies
    - Add testimonials
    - Demonstrate track record
  examples:
    weak: "Learn marketing tips"
    strong: "The exact system that generated $2.3M for my clients"

time_delay:
  minimize_by:
    - Promise IMMEDIATE access
    - Highlight quick wins
    - Use "instant," "today," "now"
    - Front-load fastest results
  examples:
    weak: "Download our comprehensive guide"
    strong: "Get instant access + see results in 48 hours"

effort_required:
  minimize_by:
    - Emphasize ease of consumption
    - Use "done-for-you" language
    - Highlight plug-and-play elements
    - Remove perceived complexity
  examples:
    weak: "A detailed training program"
    strong: "Copy-paste templates ready in 5 minutes"
```

### The "Free Content That Sells" Principle

```yaml
what_to_give_free:
  - WHAT: Reveal the problem and its impact
  - WHY: Explain why it matters
  - PARTIAL HOW: Framework overview, first steps

what_to_sell:
  - FULL HOW: Complete implementation
  - DONE-FOR-YOU: Templates, systems, support
  - SPEED: Faster results, shortcuts
```

---

## THE KENNEDY APPROACH: MAGNETIC MARKETING

### Free Report Structure (Dan Kennedy)

```yaml
kennedy_report_structure:
  1_shocking_opening:
    purpose: "Grab attention immediately"
    technique: "Contrarian statement, surprising fact"
    example: "Everything you've been told about [topic] is wrong."

  2_problem_agitation:
    purpose: "Intensify the pain"
    technique: "Describe consequences of inaction"
    example: "Every day you wait, you're losing [specific amount]"

  3_hidden_truth_revelation:
    purpose: "Position as insider"
    technique: "Reveal what 'they' don't want you to know"
    example: "The [industry] doesn't want you to know this..."

  4_partial_solution:
    purpose: "Deliver genuine value"
    technique: "Give actionable framework"
    example: "Here's the 5-step process I use..."

  5_bridge_to_offer:
    purpose: "Create desire for more"
    technique: "Natural transition to paid offer"
    example: "For full implementation, see..."

  6_clear_cta:
    purpose: "Drive next action"
    technique: "Specific, time-sensitive instruction"
    example: "Book your call before [date]..."
```

### Kennedy's 10 Rules Applied to Lead Magnets

| Rule | Application |
|------|-------------|
| Always have an offer | Lead magnet IS the offer |
| Reason to respond NOW | Limited time, scarcity |
| Clear instructions | Exact steps to download |
| Tracking | Unique landing page |
| Only no-cost brand building | Track ROI of lead magnet |
| Follow-up | Email sequence ready |
| Strong copy | Headlines, bullets, CTA |
| Direct response design | Function over beauty |
| Results rule | Test and optimize |
| Disciplined approach | No exceptions to rules |

---

## LANDING PAGE COPY FRAMEWORK

### Above-the-Fold Structure

```markdown
┌─────────────────────────────────────────┐
│                                         │
│  [PRE-HEADLINE] Free Download           │
│                                         │
│  [HEADLINE]                             │
│  The Ultimate [Result] in [Time]        │
│  Without [Common Pain]                  │
│                                         │
│  [SUBHEADLINE]                          │
│  Discover the [X] [things] that         │
│  [transformed/helped] [social proof]    │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │             │  │ [Form]           │  │
│  │  [MOCKUP]   │  │ Name: __________ │  │
│  │             │  │ Email: _________ │  │
│  │             │  │ [GET INSTANT     │  │
│  │             │  │  ACCESS →]       │  │
│  └─────────────┘  │                  │  │
│                   │ "No spam ever.   │  │
│                   │  Unsubscribe     │  │
│                   │  anytime."       │  │
│                   └──────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### Below-the-Fold Elements (Optional)

```markdown
## What You'll Learn/Get

- ✅ [Benefit 1 with specific outcome]
- ✅ [Benefit 2 with specific outcome]
- ✅ [Benefit 3 with specific outcome]
- ✅ [Bonus element if applicable]

## Perfect For You If...

- [Specific situation/role description]
- [Pain point they're experiencing]
- [Goal they're trying to achieve]

## About [Author/Company]

[Mini bio - 2-3 sentences establishing credibility]

[Photo or logo]

## [Social Proof Section]

"[Testimonial quote about lead magnet quality]"
- Name, Title/Company

[Optional: Number counter - "Downloaded by 10,000+ people"]
```

### Headline Formulas

#### Formula 1: Result + Timeframe + Without Pain

```
"How to [Achieve Result] in [Timeframe] Without [Pain]"

Examples:
- "How to Double Your Email List in 30 Days Without Paid Ads"
- "How to Close 5 More Deals Per Month Without Cold Calling"
```

#### Formula 2: Number + Specific Things + Outcome

```
"[Number] [Things] to [Achieve Specific Outcome]"

Examples:
- "7 Email Templates That Book 3x More Calls"
- "15 Headline Formulas That Convert Like Crazy"
```

#### Formula 3: The Exact + Thing + Social Proof

```
"The Exact [Thing] I Used to [Achieve Result]"

Examples:
- "The Exact Script I Used to Close $500K in Sales"
- "The Exact Checklist That Grew My List to 50,000"
```

#### Formula 4: Question + Desirable Outcome

```
"Want to [Achieve Desirable Outcome]?"

Examples:
- "Want to Finally Crack the Code on Facebook Ads?"
- "Ready to Build Your First 6-Figure Funnel?"
```

#### Formula 5: For + Specific Audience + Result

```
"The [Type] for [Specific Audience] Who Want [Result]"

Examples:
- "The Pricing Guide for Coaches Who Want Premium Clients"
- "The Ad Library for E-commerce Brands Scaling to $1M"
```

### CTA Button Copy

#### High-Converting Examples

```yaml
instant_access:
  - "Get Instant Access"
  - "Download Now (Free)"
  - "Get My Free Copy"
  - "Yes! Send It To Me"

ownership:
  - "Claim Your [Lead Magnet]"
  - "Get Your [Lead Magnet]"
  - "Grab Your Free Copy"

action_oriented:
  - "Start [Achieving Result]"
  - "Begin My [Journey]"
  - "Unlock the [Lead Magnet]"
```

#### Low-Converting (Avoid)

```yaml
generic_avoid:
  - "Submit" (too formal)
  - "Sign Up" (sounds like commitment)
  - "Subscribe" (newsletter connotation)
  - "Download" (too generic)
  - "Click Here" (meaningless)
```

### Trust Elements

```yaml
near_form_trust:
  privacy_assurance:
    - "No spam, ever. Unsubscribe anytime."
    - "100% free. No credit card required."
    - "We respect your privacy."

  social_proof:
    - "Join [X,000]+ others"
    - "Downloaded by [X] people this week"
    - "★★★★★ Rated by [X] readers"

  authority_badges:
    - "As seen in [Publications]"
    - "[Certification] Approved"
    - "[X] years of expertise"
```

---

## NAMING YOUR LEAD MAGNET

### The Naming Formula

```
[Benefit Descriptor] + [Format Word] + [For Audience]
```

### Power Words by Category

```yaml
results_focused:
  - Ultimate
  - Complete
  - Definitive
  - Proven
  - Tested
  - Guaranteed

exclusivity:
  - Secret
  - Hidden
  - Insider
  - Little-Known
  - Underground
  - Private

speed_ease:
  - Quick
  - Fast
  - Simple
  - Easy
  - Effortless
  - Instant

specificity:
  - Exact
  - Step-by-Step
  - Word-for-Word
  - Blueprint
  - Framework
  - System
```

### Name Examples by Type

```yaml
cheatsheet_names:
  - "The Ultimate [Topic] Cheatsheet"
  - "[Topic] At a Glance"
  - "The Quick Reference [Topic] Guide"

checklist_names:
  - "The [Number]-Point [Topic] Checklist"
  - "Before You [Action]: The Essential Checklist"
  - "The Complete [Outcome] Checklist"

ebook_names:
  - "The Definitive Guide to [Topic]"
  - "[Topic] Mastery: From [A] to [B]"
  - "The [Audience] Handbook for [Topic]"

template_names:
  - "[Number] Proven [Type] Templates"
  - "The [Topic] Template Library"
  - "Copy-and-Paste [Type] Collection"

swipe_file_names:
  - "The [Number] [Type] Swipe File"
  - "[Expert]'s Secret [Type] Vault"
  - "Steal My [Type] Collection"
```

---

## THANK YOU PAGE STRATEGY

### Structure Options

#### Option 1: Tripwire Offer

```markdown
┌─────────────────────────────────────────┐
│                                         │
│  🎉 Success! Your [Lead Magnet]         │
│     is on the way!                      │
│                                         │
│  Check your email at [email].           │
│  (Check spam if not in inbox)           │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  ⚡ WAIT! Special One-Time Offer        │
│                                         │
│  [Tripwire Product Name]                │
│  Only $[7-47] (normally $[higher])      │
│                                         │
│  [What it includes]                     │
│  - Benefit 1                            │
│  - Benefit 2                            │
│  - Benefit 3                            │
│                                         │
│  [Buy Now - $XX]                        │
│                                         │
│  ⏰ Offer expires in [countdown]        │
│                                         │
│  [No thanks, just take me to my         │
│   free download]                        │
│                                         │
└─────────────────────────────────────────┘
```

#### Option 2: Video Welcome

```markdown
┌─────────────────────────────────────────┐
│                                         │
│  🎉 Welcome! You're In.                 │
│                                         │
│  Your [Lead Magnet] is on the way.      │
│                                         │
│  While you wait, watch this quick       │
│  welcome video:                         │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │                                 │    │
│  │     [VIDEO PLAYER]              │    │
│  │     (2-3 minutes)               │    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
│                                         │
│  In this video, I share:                │
│  - How to get the most from [LM]        │
│  - A quick tip you can use today        │
│  - What to expect from me next          │
│                                         │
└─────────────────────────────────────────┘
```

#### Option 3: Survey/Segmentation

```markdown
┌─────────────────────────────────────────┐
│                                         │
│  🎉 Almost there!                       │
│                                         │
│  One quick question so I can            │
│  personalize your experience:           │
│                                         │
│  What's your biggest challenge          │
│  with [topic] right now?                │
│                                         │
│  ○ [Option A]                           │
│  ○ [Option B]                           │
│  ○ [Option C]                           │
│  ○ [Option D - Other]                   │
│                                         │
│  [Submit & Get Your Download]           │
│                                         │
└─────────────────────────────────────────┘
```

---

## EMAIL DELIVERY SEQUENCE

### Email 1: Delivery (Immediate)

```markdown
Subject: Your [Lead Magnet Name] is here! 🎁

Hi [First Name],

Promised is promised - here's your [Lead Magnet Name]:

👉 [DOWNLOAD BUTTON/LINK]

Quick tip: [One actionable insight from the lead magnet that
they can implement immediately]

Over the next few days, I'll share:
- [Teaser for Email 2]
- [Teaser for Email 3]
- [Teaser for Email 4]

Any questions? Just hit reply.

[Your Name]

P.S. [Soft tease about what's coming next - creates open loop]
```

### Email 2: Check-In (24-48 hours)

```markdown
Subject: Did you get a chance to look at [Lead Magnet]?

Hey [First Name],

Just checking in - did you download your [Lead Magnet]?

If not, here's the link again:

👉 [DOWNLOAD LINK]

One thing I want to highlight: [Specific section/page that's
especially valuable with brief explanation of why]

I've seen people [achieve specific result] just by implementing
[that section].

Tomorrow I'll share [teaser for next email].

[Your Name]

P.S. [Question to drive reply - "What's your biggest challenge
with [topic]?"]
```

### Email 3: Success Story (48-72 hours)

```markdown
Subject: [Name] used this to [achieve result]

[First Name],

Quick story for you...

[Name] downloaded [Lead Magnet] [timeframe] ago.

At the time, [describe their "before" state - relatable problem].

But then [what they did with the lead magnet].

The result? [Specific outcome with numbers if possible].

The part that made the biggest difference? [Specific element
from the lead magnet].

If you haven't dug into [Lead Magnet] yet, I really encourage
you to start with [specific section].

[Your Name]

P.S. Want results like [Name]? [Soft mention of paid offer or
next step]
```

### Email 4: Bridge to Offer (72-96 hours)

```markdown
Subject: The next step after [Lead Magnet]

[First Name],

By now you've had a chance to go through [Lead Magnet].

Here's what I've noticed about people who get the best results:

They take action on [key insight from lead magnet], BUT they
also [what the paid offer provides].

[Lead Magnet] gives you the [what/why].

But [Paid Offer] gives you:
- [Benefit 1 - the HOW]
- [Benefit 2 - done-for-you element]
- [Benefit 3 - speed/support]

If you're serious about [achieving outcome], [Paid Offer] is
the logical next step.

[CTA - Learn more / Book a call / Get started]

[Your Name]
```

---

## QUALITY CHECKLIST

### Strategic Alignment

```yaml
lead_magnet_strategy:
  - [ ] Addresses PRIMARY pain point of target avatar
  - [ ] Topic naturally leads to main paid offer
  - [ ] Attracts QUALIFIED leads (not just freebie-seekers)
  - [ ] Provides genuine standalone value
  - [ ] Differentiates from competitor lead magnets
  - [ ] Fits audience's awareness level
```

### Value Perception

```yaml
perceived_value:
  - [ ] Title promises specific, desirable outcome
  - [ ] Format matches audience preference
  - [ ] Design is professional (not amateur)
  - [ ] Content is actionable, not just theoretical
  - [ ] Includes proof/credibility elements
  - [ ] Has proprietary naming or framework
```

### Landing Page Elements

```yaml
landing_page:
  - [ ] Headline is benefit-focused and specific
  - [ ] Subheadline qualifies or expands promise
  - [ ] Mockup/visual of lead magnet present
  - [ ] Form asks for MINIMAL information
  - [ ] CTA button uses action language
  - [ ] Trust elements near form
  - [ ] Mobile responsive
```

### Technical Excellence

```yaml
technical:
  - [ ] Page loads in <3 seconds
  - [ ] Form submission works
  - [ ] Download link works
  - [ ] Email delivery is immediate
  - [ ] Tracking/analytics in place
  - [ ] Thank you page redirect works
```

### Post-Conversion

```yaml
post_conversion:
  - [ ] Thank you page has clear next step
  - [ ] Delivery email sends immediately
  - [ ] Follow-up sequence is scheduled
  - [ ] Lead is tagged/segmented in CRM
  - [ ] Tripwire or next offer is ready
```

---

## OUTPUT DELIVERABLES

### Standard Package

```yaml
deliverables:
  1_landing_page_copy:
    includes:
      - Headline (+ 3 A/B test variations)
      - Subheadline
      - Bullet points (5-7)
      - CTA button copy
      - Trust/micro-copy
      - Below-the-fold copy (if needed)

  2_lead_magnet_content:
    includes:
      - Title (+ 2 variations)
      - Table of contents (if applicable)
      - Core content structure
      - Call-to-action at end

  3_thank_you_page_copy:
    includes:
      - Confirmation message
      - Next step instructions
      - Tripwire offer OR video/survey

  4_email_sequence:
    includes:
      - Email 1: Delivery (immediate)
      - Email 2: Check-in (24-48 hours)
      - Email 3: Success story (48-72 hours)
      - Email 4: Bridge to offer (72-96 hours)

  5_supporting_assets:
    includes:
      - Mockup/visual direction notes
      - Facebook/Google ad copy variations
      - Social media promotion posts
```

---

## VALIDATION CRITERIA

### Before Launch

```yaml
must_pass:
  - Landing page conversion rate target: 25%+ for cold traffic
  - Mobile load time: <3 seconds
  - Email deliverability test: passes
  - Download link: verified working
  - Form submission: tested on multiple devices

should_have:
  - A/B test plan for headlines
  - Tracking UTMs configured
  - CRM tagging set up
  - Follow-up sequence loaded
```

### After Launch (30 Days)

```yaml
success_metrics:
  - Landing page conversion rate: 20-40%
  - Email open rate (delivery): 50%+
  - Email click rate (delivery): 15%+
  - Tripwire conversion (if applicable): 5-15%
  - Lead to qualified opportunity rate: tracking
```

---

## COMMON MISTAKES TO AVOID

### Strategic Mistakes

```yaml
avoid:
  too_broad:
    mistake: "Marketing Guide"
    fix: "The 7-Step Email Marketing Playbook for SaaS Founders"

  no_bridge:
    mistake: "Lead magnet has no connection to paid offer"
    fix: "Design lead magnet as 'Chapter 1' of your course"

  wrong_audience:
    mistake: "Attracts freebie-seekers, not buyers"
    fix: "Be specific about WHO it's for in title and copy"

  giving_everything:
    mistake: "Nothing left to sell"
    fix: "Give WHAT and WHY, sell the HOW"
```

### Copy Mistakes

```yaml
avoid:
  generic_headlines:
    mistake: "Download Our Free Guide"
    fix: "The Exact 5-Step System I Used to [Result]"

  weak_cta:
    mistake: "Submit"
    fix: "Get Instant Access Now"

  no_urgency:
    mistake: "Download anytime"
    fix: "Bonus chapter available for 48 hours only"

  missing_proof:
    mistake: "Learn marketing tips"
    fix: "The system used by 500+ agencies"
```

### Technical Mistakes

```yaml
avoid:
  friction:
    mistake: "Asking for name, email, phone, company, role"
    fix: "Email only (name optional)"

  slow_delivery:
    mistake: "Manual email sending"
    fix: "Automated immediate delivery"

  broken_links:
    mistake: "Download link expires or breaks"
    fix: "Test links weekly, use permanent URLs"
```

---

## REAL EXAMPLES ANALYZED

### Example 1: High-Converting Checklist

**Title:** "The 12-Point Sales Page Checklist (Used by 7-Figure Copywriters)"

**Why it works:**
- Specific number (12 points)
- Clear format (checklist)
- Authority proof (7-figure copywriters)
- Implies completeness (nothing missed)

**Conversion rate:** 32%

### Example 2: High-Value Template Pack

**Title:** "Steal My $10K Email Templates (The Exact Emails That Generated $2.3M)"

**Why it works:**
- "Steal" creates exclusivity
- Dollar value ($10K) quantifies worth
- Proof ($2.3M) builds credibility
- "Exact" promises specificity

**Conversion rate:** 28%

### Example 3: Compelling Quiz

**Title:** "What's Your Entrepreneurial Archetype? (3-Minute Quiz)"

**Why it works:**
- Self-discovery appeal
- Time commitment clear (3 minutes)
- Personalized result promised
- Segmentation enabled

**Conversion rate:** 35%

---

*Task Version: 2.0*
*Research Source: lead-magnet-methodology-research.md*
*Lines: 650+*

---

# ═══════════════════════════════════════════════════════════════════════════
# HORMOZI FRAMEWORK - EXTRAÍDO DOS ARTIFACTS MMOS
# Data: 2026-01-23 | Enrichment Phase ENR-004
# Fonte: outputs/minds/alex_hormozi/artifacts/
# ═══════════════════════════════════════════════════════════════════════════

## Hormozi Lead Generation Framework

> **Fonte:** `03_OFFER_CREATION_SYSTEM.md`, `02_VALUE_EQUATION_ENGINE.md`

### Princípio da "Multidão Faminta" Aplicado a Lead Magnets

O mesmo princípio que governa ofertas pagas governa lead magnets:

> "Um professor de marketing perguntou aos alunos qual a única vantagem ao abrir uma barraca de cachorro-quente. A resposta correta foi **'uma multidão faminta'**."
> [Fonte: 03_OFFER_CREATION_SYSTEM.md, Seção 2.1]

**Aplicação para Lead Magnets:**
- Não crie lead magnets para "educar o mercado"
- Encontre a "multidão faminta" já buscando solução
- Seu lead magnet deve canalizar demanda existente, não criar demanda

### 4 Indicadores de Lead Magnet Vencedor

Adapte os indicadores de mercado para lead magnets:

| Indicador | Aplicação em Lead Magnet |
|-----------|-------------------------|
| **Dor Massiva** | O tópico aborda problema URGENTE que o avatar quer resolver AGORA |
| **Poder de Compra** | O avatar tem recursos para comprar a oferta paga subsequente |
| **Fácil de Atingir** | Você consegue distribuir o lead magnet onde o avatar está |
| **Crescendo** | O interesse no tópico está aumentando (trend positivo) |

[Fonte: 03_OFFER_CREATION_SYSTEM.md, Seção 2.2]

### Value Equation Aplicada a Lead Magnets

A mesma equação que maximiza valor de ofertas pagas maximiza conversão de lead magnets:

```
Valor do Lead Magnet = (Dream Outcome × Perceived Likelihood)
                       ÷ (Time Delay × Effort Required)
```

#### 1. Dream Outcome do Lead Magnet

**Não é:** O que você quer ensinar
**É:** A transformação que o avatar experimentará

| Lead Magnet Fraco | Lead Magnet Forte |
|-------------------|-------------------|
| "Guia de Marketing Digital" | "Como Conseguir Seus Primeiros 10 Clientes em 7 Dias" |
| "Checklist de Copywriting" | "O Checklist que Dobrou a Conversão de 147 Landing Pages" |
| "Templates de Email" | "7 Emails que Geraram $2.3M em Vendas (Copy-Paste)" |

[Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 3.1]

#### 2. Probabilidade Percebida de Conquista

**Tática Principal:** Mostre PROVA de que funciona

Elementos para adicionar ao lead magnet:
- Número de downloads/usuários ("Baixado por 50,000+ pessoas")
- Resultados específicos ("Usado para gerar $X em vendas")
- Depoimentos de quem usou
- Seu próprio resultado com o método

> "As pessoas pagam por **certeza**. Uma promessa ousada sem prova gera ceticismo."
> [Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 3.2]

#### 3. Time Delay (Minimizar)

**Princípio:** "Rápido Supera Grátis"

| Abordagem Lenta | Abordagem Rápida |
|-----------------|------------------|
| "Guia Completo de 50 Páginas" | "O Checklist de 1 Página que Você Pode Usar Hoje" |
| "Curso de 10 Módulos" | "A Aula de 12 Minutos que Muda Tudo" |
| "Ebook Definitivo" | "O Template que Você Configura em 5 Minutos" |

**Engenharia de "Vitórias Rápidas":**
> "Pessoas que experimentam uma vitória emocional cedo são cientificamente mais propensas a se comprometerem com o processo a longo prazo."
> [Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 3.3]

**Aplicação:** Seu lead magnet deve entregar uma "vitória" nas primeiras 24-48 horas de uso.

#### 4. Effort & Sacrifice (Minimizar)

**Espectro de Entrega para Lead Magnets:**

| DIY (Menor Valor) | DWY (Médio Valor) | DFY (Maior Valor) |
|-------------------|-------------------|-------------------|
| Ebook para ler | Checklist para seguir | Template pronto para usar |
| Vídeo para assistir | Quiz com recomendação | Swipe file para copiar |
| Artigo para estudar | Calculator para preencher | Script para executar |

> "Os clientes compram conveniência. Quanto menos esforço exigido, mais valiosa é a oferta."
> [Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 3.4]

[Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 3]

### Empilhamento de Valor em Lead Magnets

**REGRA:** "Uma oferta dividida em componentes vale mais que apresentada como um todo"

**Aplicação em Landing Page de Lead Magnet:**

```
❌ ERRADO:
"Baixe nosso Guia de Marketing"

✅ CERTO:
"O que você vai receber:
✓ O Guia Completo de 27 Páginas (valor $47)
✓ 5 Templates de Email Prontos para Usar (valor $97)
✓ Checklist de Implementação em 1 Página (valor $27)
✓ BÔNUS: Vídeo de 12 Min com Walk-Through (valor $47)

VALOR TOTAL: $218 → GRÁTIS"
```

[Fonte: 02_VALUE_EQUATION_ENGINE.md, Seção 6]

### Matriz de Lead Magnet por Awareness Level

Combine Hormozi com Schwartz para máxima eficácia:

| Awareness Level | Melhor Tipo de Lead Magnet | Exemplo |
|-----------------|---------------------------|---------|
| **Unaware** | Quiz/Assessment que revela problema | "Descubra se Você Está Cometendo Estes 5 Erros" |
| **Problem Aware** | Checklist/Guia que mostra solução | "O Caminho Completo de [Problema] a [Solução]" |
| **Solution Aware** | Case Study/Template do seu método | "Como [Cliente] Conseguiu [Resultado] com [Seu Método]" |
| **Product Aware** | Demo/Trial/Amostra grátis | "Experimente [Produto] Grátis por 7 Dias" |
| **Most Aware** | Desconto/Oferta especial | "Oferta Exclusiva: 30% OFF + 3 Bônus" |

[Fonte: 03_OFFER_CREATION_SYSTEM.md + 02_VALUE_EQUATION_ENGINE.md]

### O Continuum Lead Magnet → Oferta Paga

**Princípio:** Lead magnet é a FASE 1 do seu sistema de ofertas.

> "Crie fluxo. Monetize o fluxo. Depois adicione atrito."
> [Fonte: 03_OFFER_CREATION_SYSTEM.md, Seção 3]

**Aplicação:**

| Fase | O que Acontece | Objetivo |
|------|----------------|----------|
| **Lead Magnet** | Entrega valor instantâneo, resolve problema parcial | Criar fluxo de leads qualificados |
| **Tripwire ($7-47)** | Oferta low-ticket que converte lead em cliente | Monetizar fluxo, qualificar compradores |
| **Core Offer** | Sua oferta principal | Receita e transformação real |
| **Upsell/Backend** | Ofertas de maior valor | Maximizar LTV |

### Framework de Conteúdo "WHAT-WHY-HOW"

**O que dar grátis vs. o que vender:**

```yaml
gratuito_lead_magnet:
  WHAT: "O que é o problema e a solução"
  WHY: "Por que isso importa e funciona"
  PARTIAL_HOW: "Framework overview, primeiros passos"

pago_oferta:
  FULL_HOW: "Implementação completa passo a passo"
  DONE_FOR_YOU: "Templates, sistemas, suporte"
  SPEED: "Resultados mais rápidos, atalhos"
```

[Fonte: 03_OFFER_CREATION_SYSTEM.md]

### Checklist Hormozi para Lead Magnets

Antes de publicar, verifique:

- [ ] **Dream Outcome Claro:** O título promete transformação específica?
- [ ] **Prova de Resultado:** Há números, depoimentos ou credenciais?
- [ ] **Vitória Rápida:** O avatar consegue resultado nas primeiras 24-48h?
- [ ] **Esforço Mínimo:** É DFY/DWY ao invés de DIY puro?
- [ ] **Empilhamento de Valor:** Os componentes estão listados e valorados?
- [ ] **Bridge Natural:** O lead magnet leva naturalmente à oferta paga?
- [ ] **Multidão Faminta:** O tópico tem demanda comprovada?

---

*Hormozi Framework Enrichment - ENR-004*
*Fontes: 02_VALUE_EQUATION_ENGINE.md, 03_OFFER_CREATION_SYSTEM.md*
*Data da Extração: 2026-01-23*
