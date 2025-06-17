Here is the project plan


--------One-Pager “Cheat-Sheet” — every part in plain, do-this order-------------
Save the taxonomy file (10 min)

Copy the JSON below into audience_taxonomy_v2025-06.json. DONE

Add the extra codes you approved (X_HORIZ, X_SME, X_ENTERPRISE, F_HR, F_IT, F_FIN, F_MKTG, X_MULTIPLATFORM, X_REGULATED, UNKNOWN, OTHER). DONE / NEEDS CHECKING

Commit the file to Git.
(Tip — keep one comment line per code explaining when to choose it.)

Re-label the 70 partner rows (30 min)

Open your partners CSV.

For each partner’s “target-audience” text, assign one or more codes from the new file.
Quick hack: build a regex map (e.g. r"\bnursing" → HC_LTC), run it, then hand-fix the few wrong ones.

Save as partners_with_codes.csv.

Create the LLM classifier helper (20 min)

Paste the 25-line classify_blurb() sketch into classifier.py.

Insert the new taxonomy file path.

In build_prompt():

include the full code list,

add three tiny examples (one for X_HORIZ, one for F_HR, one for X_SME),

keep temperature=0, ask for JSON {primary, secondary[], explain}.

Smoke-test the classifier (10 min)

Feed five well-known horizontals (Slack, Dropbox, DocuSign, etc.).

Feed five niche vertical tools (e.g. hospice-EHR).

Confirm the codes look right; adjust prompt if not.

Enrich new prospect rows (variable)

For each prospect URL, scrape or paste a 3-sentence “what we do” blurb.

Run classify_blurb() → store the returned codes in a column audience_codes.

Implement the matching-score function (30 min)

Copy the calculate_match_score() skeleton you drafted.

Define SPECIAL = {...} once at the top (all X_* and F_* codes).

Plug in partner’s “boss score” and “avg leads” boosts if you have them.

Run first full match (15 min)

Load partners_with_codes.csv and the enriched prospects sheet.

Loop through every prospect ↔ partner pair; compute score, overlap_type.

Dump the top-5 partner matches per prospect to a new CSV (matches_v1.csv).

Log and inspect UNKNOWN / OTHER (5 min)

Append any rows where primary == "UNKNOWN" or "OTHER" to unknown_log_2025-06.csv.

Glance at explanations—good reality check.

Tuning loop (1–2 hrs once)

Sort matches_v1.csv by score; eyeball 20 high scores and 20 low scores.

If horizontals dominate, lower their base weight; if vertical misses occur, raise vertical weight.

Rerun until results “feel” right.

Weekly maintenance (15 min weekly)

Classify new prospects → cache does the heavy lifting.

Review unknown_log_*.csv; if you see ≥ 3 of the same undiscovered audience, add a new code, rename file to audience_taxonomy_v2025-08.json, bump TAXO_VERSION, and rerun only the UNKNOWN rows.

Ready-to-paste minimal taxonomy add-ons
{
  "X_HORIZ": "Cross-Industry ► Horizontal Business Software",
  "X_SME": "Cross-Industry ► Targets Small & Medium Enterprises",
  "X_ENTERPRISE": "Cross-Industry ► Targets Large Enterprises",
  "F_HR": "Functional Focus ► HR Departments",
  "F_IT": "Functional Focus ► IT Departments",
  "F_FIN": "Functional Focus ► Finance/Accounting Departments",
  "F_MKTG": "Functional Focus ► Marketing Departments",
  "X_MULTIPLATFORM": "Cross-Industry ► Multi-Sided Platform/Marketplace",
  "X_REGULATED": "Cross-Industry ► Serves Highly Regulated Sectors",
  "UNKNOWN": "Audience ► Unknown / Too little info",
  "OTHER": "Audience ► Other (manual explanation required)"
}
Follow the 10 steps above in order—you’ll have a working, auditable prototype in a single afternoon.

--------END OF One-Pager “Cheat-Sheet” — every part in plain, do-this order-------------


