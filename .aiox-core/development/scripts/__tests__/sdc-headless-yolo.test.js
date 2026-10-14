'use strict';

const assert = require('assert');
const fs = require('fs').promises;
const os = require('os');
const path = require('path');
const yaml = require('js-yaml');
const { SdcHeadlessYoloRunner, redact } = require('../../../core/orchestration/sdc-headless-yolo-runner');
const { parseArgs, createRunnerOptions } = require('../sdc-headless-yolo');

async function makeProject() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'aiox-sdc-'));
  await fs.mkdir(path.join(root, 'docs', 'workflows'), { recursive: true });
  await fs.writeFile(path.join(root, 'docs', 'workflows', 'source.md'), '# source\n', 'utf8');
  await fs.writeFile(path.join(root, 'docs', 'workflows', 'deploy.md'), '# deploy\n', 'utf8');
  return root;
}

function manifest(rootOverrides = {}) {
  return {
    sdc_execution: {
      source_artifact: 'docs/workflows/source.md',
      story_scope: 'all_unblocked',
      execution_mode: 'yolo',
      permissions_mode: 'auto',
      interaction_policy: 'never_prompt',
      on_missing_input: 'block_and_log',
      target_branch: 'feature/sdc',
      base_branch: 'main',
      deploy_environment: 'staging',
      deploy_runbook: 'docs/workflows/deploy.md',
      remote_repository: 'origin',
      remote_operations_authorized: true,
      pull_request_authorized: true,
      merge_authorized: true,
      release_authorized: true,
      deploy_authorized: true,
      rollback_authorized: true,
      migrations_authorized: false,
      destructive_migrations_authorized: false,
      max_qa_iterations: 2,
      ...rootOverrides,
    },
  };
}

async function testHappyPath() {
  const root = await makeProject();
  const operations = [];
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      devops: async (operation) => {
        operations.push(operation);
        return { status: 'completed', operation, simulated: true };
      },
    },
  });

  const result = await runner.execute(manifest());

  assert.strictEqual(result.status, 'completed');
  assert.strictEqual(result.terminal_status, 'deployed');
  assert.deepStrictEqual(operations, ['push', 'pull_request', 'merge', 'release', 'deploy']);
  assert.ok(result.execution_log);
}

async function testInvalidManifestBlocksWithoutPrompt() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({ projectRoot: root });
  const bad = manifest();
  delete bad.sdc_execution.source_artifact;

  const result = await runner.execute(bad);

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'MANIFEST_INVALID');
}

async function testPoNoGoRoutesToSm() {
  const root = await makeProject();
  let poCalls = 0;
  let smCalls = 0;
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      sm: async () => {
        smCalls += 1;
        return { status: 'completed' };
      },
      po: async () => {
        poCalls += 1;
        return poCalls === 1 ? { status: 'NO_GO' } : { status: 'GO' };
      },
    },
  });

  const result = await runner.execute(manifest({ remote_operations_authorized: false }));

  assert.strictEqual(result.terminal_status, 'PUSH_AUTHORIZATION_MISSING');
  assert.strictEqual(smCalls, 2);
}

async function testQaRetryLimit() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      qa: async () => ({ verdict: 'FAIL' }),
    },
  });

  const result = await runner.execute(manifest({ max_qa_iterations: 2 }));

  assert.strictEqual(result.status, 'blocked');
  assert.strictEqual(result.terminal_status, 'QA_MAX_ITERATIONS_EXCEEDED');
}

async function testTechnicalGateFailureBlocks() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      gates: async () => ({
        lint: 'PASS',
        typecheck: 'PASS',
        tests: 'FAIL',
        build: 'PASS',
        coderabbit: 'PASS',
        security: 'PASS',
      }),
    },
  });

  const result = await runner.execute(manifest());

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'PRE_SDC_GATE_BLOCKED');
}

