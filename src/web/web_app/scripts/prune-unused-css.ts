#!/usr/bin/env tsx
/**
 * prune-unused-css.ts
 *
 * Strategy:
 * 1. Compile each .svelte file with Svelte to collect css-unused-selector warnings.
 * 2. If none found for a file, run a conservative static analysis to detect unused
 *    simple class selectors (single-class rules) and remove those whose class name
 *    never appears in markup (class="..." or class:directive).
 *
 * Only removes entire CSS rules where ALL selectors in the rule appear unused.
 * Does NOT attempt to edit combined / descendant / attribute / id / global rules.
 *
 * CAUTION: Commit or stash before running.
 */
import fg from 'fast-glob';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { compile } from 'svelte/compiler';

interface UnusedSelectorWarning {
	file: string;
	selector: string;
}
interface SvelteWarning {
	code: string;
	message: string;
}

function extractUnusedSelectors(file: string, source: string): UnusedSelectorWarning[] {
	const { warnings } = compile(source, { filename: file, dev: true }) as unknown as {
		warnings: SvelteWarning[];
	};
	return warnings
		.filter((w) => w.code === 'css-unused-selector')
		.map((w) => {
			const match = /Unused CSS selector "([^"]+)"/.exec(w.message);
			return match ? { file, selector: match[1] } : null;
		})
		.filter((x): x is UnusedSelectorWarning => Boolean(x));
}

function escapeForRegex(sel: string) {
	return sel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function removeSelectorsFromSource(source: string, selectors: string[]): string {
	if (!selectors.length) return source;
	let updated = source;
	for (const sel of selectors) {
		const esc = escapeForRegex(sel.trim());
		// Build pattern without unnecessary escapes flagged by ESLint
		const ruleRegex = new RegExp('(^|\n)\\s*' + esc + '\\s*\\{[\\s\\S]*?\\}', 'g');
		updated = updated.replace(ruleRegex, '\n');
	}
	return updated;
}

// Static fallback: find unused simple class selectors inside <style> blocks
function staticFindUnused(source: string): string[] {
	const used = new Set<string>();
	// class="..."
	const classAttrRegex = /class\s*=\s*"([^"]*)"/g;
	let match: RegExpExecArray | null;
	while ((match = classAttrRegex.exec(source))) {
		const classesRaw = match[1] || '';
		classesRaw
			.split(/\s+/)
			.filter(Boolean)
			.forEach((c) => used.add(c));
	}
	// class:foo directives
	const classDirRegex = /class:([a-zA-Z0-9_-]+)/g;
	while ((match = classDirRegex.exec(source))) {
		const cls = match[1];
		if (cls) used.add(cls);
	}

	// Extract style blocks
	const unused: string[] = [];
	const styleBlockRegex = /<style[^>]*>([\s\S]*?)<\/style>/g;
	let sb: RegExpExecArray | null;
	while ((sb = styleBlockRegex.exec(source))) {
		const css = sb[1] || '';
		const ruleRegex = /([^{}@][^{}]*?)\{[^{}]*?\}/g; // skip @ rules
		let rr: RegExpExecArray | null;
		while ((rr = ruleRegex.exec(css))) {
			const rawSel = rr[1] || '';
			const selectorList = rawSel.trim();
			if (!selectorList) continue;
			const selectors = selectorList.split(',').map((s) => s.trim());
			// Only consider rules composed solely of simple class selectors (optionally with pseudo)
			if (!selectors.every((s) => /^\.[a-zA-Z0-9_-]+(:{1,2}[a-zA-Z0-9_-]+)?$/.test(s)))
				continue;
			const baseClasses = selectors.map((s) =>
				s.replace(/:(:{0,1})[a-zA-Z0-9_-]+$/, '').slice(1)
			);
			if (baseClasses.every((c) => !used.has(c))) {
				// all unused
				selectors.forEach((s) => unused.push(s));
			}
		}
	}
	return unused;
}

async function main() {
	const files = await fg(['src/**/*.svelte'], { dot: false });
	const allWarnings: Record<string, Set<string>> = {};

	// First pass: collect unused selectors via compiler
	for (const file of files) {
		const full = join(process.cwd(), file);
		const src = readFileSync(full, 'utf8');
		const warnings = extractUnusedSelectors(full, src);
		for (const w of warnings) {
			allWarnings[file] = allWarnings[file] || new Set();
			allWarnings[file].add(w.selector.trim());
		}
		// If no compiler warnings for this file, attempt static fallback for simple class rules
		if (!warnings.length) {
			const statics = staticFindUnused(src);
			if (statics.length) {
				allWarnings[file] = allWarnings[file] || new Set();
				const setRef2 = allWarnings[file];
				if (setRef2) statics.forEach((s) => setRef2.add(s));
			}
		}
	}

	// Second pass: apply removals
	const summary: { file: string; removed: string[] }[] = [];
	for (const [file, sels] of Object.entries(allWarnings)) {
		if (!sels.size) continue;
		const full = join(process.cwd(), file);
		const src = readFileSync(full, 'utf8');
		const before = src;
		const after = removeSelectorsFromSource(src, Array.from(sels));
		if (after !== before) {
			writeFileSync(full, after, 'utf8');
			summary.push({ file, removed: Array.from(sels) });
		}
	}

	if (!summary.length) {
		console.log('No unused selectors removed.');
		return;
	}
	console.log('Removed unused selectors:');
	for (const s of summary) {
		console.log(`\n${s.file}`);
		for (const sel of s.removed) console.log('  - ' + sel);
	}
	console.log('\nDone. Review diffs to ensure no unintended deletions.');
}

main().catch((err) => {
	console.error(err);
	process.exit(1);
});
