/**
 * MVE-2 · Tolerant Output Contract Splitter, Critic Verdict Reader & Meta Stripper
 * -----------------------------------------------------------------------------
 * Clean-room Minimal Verifiable Extract (zero external dependencies) distilled
 * from the production multi-agent engine (`split.mjs` + `run.mjs`).
 *
 * Design rationale:
 *   1. Tolerant Splitting (`splitOutput`):
 *      - Tags belong to the engine; models focus on content.
 *      - Single-output steps accept raw untagged text cleanly (recorded in `notes`).
 *      - Unclosed tag (<draft> without </draft>) recovers safely to EOF rather
 *        than wasting tokens on a full retry, logging a structured diagnostic note.
 *      - Repeated identical tags concatenate in appearance order.
 *      - Multi-output steps fall back to Markdown `## OutputName` headings, and
 *        raise hard errors ONLY when a declared output is genuinely absent.
 *   2. Substring-Safe Critic Verdict (`readVerdict`):
 *      - Inspects only the first 5 non-empty lines (ignoring rationale body).
 *      - Evaluates FAIL ("不通过") strictly BEFORE PASS ("通过"), preventing
 *        "不通过" from falsely matching its own substring "通过".
 *   3. Pre-Release Meta Stripping (`stripMeta`):
 *      - Strips internal settlement/scratch blocks (<details>, <UpdateVariable>,
 *        <Analysis>, <JSONPatch>) and excess blank runs before user release.
 */

export const VERDICT_PASS = '通过';
export const VERDICT_FAIL = '不通过';

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function sectionOf(source, name) {
  const escaped = escapeRegExp(name);
  const pattern = new RegExp(
    `^#{1,6}\\s*${escaped}\\s*$([\\s\\S]*?)(?=^#{1,6}\\s*\\S+\\s*$|$(?![\\s\\S]))`,
    'm',
  );
  const match = source.match(pattern);
  if (!match) return undefined;
  const body = match[1].trim();
  return body === '' ? undefined : body;
}

/**
 * Splits a raw LLM response into declared named output slots.
 * @param {{ text: string, outNames: string[], tags?: Record<string, string> }} args
 * @returns {{ values: Record<string, string>, errors: string[], notes: string[] }}
 */
export function splitOutput({ text, outNames, tags = {} }) {
  const tagOf = (name) =>
    typeof tags[name] === 'string' && tags[name].trim() ? tags[name].trim() : name;
  const values = {};
  const errors = [];
  const notes = [];
  const source = String(text ?? '');
  const names = Array.isArray(outNames) ? outNames.map((n) => String(n)) : [];

  if (names.length === 0) {
    errors.push('No output slots declared for this step');
    return { values, errors, notes };
  }

  const missing = [];

  for (const name of names) {
    const tagName = tagOf(name);
    const open = `<${tagName}>`;
    const close = `</${tagName}>`;
    const found = [];
    let from = 0;

    for (;;) {
      const at = source.indexOf(open, from);
      if (at < 0) break;
      const end = source.indexOf(close, at + open.length);
      if (end < 0) break;
      found.push(source.slice(at + open.length, end).trim());
      from = end + close.length;
    }

    if (found.length > 0) {
      values[name] = found.filter((piece) => piece !== '').join('\n\n');
      if (found.length > 1) {
        notes.push(`Tag <${tagName}> appeared ${found.length} times; concatenated in order`);
      }
      continue;
    }

    // Level 2 tolerant recovery: open tag present, closing tag omitted -> slice to EOF
    const openAt = source.indexOf(open);
    if (openAt >= 0 && source.indexOf(close) < 0) {
      const tail = source.slice(openAt + open.length).trim();
      if (tail) {
        values[name] = tail;
        notes.push(`Tag <${tagName}> missing closing tag; recovered safely to EOF`);
        continue;
      }
    }

    missing.push(name);
  }

  if (missing.length === 0) return { values, errors, notes };

  // Single-output fast path: untagged body belongs wholly to the single declared slot
  if (names.length === 1) {
    const whole = source.trim();
    if (whole) {
      values[missing[0]] = whole;
      notes.push(`Single output <${missing[0]}> untagged; accepted whole response`);
      return { values, errors, notes };
    }
  }

  // Multi-output heading fallback: `## OutputName`
  for (const name of missing) {
    const section = sectionOf(source, name);
    if (section !== undefined) {
      values[name] = section;
      notes.push(`Output "${name}" recovered via Markdown heading fallback`);
    } else {
      errors.push(`Missing declared output: <${name}>`);
    }
  }

  return { values, errors, notes };
}

/**
 * Reads critic verdict from the first 5 non-empty lines only.
 * Checks FAIL ("不通过") strictly before PASS ("通过") to prevent substring inversion.
 */
export function readVerdict(text) {
  const lines = String(text ?? '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  for (const line of lines.slice(0, 5)) {
    if (line.includes(VERDICT_FAIL)) return VERDICT_FAIL;
    if (line.includes(VERDICT_PASS)) return VERDICT_PASS;
  }
  return undefined;
}

const META_TAGS = ['details', 'UpdateVariable', 'Analysis', 'JSONPatch'];
const META_BLOCKS = META_TAGS.map((tag) => new RegExp(`<${tag}>[\\s\\S]*?</${tag}>`, 'gi'));
const BR_TAG = /<br[^>]*>/gi;

/**
 * Strips internal settlement / reasoning blocks before releasing prose to the player.
 */
export function stripMeta(text) {
  let out = String(text ?? '');
  for (const re of META_BLOCKS) out = out.replace(re, '');
  out = out.replace(BR_TAG, '');
  return out.replace(/\n{3,}/g, '\n\n').trim();
}
