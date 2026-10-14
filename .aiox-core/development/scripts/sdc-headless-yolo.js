#!/usr/bin/env node
'use strict';

const path = require('path');
const yaml = require('js-yaml');
const { SdcHeadlessYoloRunner } = require('../../core/orchestration/sdc-headless-yolo-runner');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--manifest') args.manifest = argv[++i];
    else if (arg === '--resume') args.resumeRunId = argv[++i];
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--adapter-module') args.adapterModule = argv[++i];
    else if (arg === '--help' || arg === '-h') args.help = true;
  }
  return args;
}

function usage() {
  return [
    'Usage:',
    '  node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest <manifest.yaml> --dry-run',
    '  node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest <manifest.yaml> --adapter-module <adapters.js>',
    '  node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest <manifest.yaml> --resume <run-id> --adapter-module <adapters.js>',
    '',
    'Non-dry-run execution requires --adapter-module. Use --dry-run for simulated DevOps/deploy effects.',
    'The runner never prompts. Missing input produces a persisted HALT state and log.',
  ].join('\n');
}

async function loadAdapterModule(adapterModule, projectRoot) {
  const resolvedPath = path.isAbsolute(adapterModule)
    ? adapterModule
    : path.resolve(projectRoot, adapterModule);
  const loaded = require(resolvedPath);
  const adapters = typeof loaded === 'function' ? await loaded({ projectRoot }) : (loaded.adapters || loaded);

  if (!adapters || typeof adapters !== 'object' || Array.isArray(adapters)) {
    throw new Error(`Adapter module must export an adapters object: ${resolvedPath}`);
  }

  return adapters;
}

async function createRunnerOptions(args, projectRoot) {
  if (args.dryRun) {
    return {
      projectRoot,
      adapters: {
        devops: async (operation) => ({ status: 'completed', operation, simulated: true }),
      },
    };
  }

  if (!args.adapterModule) {
    throw new Error('Refusing non-dry-run execution without --adapter-module. Use --dry-run for simulated execution.');
  }

  const adapters = await loadAdapterModule(args.adapterModule, projectRoot);
  if (typeof adapters.devops !== 'function') {
    throw new Error('Adapter module must export a devops adapter function for non-dry-run execution.');
  }

  return { projectRoot, adapters };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.manifest) {
    console.log(usage());
    process.exit(args.help ? 0 : 1);
  }

  const runner = new SdcHeadlessYoloRunner(await createRunnerOptions(args, process.cwd()));

  const result = await runner.execute(args.manifest, { resumeRunId: args.resumeRunId });
  console.log(yaml.dump({
    run_id: result.run_id,
    status: result.status,
    terminal_status: result.terminal_status,
    current_phase: result.current_phase,
    execution_log: result.execution_log,
  }, { lineWidth: 120 }));

  if (result.status === 'failed' || result.status === 'blocked') {
    process.exitCode = 2;
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}

module.exports = { parseArgs, usage, loadAdapterModule, createRunnerOptions };
