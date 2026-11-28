/**
 * MVE-1 · HITL Proposal Write-Safety & Per-Item CAS Gate
 * -----------------------------------------------------------------------------
 * Standalone in-memory state-transition validation demo (zero external
 * dependencies) illustrating HITL staging and per-item CAS checks.
 *
 * Hard constraints enforced in deterministic code (NOT in prompts):
 *   1. Verbatim Evidence Chain: Every proposed state mutation MUST carry a
 *      verbatim story quote (>= 6 chars) and positive source floor. Any single
 *      invalid item rejects the entire proposal (all-or-nothing atomicity).
 *   2. Physical HITL Separation: `proposeChanges()` writes only to a pending
 *      staging queue and NEVER touches committed state. `applyProposal()` is
 *      NEVER exposed as an LLM tool — it requires an explicit human confirmation
 *      `quote` (>= 2 chars) supplied by UI action.
 *   3. Per-Item Old-Value CAS Re-Verification: Between proposal creation and
 *      human approval, live state may advance. Before committing, every item's
 *      current value is re-verified against the snapshot `oldValue`; any drift
 *      aborts the whole write with zero partial mutation.
 *   4. Immutable Audit Trail: Every committed mutation appends a structured
 *      record containing proposal ID, evidence chain, and human confirmation.
 */

const MIN_EVIDENCE_QUOTE_LEN = 6;
const MIN_HUMAN_QUOTE_LEN = 2;