async function testDeployRunbookMissingBlocks() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({ projectRoot: root });

  const result = await runner.execute(manifest({ deploy_runbook: 'docs/workflows/missing.md' }));

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'DEPLOY_NOT_CONFIGURED');
}

async function testSmokeFailureRollsBack() {
  const root = await makeProject();
  const operations = [];
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      devops: async (operation) => {
        operations.push(operation);
        return { status: 'completed', operation, simulated: true };
      },
      smoke: async () => ({ status: 'FAIL' }),
    },
  });

  const result = await runner.execute(manifest());

  assert.strictEqual(result.status, 'rolled_back');
  assert.strictEqual(result.terminal_status, 'rolled_back');
  assert.ok(operations.includes('rollback'));
}

async function testMigrationsRequireRollbackReapplyProof() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      migrations: async () => ({
        status: 'completed',
        destructive: false,
        apply: 'PASS',
        rollback: 'FAIL',
        reapply: 'PASS',
      }),
    },
  });

  const result = await runner.execute(manifest({ migrations_authorized: true }));

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'MIGRATION_VALIDATION_FAILED');
}

async function testDestructiveMigrationsRequireSpecificAuthorization() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      migrations: async () => ({
        status: 'completed',
        destructive: true,
        apply: 'PASS',
        rollback: 'PASS',
        reapply: 'PASS',
        backup_verified: true,
      }),
    },
  });

  const result = await runner.execute(manifest({ migrations_authorized: true }));

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'DESTRUCTIVE_MIGRATION_AUTHORIZATION_MISSING');
}

async function testResumeSkipsCompletedRemoteEffects() {
  const root = await makeProject();
  let pushCalls = 0;
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      devops: async (operation) => {
        if (operation === 'push') pushCalls += 1;
        return { status: 'completed', operation, simulated: true };
      },
    },
  });

  const state = runner.createInitialState(manifest().sdc_execution);
  state.current_phase = 'devops_push';
  state.effects.push = { status: 'completed', authority: '@devops', idempotency_key: 'existing' };
  await runner.saveState(state);

  const result = await runner.execute(manifest(), { resumeRunId: state.run_id });

  assert.strictEqual(result.terminal_status, 'deployed');
  assert.strictEqual(pushCalls, 0);
}

async function testResumeRejectsChangedManifest() {
  const root = await makeProject();
  const runner = new SdcHeadlessYoloRunner({ projectRoot: root });
  const state = runner.createInitialState(manifest().sdc_execution);
  state.current_phase = 'devops_push';
  await runner.saveState(state);

  const result = await runner.execute(
    manifest({ target_branch: 'feature/changed-after-start' }),
    { resumeRunId: state.run_id }
  );

  assert.strictEqual(result.status, 'failed');
  assert.strictEqual(result.terminal_status, 'MANIFEST_IMMUTABLE_VIOLATION');
}

async function testResumeSkipsAllCompletedRemoteEffects() {
  const root = await makeProject();
  const operations = [];
  const runner = new SdcHeadlessYoloRunner({
    projectRoot: root,
    adapters: {
      devops: async (operation) => {
        operations.push(operation);
        return { status: 'completed', operation, simulated: true };
      },
    },
  });

  const state = runner.createInitialState(manifest().sdc_execution);
  state.current_phase = 'devops_push';
  for (const operation of ['push', 'pull_request', 'merge', 'release', 'deploy']) {
    state.effects[operation] = {
      status: 'completed',
      authority: '@devops',
      idempotency_key: `existing:${operation}`,
    };
  }
  await runner.saveState(state);

  const result = await runner.execute(manifest(), { resumeRunId: state.run_id });

  assert.strictEqual(result.terminal_status, 'deployed');
  assert.deepStrictEqual(operations, []);
}

