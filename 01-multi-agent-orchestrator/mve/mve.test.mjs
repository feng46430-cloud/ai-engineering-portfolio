import test from 'node:test';
import assert from 'node:assert/strict';

import { createHitlProposalStore } from './hitl-proposal-gate.mjs';
import {
  splitOutput,
  readVerdict,
  stripMeta,
  VERDICT_PASS,
  VERDICT_FAIL,
} from './tolerant-splitter-and-verdict.mjs';

// ============================================================================
// Suite 1: HITL Proposal Write-Safety & Per-Item CAS Gate
// ============================================================================

test('HITL: rejects entire proposal if any item lacks verbatim quote (>=6 chars) or valid floor', () => {
  const store = createHitlProposalStore({ 12: { 'reputation': 40, 'gold': 500 } });
  const res = store.proposeChanges({
    floor: 12,
    changes: [
      {
        path: 'reputation',
        newValue: 55,
        evidence: { quote: '城主当众宣布赏赐十五点声望', floor: 12 },
      },
      {
        path: 'gold',
        newValue: 800,
        evidence: { quote: '太短了', floor: 12 }, // < 6 chars
      },
    ],
  });

  assert.equal(res.ok, false);
  assert.equal(store.listPending().length, 0);
  assert.deepEqual(store.getCommittedState(12), { reputation: 40, gold: 500 });
});

test('HITL: rejects no-op proposals where newValue equals current value', () => {
  const store = createHitlProposalStore({ 5: { 'hp': 100 } });
  const res = store.proposeChanges({
    floor: 5,
    changes: [
      { path: 'hp', newValue: 100, evidence: { quote: '他在营地休息了一整晚未受伤', floor: 5 } },
    ],
  });
  assert.equal(res.ok, false);
  assert.match(res.errors[0], /no-op/i);
});

test('HITL: blocks applyProposal without explicit human confirmation quote (>=2 chars)', () => {
  const store = createHitlProposalStore({ 8: { 'rank': 'T1' } });
  const staged = store.proposeChanges({
    floor: 8,
    changes: [
      { path: 'rank', newValue: 'T2', evidence: { quote: '评委会正式授予二阶资格证书', floor: 8 } },
    ],
  });
  assert.equal(staged.ok, true);

  const denied = store.applyProposal({ id: staged.id, humanQuote: ' ' });
  assert.equal(denied.ok, false);
  assert.equal(store.getCommittedState(8).rank, 'T1');
  assert.equal(store.listPending().length, 1);
});

test('HITL: commits atomically with human quote and writes immutable change log', () => {
  const store = createHitlProposalStore({ 10: { 'trust': 20 } });
  const staged = store.proposeChanges({
    floor: 10,
    changes: [
      { path: 'trust', newValue: 35, evidence: { quote: '老铁匠把暗室钥匙交到了你手里', floor: 10 } },
      { path: 'flag.secretKey', newValue: true, evidence: { quote: '老铁匠把暗室钥匙交到了你手里', floor: 10 } },
    ],
  });

  const applied = store.applyProposal({ id: staged.id, humanQuote: '确认按原文写入' });
  assert.equal(applied.ok, true);
  assert.equal(applied.applied, 2);
  assert.deepEqual(store.getCommittedState(10), { trust: 35, 'flag.secretKey': true });
  assert.equal(store.listPending().length, 0);

  const log = store.getChangeLog();
  assert.equal(log.length, 2);
  assert.equal(log[0].humanQuote, '确认按原文写入');
  assert.equal(log[0].oldValue, 20);
  assert.equal(log[0].newValue, 35);
});

test('HITL: per-item CAS aborts entire write if live state drifted before human approval', () => {
  const store = createHitlProposalStore({ 15: { 'gold': 100, 'morale': 60 } });
  const staged = store.proposeChanges({
    floor: 15,
    changes: [
      { path: 'gold', newValue: 250, evidence: { quote: '商队结清了一百五十枚金币尾款', floor: 15 } },
      { path: 'morale', newValue: 70, evidence: { quote: '队员听闻奖金发放士气大振', floor: 15 } },
    ],
  });

  // Live state advances on 'gold' while proposal is awaiting approval
  store.mutateCommittedState(15, 'gold', 120);

  const result = store.applyProposal({ id: staged.id, humanQuote: '同意应用' });
  assert.equal(result.ok, false);
  assert.equal(result.code, 'CAS_CONFLICT');
  // Zero partial mutation: 'morale' must remain untouched at 60
  assert.deepEqual(store.getCommittedState(15), { gold: 120, morale: 60 });
  assert.equal(store.getChangeLog().length, 0);
});