export function createHitlProposalStore(initialFloorStates = {}) {
  /** @type {Map<number, Record<string, unknown>>} */
  const floorVars = new Map();
  for (const [floorKey, vars] of Object.entries(initialFloorStates)) {
    floorVars.set(Number(floorKey), structuredClone(vars));
  }

  /** @type {Map<string, object>} */
  const pending = new Map();
  /** @type {object[]} */
  const changeLog = [];
  let seq = 0;

  function getVars(floor) {
    return floorVars.get(Number(floor)) ?? {};
  }

  function validateChange(change, currentVars) {
    if (!change || typeof change !== 'object') return 'Change item must be an object';
    const keyPath = String(change.path ?? '').trim();
    if (!keyPath) return 'Missing required field: path';
    if (!('newValue' in change)) return `Path "${keyPath}" missing required field: newValue`;

    const evidence = change.evidence;
    if (!evidence || typeof evidence !== 'object') {
      return `Path "${keyPath}" missing required evidence object`;
    }
    const quote = String(evidence.quote ?? '').trim();
    if (quote.length < MIN_EVIDENCE_QUOTE_LEN) {
      return `Path "${keyPath}" evidence.quote too short (min ${MIN_EVIDENCE_QUOTE_LEN} chars)`;
    }
    const sourceFloor = Number(evidence.floor);
    if (!Number.isInteger(sourceFloor) || sourceFloor < 1) {
      return `Path "${keyPath}" evidence.floor must be a positive integer`;
    }

    const exists = Object.prototype.hasOwnProperty.call(currentVars, keyPath);
    if (exists && JSON.stringify(currentVars[keyPath]) === JSON.stringify(change.newValue)) {
      return `Path "${keyPath}" newValue equals current value (no-op rejected)`;
    }
    return null;
  }

  /**
   * Exposed to Agent: stages a proposal without touching committed state.
   * Rejects the entire batch if any single item fails validation.
   */
  function proposeChanges({ floor, changes, at = new Date().toISOString() }) {
    const list = Array.isArray(changes) ? changes : [];
    if (list.length === 0) return { ok: false, errors: ['Proposal contains no changes'] };

    const vars = getVars(floor);
    const errors = [];
    const normalized = [];

    list.forEach((change, idx) => {
      const err = validateChange(change, vars);
      if (err) {
        errors.push(`Item #${idx + 1}: ${err}`);
        return;
      }
      const keyPath = String(change.path).trim();
      const exists = Object.prototype.hasOwnProperty.call(vars, keyPath);
      normalized.push({
        path: keyPath,
        oldValue: exists ? structuredClone(vars[keyPath]) : null,
        newValue: structuredClone(change.newValue),
        op: exists ? 'update' : 'create',
        evidence: {
          quote: String(change.evidence.quote).trim(),
          floor: Number(change.evidence.floor),
        },
      });
    });

    if (errors.length > 0) return { ok: false, errors };

    seq += 1;
    const id = `prop-${String(seq).padStart(4, '0')}`;
    pending.set(id, { id, floor: Number(floor), createdAt: at, changes: normalized });
    return { ok: true, id, count: normalized.length };
  }

  /**
   * Exposed ONLY to Human UI (never registered as an Agent tool):
   * requires human confirmation quote + re-verifies every item's oldValue (CAS).
   */
  function applyProposal({ id, humanQuote, only = null, at = new Date().toISOString() }) {
    const record = pending.get(id);
    if (!record) return { ok: false, errors: [`Proposal not found: ${id}`] };

    const confirmation = String(humanQuote ?? '').trim();
    if (confirmation.length < MIN_HUMAN_QUOTE_LEN) {
      return {
        ok: false,
        errors: [`Human confirmation quote is required (min ${MIN_HUMAN_QUOTE_LEN} chars)`],
      };
    }

    let selected = record.changes;
    if (Array.isArray(only) && only.length > 0) {
      const wanted = new Set(only.map((p) => String(p).trim()));
      const missing = [...wanted].filter((p) => !record.changes.some((c) => c.path === p));
      if (missing.length > 0) {
        return { ok: false, errors: [`Requested paths not in proposal: ${missing.join(', ')}`] };
      }
      selected = record.changes.filter((c) => wanted.has(c.path));
    }

    // Per-item CAS re-verification against live committed state
    const liveVars = getVars(record.floor);
    const casErrors = [];
    for (const item of selected) {
      const liveNow = Object.prototype.hasOwnProperty.call(liveVars, item.path)
        ? liveVars[item.path]
        : null;
      if (JSON.stringify(liveNow) !== JSON.stringify(item.oldValue)) {
        casErrors.push(
          `CAS_CONFLICT on "${item.path}": expected ${JSON.stringify(item.oldValue)}, found ${JSON.stringify(liveNow)}`,
        );
      }
    }
    if (casErrors.length > 0) return { ok: false, code: 'CAS_CONFLICT', errors: casErrors };

    // Atomic commit & append-only audit log
    const nextVars = { ...structuredClone(liveVars) };
    for (const item of selected) {
      nextVars[item.path] = structuredClone(item.newValue);
    }
    floorVars.set(record.floor, nextVars);

    for (const item of selected) {
      changeLog.push({
        at,
        floor: record.floor,
        proposalId: record.id,
        path: item.path,
        oldValue: item.oldValue,
        newValue: item.newValue,
        evidence: item.evidence,
        humanQuote: confirmation,
      });
    }

    pending.delete(id);
    return { ok: true, applied: selected.length };
  }

  function rejectProposal({ id }) {
    if (!pending.has(id)) return { ok: false, errors: [`Proposal not found: ${id}`] };
    pending.delete(id);
    return { ok: true };
  }

  /** Simulates live gameplay advancing/mutating state while proposal waits for approval. */
  function mutateCommittedState(floor, keyPath, value) {
    const cur = { ...structuredClone(getVars(floor)) };
    cur[keyPath] = structuredClone(value);
    floorVars.set(Number(floor), cur);
  }

  return {
    proposeChanges,
    applyProposal,
    rejectProposal,
    mutateCommittedState,
    getCommittedState: (floor) => structuredClone(getVars(floor)),
    listPending: () => [...pending.values()].map((p) => structuredClone(p)),
    getChangeLog: () => structuredClone(changeLog),
  };
}
