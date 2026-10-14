# Delete Slides Creator Squad

**Task ID:** `delete-slides-creator`
**Pattern:** `SC-TP-001`

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Delete Slides Creator Squad |
| **status** | `pending` |
| **responsible_executor** | @squad-chief |
| **execution_type** | `Human` |
| **input** | Explicit delete request with approval |
| **output** | Removal plan or approved deletion |
| **action_items** | 4 steps |
| **acceptance_criteria** | 3 criteria |

## Action Items

1. Confirm explicit deletion intent.
2. Inventory artifacts under `squads/slides-creator/`, docs, and runtime state.
3. Check dependencies on `ds` or downstream decks.
4. Remove only after approval.

## Acceptance Criteria

- [ ] Deletion was explicitly requested
- [ ] Dependent artifacts were inventoried
- [ ] Removal plan is clear before execution
