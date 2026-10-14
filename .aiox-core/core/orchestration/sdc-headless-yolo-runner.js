'use strict';

const crypto = require('crypto');
const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const REQUIRED_MANIFEST_FIELDS = [
  'source_artifact',
  'story_scope',
  'execution_mode',
  'permissions_mode',
  'interaction_policy',
  'on_missing_input',
  'target_branch',
  'base_branch',
  'deploy_environment',
  'deploy_runbook',
  'remote_repository',
  'remote_operations_authorized',
  'pull_request_authorized',
  'merge_authorized',
  'release_authorized',
  'deploy_authorized',
  'rollback_authorized',
  'migrations_authorized',
  'destructive_migrations_authorized',
  'max_qa_iterations',
];

const REMOTE_OPERATIONS = {
  push: 'remote_operations_authorized',
  pull_request: 'pull_request_authorized',
  merge: 'merge_authorized',
  release: 'release_authorized',
  deploy: 'deploy_authorized',
};

const SECRET_KEY_PATTERN = /(secret|token|password|passwd|credential|api[_-]?key|private[_-]?key)/i;

function stableStringify(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(',')}}`;
  }
  return JSON.stringify(value);
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function redact(value) {
  if (Array.isArray(value)) {
    return value.map((item) => redact(item));
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, child]) => [
        key,
        SECRET_KEY_PATTERN.test(key) ? '[REDACTED]' : redact(child),
      ]),
    );
  }
  return value;
}

function normalizeManifest(rawManifest) {
  if (!rawManifest || typeof rawManifest !== 'object') {
    throw new Error('Manifest must be an object');
  }
  return rawManifest.sdc_execution || rawManifest;
}

class SdcHeadlessYoloRunner {
  constructor(options = {}) {
    this.projectRoot = options.projectRoot || process.cwd();
    this.stateDir = options.stateDir || path.join(this.projectRoot, '.aiox', 'sdc-headless');
    this.logsDir = options.logsDir || path.join(this.projectRoot, 'docs', 'workflows', 'logs');
    this.maxTransitions = options.maxTransitions || 200;
    this.now = options.now || (() => new Date());
    this.adapters = {
      sm: async () => ({ status: 'completed', story_status: 'Draft' }),
      po: async () => ({ status: 'GO', story_status: 'Approved' }),
      dev: async () => ({ status: 'completed' }),
      qa: async () => ({ verdict: 'PASS' }),
      gates: async () => ({
        lint: 'PASS',
        typecheck: 'PASS',
        tests: 'PASS',
        build: 'PASS',
        coderabbit: 'PASS',
        security: 'PASS',
      }),
      migrations: async () => ({
        status: 'skipped',
        destructive: false,
        apply: 'PASS',
        rollback: 'PASS',
        reapply: 'PASS',
        backup_verified: true,
      }),
      devops: async (operation) => ({ status: 'completed', operation, simulated: true }),
      smoke: async () => ({ status: 'PASS' }),
      ...options.adapters,
    };
  }

  async loadManifest(input) {
    if (typeof input === 'string') {
      const manifestPath = path.isAbsolute(input) ? input : path.join(this.projectRoot, input);
      const content = await fs.readFile(manifestPath, 'utf8');
      const data = manifestPath.endsWith('.json') ? JSON.parse(content) : yaml.load(content);
      return normalizeManifest(data);
    }
    return normalizeManifest(input);
  }

  validateManifest(manifest) {
    const errors = [];
    const missing = REQUIRED_MANIFEST_FIELDS.filter((field) => manifest[field] === undefined);

    for (const field of missing) {
      errors.push({ code: 'MANIFEST_FIELD_MISSING', field });
    }

    if (manifest.execution_mode !== undefined && manifest.execution_mode !== 'yolo') {
      errors.push({ code: 'MANIFEST_EXECUTION_MODE_NOT_YOLO', field: 'execution_mode' });
    }
    if (manifest.interaction_policy !== undefined && manifest.interaction_policy !== 'never_prompt') {
      errors.push({ code: 'MANIFEST_INTERACTION_POLICY_INVALID', field: 'interaction_policy' });
    }
    if (
      manifest.on_missing_input !== undefined &&
      manifest.on_missing_input !== 'block_and_log'
    ) {
      errors.push({ code: 'MANIFEST_MISSING_INPUT_POLICY_INVALID', field: 'on_missing_input' });
    }
    if (
      manifest.max_qa_iterations !== undefined &&
      (!Number.isInteger(manifest.max_qa_iterations) || manifest.max_qa_iterations < 1)
    ) {
      errors.push({ code: 'MANIFEST_MAX_QA_ITERATIONS_INVALID', field: 'max_qa_iterations' });
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  fingerprintManifest(manifest) {
    return crypto.createHash('sha256').update(stableStringify(manifest)).digest('hex');
  }

  createInitialState(manifest) {
    const now = this.now().toISOString();
    const runId = `sdc-headless-${now.replace(/[:.]/g, '-')}`;
    return {
      version: '1.0.0',
      run_id: runId,
      status: 'active',
      terminal_status: null,
      current_phase: 'manifest_validation',
      manifest_snapshot: clone(manifest),
      manifest_fingerprint: this.fingerprintManifest(manifest),
      counters: {
        po_iterations: 0,
        qa_iterations: 0,
      },
      gates: {},
      effects: {},
      transitions: [],
      blocks: [],
      started_at: now,
      updated_at: now,
    };
  }

  async loadState(runId) {
    const statePath = this.getStatePath(runId);
    const content = await fs.readFile(statePath, 'utf8');
    return yaml.load(content);
  }

  getStatePath(runId) {
    if (!runId || runId.includes('..') || runId.includes('/') || runId.includes('\\')) {
      throw new Error('Invalid run id');
    }
    return path.join(this.stateDir, `${runId}.yaml`);
  }

  async saveState(state) {
    await fs.mkdir(this.stateDir, { recursive: true });
    state.updated_at = this.now().toISOString();
    await fs.writeFile(this.getStatePath(state.run_id), yaml.dump(state, { lineWidth: 120 }), 'utf8');
  }

  async writeExecutionLog(state) {
    await fs.mkdir(this.logsDir, { recursive: true });
    const artifact = path.basename(String(state.manifest_snapshot.source_artifact || 'manifest'))
      .replace(/[^A-Za-z0-9._-]/g, '-')
      .replace(/-+/g, '-');
    const logPath = path.join(this.logsDir, `SDC-${artifact}-${state.started_at.replace(/[:.]/g, '-')}.md`);
    const lines = [
      `# SDC Headless YOLO Run ${state.run_id}`,
      '',
      `Status: ${state.status}`,
      `Terminal: ${state.terminal_status || 'active'}`,
      `Started: ${state.started_at}`,
      `Updated: ${state.updated_at}`,
      `Manifest fingerprint: ${state.manifest_fingerprint}`,
      '',
      '## Manifest Snapshot',
      '',
      '```yaml',
      yaml.dump({ sdc_execution: redact(state.manifest_snapshot) }, { lineWidth: 120 }).trim(),
      '```',
      '',
      '## Transitions',
      '',
      ...state.transitions.map(
        (entry) => `- ${entry.at} | ${entry.from} -> ${entry.to} | ${entry.code || entry.status || 'OK'}`,
      ),
      '',
      '## Blocks',
      '',
      ...(state.blocks.length
        ? state.blocks.map((entry) => `- ${entry.at} | ${entry.code}: ${entry.reason}`)
        : ['- none']),
    ];
    await fs.writeFile(logPath, `${lines.join('\n')}\n`, 'utf8');
    state.execution_log = path.relative(this.projectRoot, logPath).replace(/\\/g, '/');
    await this.saveState(state);
    return logPath;
  }

  async execute(input, options = {}) {
    const manifest = await this.loadManifest(input);
    let state;

    if (options.resumeRunId) {
      state = await this.loadState(options.resumeRunId);
      const incomingFingerprint = this.fingerprintManifest(manifest);
      if (incomingFingerprint !== state.manifest_fingerprint) {
        return this.halt(state, 'MANIFEST_IMMUTABLE_VIOLATION', 'Manifest changed after run start');
      }
    } else {
      state = this.createInitialState(manifest);
      await this.saveState(state);
    }

    for (let i = 0; i < this.maxTransitions && state.status === 'active'; i += 1) {
      await this.step(state);
      await this.saveState(state);
    }

    if (state.status === 'active') {
      this.halt(state, 'MAX_TRANSITIONS_EXCEEDED', 'Transition limit reached');
    }

    await this.writeExecutionLog(state);
    return state;
  }

  async step(state) {
    switch (state.current_phase) {
      case 'manifest_validation':
        return this.stepManifestValidation(state);
      case 'sm_story_creation':
        return this.stepSm(state);
      case 'po_story_validation':
        return this.stepPo(state);
      case 'dev_implementation':
        return this.stepDev(state);
      case 'qa_review':
        return this.stepQa(state);
      case 'quality_gates':
        return this.stepQualityGates(state);
      case 'migration_validation':
        return this.stepMigrations(state);
      case 'devops_push':
        return this.stepRemoteOperation(state, 'push', 'devops_pr');
      case 'devops_pr':
        return this.stepRemoteOperation(state, 'pull_request', 'devops_merge');
      case 'devops_merge':
        return this.stepRemoteOperation(state, 'merge', 'devops_release');
      case 'devops_release':
        return this.stepRemoteOperation(state, 'release', 'devops_deploy');
      case 'devops_deploy':
        return this.stepDeploy(state);
      case 'post_deploy_smoke':
        return this.stepSmoke(state);
      default:
        return this.halt(state, 'UNKNOWN_PHASE', `Unknown phase: ${state.current_phase}`);
    }
  }

  transition(state, to, details = {}) {
    const from = state.current_phase;
    state.current_phase = to;
    state.transitions.push({
      at: this.now().toISOString(),
      from,
      to,
      ...details,
    });
  }

  halt(state, code, reason) {
    state.status = ['QA_MAX_ITERATIONS_EXCEEDED'].includes(code) ? 'blocked' : 'failed';
    state.terminal_status = code;
    state.blocks.push({
      at: this.now().toISOString(),
      code,
      reason,
    });
    state.transitions.push({
      at: this.now().toISOString(),
      from: state.current_phase,
      to: state.status,
      code,
    });
    return state;
  }

  complete(state, terminalStatus) {
    state.status = terminalStatus === 'rolled_back' ? 'rolled_back' : 'completed';
    state.terminal_status = terminalStatus;
    state.transitions.push({
      at: this.now().toISOString(),
      from: state.current_phase,
      to: terminalStatus,
      status: terminalStatus,
    });
    return state;
  }

  async stepManifestValidation(state) {
    const validation = this.validateManifest(state.manifest_snapshot);
    state.gates.manifest = validation;
    if (!validation.valid) {
      return this.halt(
        state,
        'MANIFEST_INVALID',
        validation.errors.map((error) => error.field || error.code).join(', '),
      );
    }

    const sourcePath = path.join(this.projectRoot, state.manifest_snapshot.source_artifact);
    if (!fsSync.existsSync(sourcePath)) {
      return this.halt(state, 'SOURCE_ARTIFACT_NOT_FOUND', state.manifest_snapshot.source_artifact);
    }

    this.transition(state, 'sm_story_creation', { status: 'manifest_validated' });
    return state;
  }

  async stepSm(state) {
    const result = await this.adapters.sm({ state: clone(state), agent: '@sm' });
    if (result.status !== 'completed') {
      return this.halt(state, 'SM_STORY_CREATION_FAILED', result.reason || 'SM did not complete');
    }
    state.sm_result = result;
    this.transition(state, 'po_story_validation', { status: 'story_drafted' });
    return state;
  }

  async stepPo(state) {
    state.counters.po_iterations += 1;
    const result = await this.adapters.po({ state: clone(state), agent: '@po' });
    state.po_result = result;
    if (result.status === 'GO') {
      this.transition(state, 'dev_implementation', { status: 'po_go' });
      return state;
    }
    if (result.status === 'NO_GO') {
      if (state.counters.po_iterations >= (state.manifest_snapshot.max_po_iterations || 3)) {
        return this.halt(state, 'STORY_VALIDATION_EXTERNAL_BLOCKER', result.reason || 'PO NO-GO limit');
      }
      this.transition(state, 'sm_story_creation', { status: 'po_no_go' });
      return state;
    }
    return this.halt(state, 'PO_VALIDATION_INVALID_RESULT', `Unexpected PO status: ${result.status}`);
  }

  async stepDev(state) {
    const result = await this.adapters.dev({ state: clone(state), agent: '@dev' });
    state.dev_result = result;
    if (result.status !== 'completed') {
      return this.halt(state, 'DEV_IMPLEMENTATION_FAILED', result.reason || 'Dev did not complete');
    }
    this.transition(state, 'qa_review', { status: 'dev_complete' });
    return state;
  }

  async stepQa(state) {
    state.counters.qa_iterations += 1;
    const result = await this.adapters.qa({ state: clone(state), agent: '@qa' });
    state.qa_result = result;
    if (result.verdict === 'PASS' || result.verdict === 'WAIVED') {
      this.transition(state, 'quality_gates', { status: `qa_${String(result.verdict).toLowerCase()}` });
      return state;
    }
    if (result.verdict === 'FAIL') {
      if (state.counters.qa_iterations >= state.manifest_snapshot.max_qa_iterations) {
        return this.halt(state, 'QA_MAX_ITERATIONS_EXCEEDED', 'QA retry limit reached');
      }
      this.transition(state, 'dev_implementation', { status: 'qa_fail_retry' });
      return state;
    }
    if (result.verdict === 'CONCERNS') {
      return this.halt(state, 'QUALITY_GATE_CONCERNS', result.reason || 'QA concerns require explicit waiver');
    }
    return this.halt(state, 'QA_INVALID_VERDICT', `Unexpected QA verdict: ${result.verdict}`);
  }

  async stepQualityGates(state) {
    const gates = await this.adapters.gates({ state: clone(state) });
    state.gates.technical = gates;
    const required = ['lint', 'typecheck', 'tests', 'build', 'coderabbit', 'security'];
    const failed = required.filter((gate) => gates[gate] !== 'PASS' && gates[gate] !== 'WAIVED');
    if (failed.length > 0) {
      return this.halt(state, 'PRE_SDC_GATE_BLOCKED', failed.join(', '));
    }
    this.transition(state, 'migration_validation', { status: 'quality_gates_passed' });
    return state;
  }

  async stepMigrations(state) {
    if (state.effects.migrations?.status === 'completed' || state.effects.migrations?.status === 'skipped') {
      this.transition(state, 'devops_push', { status: `migrations_${state.effects.migrations.status}` });
      return state;
    }

    if (state.manifest_snapshot.migrations_authorized !== true) {
      state.effects.migrations = {
        status: 'skipped',
        at: this.now().toISOString(),
        reason: 'migrations_authorized is false',
      };
      this.transition(state, 'devops_push', { status: 'migrations_skipped' });
      return state;
    }

    const result = await this.adapters.migrations({ state: clone(state), agent: '@dev' });
    if (result.destructive === true && state.manifest_snapshot.destructive_migrations_authorized !== true) {
      return this.halt(
        state,
        'DESTRUCTIVE_MIGRATION_AUTHORIZATION_MISSING',
        'destructive_migrations_authorized is not true',
      );
    }

    const proofOk =
      result.status === 'completed' &&
      result.apply === 'PASS' &&
      result.rollback === 'PASS' &&
      result.reapply === 'PASS' &&
      (result.destructive !== true || result.backup_verified === true);

    if (!proofOk) {
      return this.halt(
        state,
        'MIGRATION_VALIDATION_FAILED',
        'Migration requires apply, rollback, reapply and destructive backup evidence',
      );
    }

    state.effects.migrations = {
      status: 'completed',
      at: this.now().toISOString(),
      destructive: result.destructive === true,
      backup_verified: result.backup_verified === true,
    };
    this.transition(state, 'devops_push', { status: 'migrations_validated' });
    return state;
  }

  async stepRemoteOperation(state, operation, nextPhase) {
    if (state.effects[operation]?.status === 'completed') {
      this.transition(state, nextPhase, { status: `${operation}_already_completed` });
      return state;
    }

    const requiredFlag = REMOTE_OPERATIONS[operation];
    if (state.manifest_snapshot[requiredFlag] !== true) {
      return this.halt(
        state,
        `${operation.toUpperCase()}_AUTHORIZATION_MISSING`,
        `${requiredFlag} is not true`,
      );
    }

    const result = await this.adapters.devops(operation, { state: clone(state), agent: '@devops' });
    if (result.status !== 'completed') {
      return this.halt(state, `${operation.toUpperCase()}_FAILED`, result.reason || 'DevOps operation failed');
    }
    state.effects[operation] = {
      status: 'completed',
      at: this.now().toISOString(),
      authority: '@devops',
      idempotency_key: result.idempotency_key || `${state.run_id}:${operation}`,
      simulated: result.simulated === true,
    };
    this.transition(state, nextPhase, { status: `${operation}_completed` });
    return state;
  }

  async stepDeploy(state) {
    const runbookPath = path.join(this.projectRoot, state.manifest_snapshot.deploy_runbook || '');
    if (!state.manifest_snapshot.deploy_runbook || !fsSync.existsSync(runbookPath)) {
      return this.halt(state, 'DEPLOY_NOT_CONFIGURED', 'deploy_runbook does not exist');
    }
    if (state.manifest_snapshot.deploy_authorized !== true) {
      return this.halt(state, 'DEPLOY_AUTHORIZATION_MISSING', 'deploy_authorized is not true');
    }
    if (state.manifest_snapshot.rollback_authorized !== true) {
      return this.halt(state, 'ROLLBACK_AUTHORIZATION_MISSING', 'rollback_authorized is required before deploy');
    }
    return this.stepRemoteOperation(state, 'deploy', 'post_deploy_smoke');
  }

  async stepSmoke(state) {
    const result = await this.adapters.smoke({ state: clone(state) });
    state.smoke_result = result;
    if (result.status === 'PASS') {
      return this.complete(state, 'deployed');
    }
    if (state.manifest_snapshot.rollback_authorized === true) {
      const rollback = await this.adapters.devops('rollback', { state: clone(state), agent: '@devops' });
      state.effects.rollback = {
        status: rollback.status === 'completed' ? 'completed' : 'failed',
        at: this.now().toISOString(),
        authority: '@devops',
        simulated: rollback.simulated === true,
      };
      return rollback.status === 'completed'
        ? this.complete(state, 'rolled_back')
        : this.halt(state, 'ROLLBACK_FAILED', rollback.reason || 'Rollback failed');
    }
    return this.halt(state, 'POST_DEPLOY_SMOKE_FAILED', result.reason || 'Smoke failed');
  }
}

module.exports = {
  SdcHeadlessYoloRunner,
  REQUIRED_MANIFEST_FIELDS,
  stableStringify,
  redact,
};
