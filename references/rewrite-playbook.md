# Rewrite playbook

Removing tells is only half the job. A design that merely avoids slop can still be bland. This file gives positive direction: how to make the replacement *specific* to the product.

## Start with the structure

The biggest wins come from changing the shape of the page, not swapping colors. Before touching CSS, answer: **what is the one thing this screen should make someone understand or do?**

Then pick a structure that fits that answer:

- **One claim + proof.** A large headline, a real artifact (screenshot, diagram, code sample), one primary action. Best for products with a single sharp idea.
- **Asymmetric split.** A short narrative column beside a substantial visual. Best when the visual carries information the copy cannot.
- **Sequential walkthrough.** Three to five numbered steps *when the product actually has a sequence*. Each step gets a concrete outcome, not an icon.
- **Comparison.** Two columns with real differences and a clear recommendation. Best for "why us vs. the old way".
- **Catalog with hierarchy.** A featured item at a different scale, then supporting items. Best when there really are many equal things.

Avoid the default of equal columns of equal cards. Symmetry at every level is the structural signature of generated layouts.

## Typography that signals intent

- Use two families at most: one workhorse for text, one distinctive face for display. Justify the display face in one sentence — if you can't, change it.
- Set a clear type scale with a real jump between levels. If h1, h2, and h3 are only slightly different sizes, hierarchy is decorative rather than functional.
- Prefer a slightly tighter line-height on display text and generous line-height on body text. That contrast does more than a new font.
- Use weight and spacing for emphasis before resorting to italics or color.
- Let numerals be a designed part of the system — tabular figures for data, a distinct treatment for stats you can actually source.

## Copy that carries information

A reliable test: **could this sentence appear on any other product with a find-and-replace?** If yes, rewrite it.

| Instead of | Write |
|---|---|
| "A seamless, intuitive experience" | The exact interaction: "Press ⌘K to jump to any file." |
| "Built for real work" | A real workflow: "Imports your existing CSV without a schema." |
| "10x faster" | The benchmark and its conditions: "2.1s on 10k rows, M2 Pro, local run." |
| "Quiet by design" | The behavior: "No notifications unless you're mentioned." |
| "Powerful features for teams" | One feature with one outcome: "Shared drafts with per-file history." |
| "Ship from the shell." | A full claim with a consequence: "Ship from the terminal without opening a dashboard." |

Vary sentence length. Keep a short line only where the brevity is itself the point.

## Color and surface

- Start with one neutral and one accent, then add a third only if it has a job (error, success, focus).
- Decide whether the product is a *reading surface* or a *tool surface*. Reading surfaces can afford warmth and lower contrast in decorative areas; tools need high contrast and predictable density.
- Use surface changes to mean something: raised = interactive, inset = contained, plain = content. If everything is raised, nothing is.
- A gradient should have an edge or a direction that organizes the layout. A soft radial fog behind a headline organizes nothing.

## Motion

- Motion explains state: opened, closed, pending, done, changed. If it does not explain state, question it.
- Keep micro-interactions under 200ms and tie them to the user's action, not to scroll position.
- Respect `prefers-reduced-motion`.
- A pulsing indicator must be bound to real live data. Static "live" badges are the visual equivalent of a made-up stat.

## A worked before/after

**Before (score ~25/100):**

```html
<section class="bg-[#FAF6EF] py-24 text-center">
  <span class="rounded-full bg-violet-100 px-3 py-1 text-xs">NEW</span>
  <h2 class="font-[Instrument_Serif] text-5xl">
    A quieter way to <em>work</em>.
  </h2>
  <div class="mx-auto mt-12 grid max-w-4xl grid-cols-3 gap-6">
    <!-- three icon cards, identical structure -->
  </div>
  <p class="mt-12">10x faster. Real results. →</p>
</section>
```

**After (score ~95/100):**

```html
<section class="grid gap-12 py-24 md:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
  <div>
    <h2 class="text-4xl font-semibold tracking-tight">
      Every draft in one place, with the history attached.
    </h2>
    <p class="mt-6 text-lg text-neutral-600">
      Reviewers comment on the exact paragraph they mean. Changes are
      attributable, and you can restore any earlier version per file.
    </p>
    <a class="mt-8 inline-block border-b-2 border-current pb-1 font-medium"
       href="/docs">See a review in progress</a>
  </div>
  <figure class="min-h-80 border border-neutral-200 bg-neutral-50 p-6">
    <!-- a real artifact: annotated screenshot of the product -->
  </figure>
</section>
```

What changed and why: the cream wash, pill, italic word, icon trio, and unverifiable stats are gone; the layout is asymmetric because the artifact carries information; the copy describes verifiable behavior; the link is a text link because the label already says what happens; the "card" is a figure containing a real artifact, which is a legitimate use of a container.

## When the user wants the aesthetic anyway

Some briefs genuinely call for the look — a parody, a period piece, a deliberate "generated" concept. In that case, note that the tells are intentional, skip the rewrite, and score the work against the *user's* intent instead of the default one. The skill is a taste check, not a style police.
