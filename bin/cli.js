#!/usr/bin/env node
/**
 * FindMeSaaS installer.
 *
 * Copies the skill system, workflows, memory scaffolding and platform adapters
 * into the current project so an existing repository can use FindMeSaaS without
 * being cloned over.
 *
 * Zero runtime dependencies: Node built-ins only, so `npx find-me-saas` works on
 * a clean machine. Paths are built with `path.join` throughout, so Windows,
 * macOS and Linux behave identically.
 *
 * Note on rule 10 (no console output in production code): this file is a command
 * line interface. Its stdout IS the product, and every write below is deliberate
 * user-facing output rather than leftover debugging.
 */

import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync, readFileSync } from 'node:fs';
import { dirname, join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import process from 'node:process';

const PACKAGE_ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const VERSION = readVersion();

/** Paths copied for every platform, relative to the package root. */
const CORE_SOURCES = [
  'skills',
  'workflows',
  'tests',
  'memory/README.md',
  'memory/extra-context',
  'memory/ideas/.gitkeep',
  'memory/market_insights/README.md',
];

/** Paths copied only for the named platform. */
const PLATFORM_SOURCES = {
  claude: ['.claude', 'CLAUDE.md'],
  codex: ['.codex', 'AGENTS.md'],
  cursor: ['.cursor'],
};

/**
 * Local runtime artifacts that exist in the maintainer's working copy but are
 * not part of the product. Copying these to a user would leak local state.
 */
const EXCLUDED_NAMES = new Set([
  '__pycache__',
  'node_modules',
  'worktrees',
  'scheduled_tasks.lock',
  'settings.local.json',
  '.DS_Store',
]);

/**
 * Destination paths that hold the user's own analyses. These are never written
 * over, with or without --force, because losing them to a reinstall would
 * destroy work the tool exists to produce.
 */
const USER_DATA_PATTERNS = [
  /^memory[/\\]user_profile\.md$/,
  // Everything under ideas/ except the placeholder the installer itself ships.
  /^memory[/\\]ideas[/\\](?!\.gitkeep$).+/,
  // Research files, but not the index README the installer ships.
  /^memory[/\\]market_insights[/\\](?!README\.md$).+\.md$/,
];

/** Read the version from the package manifest, falling back if it is unreadable. */
function readVersion() {
  try {
    return JSON.parse(readFileSync(join(PACKAGE_ROOT, 'package.json'), 'utf8')).version;
  } catch {
    return '0.0.0';
  }
}

/** True when a destination path belongs to the user rather than to the tool. */
function isUserData(destRelative) {
  const normalised = destRelative.split(sep).join('/');
  return USER_DATA_PATTERNS.some((pattern) => pattern.test(normalised) || pattern.test(destRelative));
}

/** Recursively list every file under a path, or the path itself if it is a file. */
function listFiles(absolutePath) {
  if (!existsSync(absolutePath)) return [];
  if (statSync(absolutePath).isFile()) return [absolutePath];
  return readdirSync(absolutePath).flatMap((entry) => {
    if (EXCLUDED_NAMES.has(entry)) return [];
    return listFiles(join(absolutePath, entry));
  });
}

/** Parse argv into an options object; unknown flags are reported by the caller. */
function parseArgs(argv) {
  const options = { command: null, platform: 'all', force: false, dryRun: false, unknown: [] };
  for (const arg of argv) {
    if (arg === 'init') options.command = 'init';
    else if (arg === '--force' || arg === '-f') options.force = true;
    else if (arg === '--dry-run' || arg === '-n') options.dryRun = true;
    else if (arg === '--help' || arg === '-h') options.command = 'help';
    else if (arg === '--version' || arg === '-v') options.command = 'version';
    else if (arg.startsWith('--platform=')) options.platform = arg.slice('--platform='.length);
    else options.unknown.push(arg);
  }
  return options;
}

/** Print usage. */
function printHelp() {
  console.log(`
FindMeSaaS ${VERSION}
An AI venture analyst that runs in your terminal.

USAGE
  npx find-me-saas init [options]

OPTIONS
  --platform <name>   claude | codex | cursor | all     (default: all)
  --force, -f         overwrite existing tool files
  --dry-run, -n       list what would be written, change nothing
  --help, -h          show this message
  --version, -v       print the version

WHAT IT WRITES
  skills/        15 analysis skills
  workflows/     4 workflow specifications
  tests/         validation harness and fixtures
  memory/        scaffolding for your profile, research and ideas
  .claude/       commands, hooks and adapters   (--platform claude)
  .codex/        adapters                       (--platform codex)
  .cursor/       rules                          (--platform cursor)

WHAT IT NEVER TOUCHES
  memory/user_profile.md, memory/ideas/, memory/market_insights/*.md
  Your analyses are yours. A reinstall cannot destroy them.

AFTER INSTALLING
  Open the project in Claude Code, Codex or Cursor and run /founder-profile,
  or just say "validate my idea: ...".
`);
}

/**
 * Build the copy plan: every source file mapped to its destination, tagged with
 * whether it will be written, skipped as existing, or protected as user data.
 */
function buildPlan(platform, force) {
  const platforms = platform === 'all' ? Object.keys(PLATFORM_SOURCES) : [platform];
  const sources = [...CORE_SOURCES];
  for (const name of platforms) sources.push(...(PLATFORM_SOURCES[name] || []));

  const plan = [];
  for (const source of sources) {
    const absoluteSource = join(PACKAGE_ROOT, source);
    for (const file of listFiles(absoluteSource)) {
      const destRelative = relative(PACKAGE_ROOT, file);
      const destAbsolute = join(process.cwd(), destRelative);
      let action = 'write';
      if (isUserData(destRelative)) action = existsSync(destAbsolute) ? 'protected' : 'write';
      else if (existsSync(destAbsolute)) action = force ? 'overwrite' : 'skip';
      plan.push({ source: file, dest: destAbsolute, rel: destRelative, action });
    }
  }
  return plan;
}

/** Execute a copy plan, creating parent directories as needed. */
function apply(plan) {
  for (const item of plan) {
    if (item.action === 'skip' || item.action === 'protected') continue;
    mkdirSync(dirname(item.dest), { recursive: true });
    copyFileSync(item.source, item.dest);
  }
}

/** Print a grouped summary of what happened, or would happen. */
function report(plan, dryRun) {
  const counts = { write: 0, overwrite: 0, skip: 0, protected: 0 };
  for (const item of plan) counts[item.action] += 1;

  const verb = dryRun ? 'would write' : 'wrote';
  console.log(`\nFindMeSaaS ${VERSION} -> ${process.cwd()}\n`);

  const written = plan.filter((i) => i.action === 'write' || i.action === 'overwrite');
  const topLevel = [...new Set(written.map((i) => i.rel.split(sep)[0]))].sort();
  for (const group of topLevel) {
    const n = written.filter((i) => i.rel.split(sep)[0] === group).length;
    console.log(`  ${verb.padEnd(11)} ${group.padEnd(18)} ${n} file${n === 1 ? '' : 's'}`);
  }

  if (counts.skip) console.log(`\n  skipped ${counts.skip} existing file(s). Use --force to overwrite.`);

  const settingsSkipped = plan.some(
    (i) => i.action === 'skip' && i.rel.split(sep).join('/') === '.claude/settings.json'
  );
  if (settingsSkipped) {
    console.log(`
  NOTE: you already have .claude/settings.json, so it was left alone and the
  hooks were not installed. To enable them, merge this into that file:

    "hooks": {
      "SessionStart": [{ "matcher": "startup|resume", "hooks": [
        { "type": "command", "command": "python \"\${CLAUDE_PROJECT_DIR}/.claude/hooks/session_start.py\"", "timeout": 10 }]}],
      "PostToolUse": [{ "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "python \"\${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea.py\"", "timeout": 30 }]}]
    }`);
  }
  if (counts.protected) {
    console.log(`  protected ${counts.protected} file(s) of your own analyses; these are never overwritten:`);
    for (const item of plan.filter((i) => i.action === 'protected').slice(0, 5)) {
      console.log(`      ${item.rel}`);
    }
  }

  if (dryRun) {
    console.log('\n  Dry run. Nothing was written.\n');
    return;
  }
  console.log(`
  Done. Next:
    1. Open this folder in Claude Code, Codex or Cursor.
    2. Run /founder-profile to set up your builder profile.
    3. Or just say: "validate my idea: <your idea>"

  Commands: /find-idea /validate-idea /gut-check /market-scan
            /pivot-idea /auto-pilot /idea-status /verify-memory
`);
}

/** Entry point. */
function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.unknown.length) {
    console.error(`Unknown argument: ${options.unknown[0]}\nRun "npx find-me-saas --help" for usage.`);
    process.exit(1);
  }
  if (options.command === 'version') {
    console.log(VERSION);
    return;
  }
  if (options.command !== 'init') {
    printHelp();
    return;
  }
  if (!['all', ...Object.keys(PLATFORM_SOURCES)].includes(options.platform)) {
    console.error(`Unknown platform "${options.platform}". Expected: claude, codex, cursor, or all.`);
    process.exit(1);
  }

  const plan = buildPlan(options.platform, options.force);
  if (plan.length === 0) {
    console.error('Nothing to install. The package looks incomplete; try reinstalling it.');
    process.exit(1);
  }
  if (!options.dryRun) apply(plan);
  report(plan, options.dryRun);
}

main();