async function testRemoteAuthorizationFlagsBlockIndependently() {
  const cases = [
    ['remote_operations_authorized', false, 'PUSH_AUTHORIZATION_MISSING'],
    ['pull_request_authorized', false, 'PULL_REQUEST_AUTHORIZATION_MISSING'],
    ['merge_authorized', false, 'MERGE_AUTHORIZATION_MISSING'],
    ['release_authorized', false, 'RELEASE_AUTHORIZATION_MISSING'],
    ['deploy_authorized', false, 'DEPLOY_AUTHORIZATION_MISSING'],
  ];

  for (const [field, value, terminalStatus] of cases) {
    const root = await makeProject();
    const runner = new SdcHeadlessYoloRunner({ projectRoot: root });
    const result = await runner.execute(manifest({ [field]: value }));

    assert.strictEqual(result.status, 'failed', field);
    assert.strictEqual(result.terminal_status, terminalStatus, field);
  }
}

async function testCanonicalGuidedInteractiveMetadataIsPreserved() {
  const workflowPath = path.join(__dirname, '..', '..', 'workflows', 'story-development-cycle.yaml');
  const workflow = yaml.load(await fs.readFile(workflowPath, 'utf8')).workflow;

  assert.strictEqual(workflow.metadata.elicit, true);
  assert.strictEqual(workflow.metadata.confirmation_required, true);
  assert.strictEqual(workflow.metadata.headless_extension, 'story-development-cycle-headless-yolo');
  assert.ok(workflow.execution_modes.some((mode) => mode.mode === 'interactive' && mode.default === true));
  assert.ok(workflow.execution_modes.some((mode) => mode.mode === 'yolo'));
  assert.strictEqual(workflow.sequence.find((step) => step.id === 'review').next, 'devops_publish');
}

function testRedaction() {
  const output = redact({ token: 'abc', nested: { apiKey: 'def', safe: 'ok' } });
  assert.strictEqual(output.token, '[REDACTED]');
  assert.strictEqual(output.nested.apiKey, '[REDACTED]');
  assert.strictEqual(output.nested.safe, 'ok');
}

async function testCliRequiresDryRunOrAdapterModule() {
  const root = await makeProject();

  await assert.rejects(
    () => createRunnerOptions(parseArgs(['--manifest', 'manifest.yaml']), root),
    /Refusing non-dry-run execution without --adapter-module/
  );
}

async function testCliDryRunUsesSimulatedDevopsAdapter() {
  const root = await makeProject();
  const options = await createRunnerOptions(parseArgs(['--manifest', 'manifest.yaml', '--dry-run']), root);
  const result = await options.adapters.devops('deploy');

  assert.strictEqual(result.status, 'completed');
  assert.strictEqual(result.operation, 'deploy');
  assert.strictEqual(result.simulated, true);
}

async function testCliAdapterModuleRequiresDevopsFunction() {
  const root = await makeProject();
  await fs.writeFile(path.join(root, 'empty-adapters.js'), 'module.exports = {};', 'utf8');

  await assert.rejects(
    () => createRunnerOptions(parseArgs(['--manifest', 'manifest.yaml', '--adapter-module', 'empty-adapters.js']), root),
    /must export a devops adapter function/
  );
}

async function main() {
  const tests = [
    testHappyPath,
    testInvalidManifestBlocksWithoutPrompt,
    testPoNoGoRoutesToSm,
    testQaRetryLimit,
    testTechnicalGateFailureBlocks,
    testDeployRunbookMissingBlocks,
    testSmokeFailureRollsBack,
    testMigrationsRequireRollbackReapplyProof,
    testDestructiveMigrationsRequireSpecificAuthorization,
    testResumeSkipsCompletedRemoteEffects,
    testResumeRejectsChangedManifest,
    testResumeSkipsAllCompletedRemoteEffects,
    testRemoteAuthorizationFlagsBlockIndependently,
    testCanonicalGuidedInteractiveMetadataIsPreserved,
    testRedaction,
    testCliRequiresDryRunOrAdapterModule,
    testCliDryRunUsesSimulatedDevopsAdapter,
    testCliAdapterModuleRequiresDevopsFunction,
  ];

  for (const test of tests) {
    await test();
    console.log(`PASS ${test.name}`);
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
