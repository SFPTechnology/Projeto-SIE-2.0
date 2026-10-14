# Update Slides Creator Squad

**Task ID:** `update-slides-creator`
**Pattern:** `SC-TP-001`

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Update Slides Creator Squad |
| **status** | `pending` |
| **responsible_executor** | @squad-chief |
| **execution_type** | `Agent` |
| **input** | Change request, PRD delta, app surface change |
| **output** | Updated squad files, CHANGELOG entry, version bump |
| **action_items** | 5 steps |
| **acceptance_criteria** | 4 criteria |

## Action Items

1. Identify affected artifact scope.
2. Apply changes without breaking `ds` delivery contract.
3. Update docs and runtime artifacts if the contract changes.
4. Add CHANGELOG entry and version bump.
5. Re-run validation.

## Acceptance Criteria

- [ ] Updated files are syntactically valid
- [ ] CHANGELOG has a new entry
- [ ] `config.yaml` version reflects the update
- [ ] validation completed