------Over arching plan-----
**Verdict in one line:**
Our outlined plan is a solid “v 1.0+” roadmap—just tighten a few details before we freeze the taxonomy and start coding.

---

## 1  Taxonomy tweaks before you save `audience_taxonomy_v2025-06.json`

| What to add / change                                                                | Why it matters                                                                                | Quick fix                                                                                        |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Give every new bucket a short code.**                                             | Keeps the JSON small and the matching logic fast.                                             | `X_HORIZ`, `X_SME`, `F_HR`, `X_MULTIPLATFORM`, `X_REGULATED`, `UNKNOWN`, `OTHER`, etc.           |
| **Add a one-line “when to use” note (comment) next to each new code – for humans.** | Future-you will forget edge-case rules in six months.                                         | In the JSON file or a README.                                                                    |
| **Decide on *one* multi-sided strategy for v 1.**                                   | Either generic `X_MULTIPLATFORM` **or** two explicit sides—doing both will confuse the model. | For speed, go with generic `X_MULTIPLATFORM` now; revisit after you have data.                   |
| **List the “regulated verticals” once, centrally.**                                 | Your scoring logic needs to know which codes count as “regulated.”                            | e.g. `REGULATED_SET = {"FIN_*", "HC_*", "PUB_*"}` in code; keep it near taxonomy for easy edits. |

---

## 2  LLM prompt – three practical pointers

1. **Closed list + concise rule bullets.**
   Put the entire code list first, then a short “rules” block such as:
   *`If product works for any industry → X_HORIZ.`*
   *`If it serves a department across all verticals → pick one F_* code.`*

2. **Few-shot examples for new specials.**
   Add one example each for `X_HORIZ`, `F_HR`, and `X_SME`. That alone will cut mis-labelling by >50 %.

3. **Temperature = 0, `max_tokens` small, and require valid JSON.**
   Keeps output deterministic and cache-friendly.

---

## 3  Matching / scoring logic – sanity checks

* **Weight order** you drafted (vertical > functional > size > horizontal > regulated > multi-sided) is sensible.
* **Tune weights empirically:** start with the illustrative values you wrote, run on 10–20 pairs, then adjust until the top-5 matches *feel* right.
* **Store `overlap_type`** exactly as you suggested—it’s a life-saver when debugging why score = 0.6 instead of 1.0.

---

## 4  Workflow checklist before “go live”

1. **Update taxonomy file** with the new codes + comments.
2. **Re-tag the 70 partners** using only those codes (you can bulk-edit with regex, then manual spot-check).
3. **Upgrade `classify_blurb()`** – swap in the new prompt and keep the same caching logic.
4. **Implement the new `calculate_match_score()`** (copy-paste skeleton, replace your regulated-set placeholder).
5. **Dry-run on five horizontal SaaS and five niche vendors** to confirm codes, `overlap_type`, and final scores look sane.
6. **Log `UNKNOWN` and `OTHER` rows** to CSV; set a recurring reminder to review weekly.

---

## 5  Common pitfalls (avoid early pain)

| Pitfall                                       | Preventive measure                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| Model returns “raw text” instead of code.     | Explicitly state: *“Return only codes shown above”* and show JSON schema.      |
| Explosion of “OTHER”.                         | Add two-shot examples of *correct* use of `OTHER` (rare, with explanation).    |
| Horizontal code swamping everything.          | Lower its base weight (0.3–0.5) and let vertical or functional beats override. |
| Mismatched camel-case / underscores in codes. | Validate with `assert primary in TAXONOMY` inside `classify_blurb()`.          |

---

## 6  Green light?

If we action the tweaks above, our plan covers:

* deterministic labelling (closed list + cache)
* all realistic edge cases (horizontal, size, functional, regulated, multi-sided)
* weighted matching that favours the most relevant overlaps
* a feedback loop to grow the taxonomy (“UNKNOWN/OTHER” log)

This is a rock-solid prototype scope we can build and test in a couple of days. Once we have real scores coming out, tuning becomes a data exercise instead of guesswork.

**We’re good to proceed—ship v 1, then iterate.**


------End of Over arching plan-----