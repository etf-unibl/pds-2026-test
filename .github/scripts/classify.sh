#!/usr/bin/env bash
# Determines the issue checked by the verification workflows and writes the results to $GITHUB_OUTPUT:
#   issue         issue number (first number in the pull request title, or the manual input)
#   kind          test ("good first issue" label), assignment (exactly one "assignment-<n>" label)
#                 or example (issue 0 of a manual run: NAND2 example of the verification environment)
#   topic         assignment topic <n> (graded assignments only)
#   lookup_table  lookup table of the verification repository (PDS_LOOKUP_TABLE or the default
#                 pds_<year>_issues.lookup, <year> = first 20xx in the repository name, else the current year)
#
# Environment: GH_TOKEN, GITHUB_REPOSITORY, GITHUB_EVENT_NAME, GITHUB_OUTPUT, PR_TITLE, INPUT_ISSUE,
#              REPO_NAME, LOOKUP_TABLE (optional)
set -euo pipefail

if [ -z "${LOOKUP_TABLE:-}" ]; then
  YEAR=$(echo "$REPO_NAME" | grep -o -E '20[0-9]{2}' | head -n 1 || true)
  [ -n "$YEAR" ] || YEAR=$(date +%Y)
  LOOKUP_TABLE="pds_${YEAR}_issues.lookup"
fi
echo "lookup_table=$LOOKUP_TABLE" >> "$GITHUB_OUTPUT"

if [ -n "${INPUT_ISSUE:-}" ]; then
  ISSUE="$INPUT_ISSUE"
else
  ISSUE=$(echo "${PR_TITLE:-}" | grep -o -E '[0-9]+' | head -n 1 || true)
fi
if [ -z "$ISSUE" ]; then
  echo "::error::The pull request title must contain the issue number (e.g. 'Issue #55 : ...')."
  exit 1
fi

# Issue 0 is the NAND2 example of the verification environment (manual runs only)
if [ "$ISSUE" = "0" ] && [ "$GITHUB_EVENT_NAME" = "workflow_dispatch" ]; then
  echo "Verification environment example (issue 0), lookup table $LOOKUP_TABLE"
  { echo "issue=0"; echo "kind=example"; echo "topic="; } >> "$GITHUB_OUTPUT"
  exit 0
fi

if ! JSON=$(gh api "repos/$GITHUB_REPOSITORY/issues/$ISSUE"); then
  echo "::error::Issue #$ISSUE does not exist. Check the number in the pull request title."
  exit 1
fi
if [ "$(echo "$JSON" | jq 'has("pull_request")')" = "true" ]; then
  echo "::error::#$ISSUE is a pull request, not an issue. Use the issue number in the pull request title."
  exit 1
fi

LABELS=$(echo "$JSON" | jq -r '.labels[].name')
IS_TEST=$(echo "$LABELS" | grep -c -x 'good first issue' || true)
TOPIC_LABELS=$(echo "$LABELS" | grep -x -E 'assignment-[0-9]+' || true)
N_TOPICS=$(echo -n "$TOPIC_LABELS" | grep -c . || true)
if [ "$IS_TEST" -gt 0 ] && [ "$N_TOPICS" -eq 0 ]; then
  KIND=test
  TOPIC=
elif [ "$N_TOPICS" -eq 1 ] && [ "$IS_TEST" -eq 0 ]; then
  KIND=assignment
  TOPIC=${TOPIC_LABELS#assignment-}
else
  echo "::error::Issue #$ISSUE must have either the 'good first issue' label or exactly one 'assignment-<n>' label (labels: $(echo "$LABELS" | paste -sd ',' -))."
  exit 1
fi
echo "Issue #$ISSUE, type: $KIND${TOPIC:+, assignment topic $TOPIC}, lookup table $LOOKUP_TABLE"
{ echo "issue=$ISSUE"; echo "kind=$KIND"; echo "topic=$TOPIC"; } >> "$GITHUB_OUTPUT"
