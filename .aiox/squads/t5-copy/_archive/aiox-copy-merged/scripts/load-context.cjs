#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const runtimePaths = require('./runtime-paths.cjs');
const { resolveSquadWorkspaceReadiness } = require('../../workspace-governance-legacy/scripts/resolve-squad-workspace-readiness.cjs');
function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    business: null,
    product: null,
    campaignSlug: null,
    task: null,
    format: 'json',
  };

  for (const raw of argv) {
    if (raw.startsWith('--business=')) {
      args.business = raw.slice('--business='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--product=')) {
      args.product = raw.slice('--product='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--campaign-slug=')) {
      args.campaignSlug = raw.slice('--campaign-slug='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--campaign=')) {
      args.campaignSlug = raw.slice('--campaign='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--task=')) {
      args.task = raw.slice('--task='.length).trim() || null;
      continue;
    }
    if (raw.startsWith('--format=')) {
      args.format = raw.slice('--format='.length).trim() || 'json';
    }
  }

  return args;
}

function readSessionContext() {
  const sessionPath = runtimePaths.getCopySessionContextPath();
  if (!fs.existsSync(sessionPath)) {
    fail(`Copy session context not found: ${runtimePaths.toWorkspaceRelative(sessionPath)}. Run node squads/aiox-copy/scripts/set-active-context.cjs --product=<slug>.`);
  }

  const payload = yaml.load(fs.readFileSync(sessionPath, 'utf8')) || {};
  const active = payload.active_context || {};
  if (!active.business_slug || !active.product_slug) {
    fail(`Invalid copy session context: missing active_context.business_slug or active_context.product_slug in ${runtimePaths.toWorkspaceRelative(sessionPath)}`);
  }

  return {
    sessionPath,
    businessSlug: String(active.business_slug).trim(),
    productSlug: String(active.product_slug).trim(),
    campaignSlug: typeof active.campaign_slug === 'string' && active.campaign_slug.trim() !== '' ? active.campaign_slug.trim() : null,
    assetType: typeof active.asset_type === 'string' && active.asset_type.trim() !== '' ? active.asset_type.trim() : null,
  };
}

function workspacePath(...parts) {
  return path.join(runtimePaths.WORKSPACE_ROOT, ...parts);
}

function getCampaignArtifacts(business, campaignSlug) {
  if (!campaignSlug) {
    return {
      status: 'not_set',
      root: null,
      files: [],
      missing_required: [],
    };
  }

  const campaignRoot = workspacePath('workspace', 'businesses', business, 'copy', campaignSlug);
  const fileCandidates = [
    'campaign-brief.yaml',
    'message-architecture.yaml',
    'creative-brief.yaml',
  ];
  const files = fileCandidates
    .map((file) => path.join(campaignRoot, file))
    .filter((file) => fs.existsSync(file))
    .map((file) => runtimePaths.toWorkspaceRelative(file));

  const assetsRoot = path.join(campaignRoot, 'assets');
  if (fs.existsSync(assetsRoot) && fs.statSync(assetsRoot).isDirectory()) {
    const assetFiles = fs.readdirSync(assetsRoot)
      .filter((entry) => entry.endsWith('.yaml') || entry.endsWith('.yml'))
      .sort()
      .map((entry) => runtimePaths.toWorkspaceRelative(path.join(assetsRoot, entry)));
    files.push(...assetFiles);
  }

  const requiredCampaignBrief = path.join(campaignRoot, 'campaign-brief.yaml');
  return {
    status: fs.existsSync(requiredCampaignBrief) ? 'ready' : 'missing_campaign_brief',
    root: runtimePaths.toWorkspaceRelative(campaignRoot),
    files,
    missing_required: fs.existsSync(requiredCampaignBrief)
      ? []
      : [runtimePaths.toWorkspaceRelative(requiredCampaignBrief)],
  };
}

function deriveOperationalBriefStatus(productReadiness, campaignArtifacts, campaignSlug) {
  if (productReadiness.status !== 'ready') {
    return {
      status: productReadiness.status,
      final_allowed: false,
      notes: productReadiness.reasons || [],
    };
  }

  if (!campaignSlug) {
    return {
      status: 'product_ready_draft_only',
      final_allowed: false,
      notes: ['Product context is ready, but campaign context is not set. FINAL promotion remains blocked.'],
    };
  }

  if (campaignArtifacts.status !== 'ready') {
    return {
      status: 'campaign_context_incomplete',
      final_allowed: false,
      notes: ['Campaign slug is set, but campaign-brief.yaml is missing. FINAL promotion remains blocked.'],
    };
  }

  return {
    status: 'ready_for_campaign_execution',
    final_allowed: true,
    notes: ['Product and campaign context are ready. FINAL promotion may proceed after review gates.'],
  };
}

function buildOutput(args) {
  const session = readSessionContext();
  const business = args.business || session.businessSlug;
  const product = args.product || session.productSlug;
  const campaignSlug = args.campaignSlug || session.campaignSlug;
  const cooReadiness = resolveSquadWorkspaceReadiness({
    squad: 'copy',
    business,
    product,
    contextType: 'product',
  });
  const readiness = cooReadiness.readiness_payload;

  const sharedFiles = readiness.requirements.filter((item) =>
    ['icp', 'brand', 'brandbook', 'positioning'].includes(item.id) && item.exists
  );
  const productFiles = readiness.requirements.filter((item) =>
    !['icp', 'brand', 'brandbook', 'positioning', 'pricing', 'product_structure'].includes(item.id) && item.exists
  );
  const campaignArtifacts = getCampaignArtifacts(business, campaignSlug);
  const operationalBrief = deriveOperationalBriefStatus(readiness, campaignArtifacts, campaignSlug);

  return {
    task: args.task || null,
    consumer: 'copy',
    business_slug: business,
    product_slug: product,
    campaign_slug: campaignSlug,
    asset_type: session.assetType,
    coo_readiness: {
      owner: cooReadiness.owner,
      status: cooReadiness.status,
      reason: cooReadiness.reason,
      canonical_config_paths: cooReadiness.canonical_config_paths,
    },
    readiness: {
      status: readiness.status,
      reasons: readiness.reasons,
      missing_required: readiness.missing_required.map((item) => ({
        id: item.id,
        path: item.path,
      })),
      compliance_audit: readiness.compliance_audit,
    },
    operational_brief: {
      status: operationalBrief.status,
      final_allowed: operationalBrief.final_allowed,
      notes: operationalBrief.notes,
    },
    campaign_context: {
      status: campaignArtifacts.status,
      root: campaignArtifacts.root,
      missing_required: campaignArtifacts.missing_required,
      promotion_rule: 'Strategic or FINAL work requires persisted campaign artifacts.',
    },
    session_context_path: runtimePaths.toWorkspaceRelative(session.sessionPath),
    company_offerbook_index: readiness.company_offerbook_index,
    resolved_paths: {
      shared_files: sharedFiles.map((item) => item.path),
      product_files: productFiles.map((item) => item.path),
      structure_source: readiness.requirements.find((item) => item.id === 'product_structure' && item.exists)?.path || null,
      pricing_source: readiness.requirements.find((item) => item.id === 'pricing' && item.exists)?.path || null,
      company_narrative_files: readiness.narrative_files?.company || [],
      product_narrative_files: readiness.narrative_files?.product || [],
      campaign_files: campaignArtifacts.files,
    },
  };
}

function printOutput(output, format) {
  if (format === 'yaml') {
    process.stdout.write(yaml.dump(output, { lineWidth: 120, noRefs: true, sortKeys: false }));
    return;
  }
  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const output = buildOutput(args);
  printOutput(output, args.format);
}

if (require.main === module) {
  main();
}

module.exports = {
  buildOutput,
};