test('HITL: rejectProposal drops pending file without touching committed state', () => {
  const store = createHitlProposalStore({ 3: { 'debt': 300 } });
  const staged = store.proposeChanges({
    floor: 3,
    changes: [
      { path: 'debt', newValue: 0, evidence: { quote: '神秘资助人替你还清了全部欠款', floor: 3 } },
    ],
  });
  const rej = store.rejectProposal({ id: staged.id });
  assert.equal(rej.ok, true);
  assert.equal(store.listPending().length, 0);
  assert.equal(store.getCommittedState(3).debt, 300);
});

// ============================================================================
// Suite 2: Tolerant Output Contract Splitter, Verdict Reader & Meta Stripper
// ============================================================================

test('splitOutput: Level 1 strict closed tags extract cleanly with zero notes', () => {
  const res = splitOutput({
    text: '<beats>先压低气氛再反转</beats>\n<prose>雨点砸在铁皮屋檐上。</prose>',
    outNames: ['beats', 'prose'],
  });
  assert.deepEqual(res.errors, []);
  assert.deepEqual(res.notes, []);
  assert.equal(res.values.beats, '先压低气氛再反转');
  assert.equal(res.values.prose, '雨点砸在铁皮屋檐上。');
});

test('splitOutput: Level 2 unclosed tag recovers safely to EOF and logs diagnostic note', () => {
  const res = splitOutput({
    text: '<prose>他推开酒馆木门，寒风灌入室内。',
    outNames: ['prose'],
  });
  assert.deepEqual(res.errors, []);
  assert.equal(res.values.prose, '他推开酒馆木门，寒风灌入室内。');
  assert.equal(res.notes.length, 1);
  assert.match(res.notes[0], /missing closing tag/i);
});

test('splitOutput: concatenates duplicate identical tags in appearance order', () => {
  const res = splitOutput({
    text: '<prose>第一段正文。</prose>\n无关过渡\n<prose>第二段正文。</prose>',
    outNames: ['prose'],
  });
  assert.deepEqual(res.errors, []);
  assert.equal(res.values.prose, '第一段正文。\n\n第二段正文。');
  assert.match(res.notes[0], /appeared 2 times/i);
});

test('splitOutput: single-output step accepts untagged response wholly', () => {
  const res = splitOutput({
    text: '夜色沉入港湾，远处的灯塔明灭不定。',
    outNames: ['正文'],
  });
  assert.deepEqual(res.errors, []);
  assert.equal(res.values['正文'], '夜色沉入港湾，远处的灯塔明灭不定。');
  assert.match(res.notes[0], /untagged/i);
});

test('splitOutput: multi-output falls back to Markdown headings and errors only on genuinely missing slots', () => {
  const res = splitOutput({
    text: '## 节拍\n开场压迫感\n\n## 正文\n石门缓缓合拢。',
    outNames: ['节拍', '正文', '结算'],
  });
  assert.equal(res.values['节拍'], '开场压迫感');
  assert.equal(res.values['正文'], '石门缓缓合拢。');
  assert.equal(res.errors.length, 1);
  assert.match(res.errors[0], /结算/);
});

test('readVerdict: checks FAIL ("不通过") strictly before PASS ("通过") to prevent substring bug', () => {
  assert.equal(readVerdict('判决：不通过\n原因：第3段违背角色私有视野'), VERDICT_FAIL);
  assert.equal(readVerdict('虽然节奏通过，但核心规则不通过'), VERDICT_FAIL);
  assert.equal(readVerdict('判决：通过\n原因：符合所有硬约束'), VERDICT_PASS);
});

test('readVerdict: ignores PASS/FAIL words appearing after the first 5 non-empty lines', () => {
  const longRationale = [
    '审校摘要：本轮存在两处边界争议',
    '细节 1：台词节奏偏紧',
    '细节 2：伏笔回收完整',
    '细节 3：数值校验一致',
    '细节 4：等待人工确认',
    '附注：上轮曾判定通过，本轮未显式给结论',
  ].join('\n');
  assert.equal(readVerdict(longRationale), undefined);
});

test('stripMeta: strips internal settlement/thinking blocks while preserving clean prose', () => {
  const raw = [
    '<Analysis>内部草稿推理</Analysis>',
    '他收起长剑，转身没入雨幕。<br/>',
    '<UpdateVariable><JSONPatch>[{"op":"replace","path":"/hp","value":80}]</JSONPatch></UpdateVariable>',
    '<details><summary>状态</summary>HP: 80</details>',
    '',
    '',
    '街角只余下一盏摇晃的煤油灯。',
  ].join('\n');

  assert.equal(stripMeta(raw), '他收起长剑，转身没入雨幕。\n\n街角只余下一盏摇晃的煤油灯。');
});
