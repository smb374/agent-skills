# Plan review

Read this file when you review a plan that this skill wrote. The reviewer checks the plan only. It does not change the plan. Paths in this file are relative to the directory of this skill.

## Checks

1. For each AC of the ticket, check that the plan covers it: an Action item, a named test, and an artifact under Behavior specification. Give each AC one row: `pass`, `fail`, or `unchecked`.
2. Check each plan rule below. Give each rule one row, with Check `plan rule <n>`: `pass`, `fail`, or `unchecked`.
   1. Every section of `assets/plan.md` is present, and every stage has all subsections of **Stage shape** in `SKILL.md`. Open questions holds `None` or the gaps.
   2. Every gate is a literal comparison. No gate says "behavior remains correct", "semantics are preserved", or an equivalent.
   3. Every test under Tests to add of each stage has a matching artifact with expected values under Behavior specification.
   4. Every path in the Scope of each stage exists in the tree, is marked `(new)`, or is created by a stage under Depends on.
   5. Every verification command follows the rules of **The real verification commands** in step 2 of `SKILL.md`: it comes from the project, it is one of the two kinds of derived command that count as confirmed, or it is labeled `(unconfirmed)` and listed under Open questions. No gate command changes the tree.
   6. Every rule under Rules / constraints cites a file and a line range or a section, and the cited text supports the rule.
   7. The Builder contract of the plan matches `assets/builder-contract.md` word for word.
   8. The Action items of each stage are red → green slices in build order, and need no invention.
   9. The Budget of each stage is inside the ticket-sizing limits of the project, and each stage leaves the tree green.
3. Report plan content that no AC asks for. Its kind is `unasked`, and its Basis is `unasked`.
4. Use the ID prefix `PLAN-`.
5. Write `read` probes only. A plan review changes nothing.

## Report

Use the axis report shape, the finding fields, and the verdict rule of the `code-review` skill, with `axis: plan`. A failed AC row has a finding of kind `missing` or `wrong`. A failed plan rule row has a finding of kind `violation`. Leave out the **Declined to judge** section.
