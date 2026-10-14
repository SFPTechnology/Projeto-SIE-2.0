#!/usr/bin/env node
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');

const sourceFiles = [
  '.aiox-core/core/orchestration/sdc-headless-yolo-runner.js',
  '.aiox-core/development/scripts/sdc-headless-yolo.js',
  '.aiox-core/development/scripts/__tests__/sdc-headless-yolo.test.js',
];

const workflowFiles = [
  '.aiox-core/development/workflows/story-development-cycle.yaml',
  '.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml',
];

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: projectRoot,
    encoding: 'utf8',
    stdio: options.capture ? 'pipe' : 'inherit',
    shell: false,
  });

  if (options.expectFailure) {
    if (result.status === 0) {
      throw new Error(`${command} ${args.join(' ')} was expected to fail but passed`);
    }
    if (options.expectedText) {
      const output = `${result.stdout || ''}${result.stderr || ''}`;
      if (!output.includes(options.expectedText)) {
        throw new Error(`Expected failure text not found: ${options.expectedText}`);
      }
    }
    return result;
  }

  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(' ')} failed with exit code ${result.status}`);
  }

  return result;
}

async function validateWorkflowFiles() {
  const { WorkflowValidator } = require('../.aiox-core/development/scripts/workflow-validator');
  const validator = new WorkflowValidator();

  for (const file of workflowFiles) {
    const result = await validator.validate(file);
    console.log(`${file}: valid=${result.valid} errors=${result.errors.length} warnings=${result.warnings.length}`);
    if (!result.valid || result.warnings.length > 0) {
      const errors = result.errors.map((entry) => entry.message || String(entry));
      const warnings = result.warnings.map((entry) => entry.message || String(entry));
      throw new Error([file, ...errors, ...warnings].join('\n'));
    }
  }
}

function validateSyntax() {
  for (const file of sourceFiles) {
    run(process.execPath, ['-c', file]);
  }
}

function validateExports() {
  const orchestration = require('../.aiox-core/core/orchestration');
  const cli = require('../.aiox-core/development/scripts/sdc-headless-yolo');

  if (typeof orchestration.SdcHeadlessYoloRunner !== 'function') {
    throw new Error('SdcHeadlessYoloRunner export is missing');
  }
  if (!Array.isArray(orchestration.SDC_REQUIRED_MANIFEST_FIELDS)) {
    throw new Error('SDC_REQUIRED_MANIFEST_FIELDS export is missing');
  }
  if (typeof cli.createRunnerOptions !== 'function') {
    throw new Error('createRunnerOptions export is missing');
  }
}

function validateGateYaml() {
  const yaml = require('../.aiox-core/node_modules/js-yaml');
  const gatePath = path.join(projectRoot, 'docs/qa/gates/SDC-AUTO-1-orquestracao-headless-yolo.yml');
  const gate = yaml.load(fs.readFileSync(gatePath, 'utf8'));

  if (gate.gate !== 'CONCERNS') {
    throw new Error(`Unexpected QA gate value: ${gate.gate}`);
  }
  if (gate.evidence?.tests_reviewed !== 18) {
    throw new Error('QA gate must reference the 18-test SDC suite');
  }
  if (gate.evidence?.trace?.ac_gaps?.length !== 0) {
    throw new Error('QA gate still reports AC gaps');
  }
}

function validateCliBoundary() {
  run(process.execPath, ['.aiox-core/development/scripts/sdc-headless-yolo.js', '--help'], { capture: true });
  run(
    process.execPath,
    ['.aiox-core/development/scripts/sdc-headless-yolo.js', '--manifest', 'missing.yaml'],
    {
      capture: true,
      expectFailure: true,
      expectedText: 'Refusing non-dry-run execution without --adapter-module',
    },
  );
}

async function main() {
  const mode = process.argv[2] || 'build';

  if (mode === 'lint') {
    validateSyntax();
    await validateWorkflowFiles();
    validateGateYaml();
    return;
  }

  if (mode === 'typecheck') {
    validateSyntax();
    validateExports();
    return;
  }

  if (mode === 'test') {
    run(process.execPath, ['.aiox-core/development/scripts/__tests__/sdc-headless-yolo.test.js']);
    return;
  }

  if (mode === 'build') {
    validateSyntax();
    validateExports();
    await validateWorkflowFiles();
    validateCliBoundary();
    validateGateYaml();
    return;
  }

  throw new Error(`Unknown validation mode: ${mode}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
