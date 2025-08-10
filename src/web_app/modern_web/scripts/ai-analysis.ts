/**
 * AI Implementation Analysis Script
 *
 * This script analyzes the modern pictograph implementation and provides
 * comprehensive feedback on architecture, potential issues, and code quality.
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

interface AnalysisResult {
	category: string;
	status: 'success' | 'warning' | 'error';
	message: string;
	details?: string[];
	recommendations?: string[];
}

interface FileInfo {
	path: string;
	size: number;
	lines: number;
	content: string;
}

class PictographImplementationAnalyzer {
	private results: AnalysisResult[] = [];
	private files: FileInfo[] = [];

	constructor(private basePath: string) {}

	async analyze(): Promise<AnalysisResult[]> {
		console.log('🔍 Starting AI Analysis of Modern Pictograph Implementation...\n');

		// Load all relevant files
		this.loadFiles();

		// Run analysis categories
		this.analyzeArchitecture();
		this.analyzeRunesUsage();
		this.analyzeDataFlow();
		this.analyzeComponentStructure();
		this.analyzeTestCoverage();
		this.analyzePerformance();
		this.analyzeErrorHandling();
		this.analyzeAccessibility();
		this.analyzeMaintainability();
		this.analyzeIntegration();

		// Print results
		this.printResults();

		return this.results;
	}

	private loadFiles(): void {
		const extensions = ['.svelte', '.ts', '.js'];
		const paths = [
			'src/lib/components/pictograph',
			'src/lib/services',
			'src/lib/components/workbench',
			'src/lib/components/demo',
		];

		for (const relativePath of paths) {
			const fullPath = join(this.basePath, relativePath);
			if (this.pathExists(fullPath)) {
				this.loadFilesRecursive(fullPath, extensions);
			}
		}

		this.addResult(
			'File Loading',
			'success',
			`Loaded ${this.files.length} implementation files for analysis`,
			this.files.map((f) => `${f.path} (${f.lines} lines)`)
		);
	}

	private loadFilesRecursive(dirPath: string, extensions: string[]): void {
		try {
			const items = readdirSync(dirPath);

			for (const item of items) {
				const fullPath = join(dirPath, item);
				const stat = statSync(fullPath);

				if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
					this.loadFilesRecursive(fullPath, extensions);
				} else if (stat.isFile() && extensions.some((ext) => item.endsWith(ext))) {
					const content = readFileSync(fullPath, 'utf8');
					const lines = content.split('\n').length;

					this.files.push({
						path: fullPath.replace(this.basePath, '').replace(/\\\\/g, '/'),
						size: stat.size,
						lines,
						content,
					});
				}
			}
		} catch (error) {
			// Directory doesn't exist or can't be read
		}
	}

	private pathExists(path: string): boolean {
		try {
			statSync(path);
			return true;
		} catch {
			return false;
		}
	}

	private analyzeArchitecture(): void {
		const svelteFiles = this.files.filter((f) => f.path.endsWith('.svelte'));
		const tsFiles = this.files.filter((f) => f.path.endsWith('.ts'));

		// Check for proper separation of concerns
		const hasComponents = svelteFiles.some((f) => f.path.includes('/components/pictograph/'));
		const hasServices = tsFiles.some((f) => f.path.includes('/services/'));
		const hasDataAdapters = tsFiles.some((f) => f.path.includes('dataAdapter'));

		if (hasComponents && hasServices && hasDataAdapters) {
			this.addResult(
				'Architecture',
				'success',
				'Clean separation of concerns with proper layering',
				[
					'✓ Component layer (Svelte components)',
					'✓ Service layer (TypeScript services)',
					'✓ Data adaptation layer (Bridge functions)',
					'✓ Clear dependency flow',
				]
			);
		} else {
			this.addResult('Architecture', 'warning', 'Missing some architectural layers', [
				`Components: ${hasComponents ? '✓' : '✗'}`,
				`Services: ${hasServices ? '✓' : '✗'}`,
				`Data Adapters: ${hasDataAdapters ? '✓' : '✗'}`,
			]);
		}

		// Check for circular dependencies
		this.analyzeCircularDependencies();
	}

	private analyzeRunesUsage(): void {
		const svelteFiles = this.files.filter((f) => f.path.endsWith('.svelte'));
		const runesUsage = {
			state: 0,
			derived: 0,
			effect: 0,
			stores: 0,
		};

		const issuesFound: string[] = [];

		for (const file of svelteFiles) {
			// Count runes usage
			runesUsage.state += (file.content.match(/\$state/g) || []).length;
			runesUsage.derived += (file.content.match(/\$derived/g) || []).length;
			runesUsage.effect += (file.content.match(/\$effect/g) || []).length;

			// Check for old store usage (should be avoided)
			const storeUsage = file.content.match(/import.*from 'svelte\/store'/g);
			if (storeUsage) {
				runesUsage.stores += storeUsage.length;
				issuesFound.push(`${file.path}: Uses legacy stores instead of runes`);
			}

			// Check for proper runes patterns
			if (file.content.includes('let ') && file.content.includes('$state')) {
				const properStatePattern = /let\\s+\\w+\\s*=\\s*\\$state/g;
				const stateDeclarations = file.content.match(properStatePattern) || [];

				if (stateDeclarations.length === 0 && file.content.includes('$state')) {
					issuesFound.push(`${file.path}: Potential improper $state usage pattern`);
				}
			}
		}

		const status = issuesFound.length === 0 ? 'success' : 'warning';
		const message =
			issuesFound.length === 0
				? 'Excellent Svelte 5 runes adoption'
				: 'Some runes usage issues detected';

		this.addResult('Svelte 5 Runes', status, message, [
			`$state usage: ${runesUsage.state} instances`,
			`$derived usage: ${runesUsage.derived} instances`,
			`$effect usage: ${runesUsage.effect} instances`,
			`Legacy stores: ${runesUsage.stores} instances`,
			...issuesFound,
		]);
	}

	private analyzeDataFlow(): void {
		const adapterFile = this.files.find((f) => f.path.includes('dataAdapter'));

		if (!adapterFile) {
			this.addResult('Data Flow', 'error', 'Missing data adapter layer');
			return;
		}

		// Check for proper conversion functions
		const hasLegacyToModern = adapterFile.content.includes('legacyToModernPictographData');
		const hasModernToLegacy = adapterFile.content.includes('modernToLegacyPictographData');
		const hasEnsureModern = adapterFile.content.includes('ensureModernPictographData');
		const hasBeatExtraction = adapterFile.content.includes('beatDataToPictographData');

		const conversionScore = [
			hasLegacyToModern,
			hasModernToLegacy,
			hasEnsureModern,
			hasBeatExtraction,
		].filter(Boolean).length;

		if (conversionScore === 4) {
			this.addResult(
				'Data Flow',
				'success',
				'Comprehensive data conversion layer implemented',
				[
					'✓ Legacy to modern conversion',
					'✓ Modern to legacy conversion',
					'✓ Auto-detection and conversion',
					'✓ Beat data extraction',
				]
			);
		} else {
			this.addResult('Data Flow', 'warning', 'Incomplete data conversion coverage', [
				`Legacy to modern: ${hasLegacyToModern ? '✓' : '✗'}`,
				`Modern to legacy: ${hasModernToLegacy ? '✓' : '✗'}`,
				`Auto-detection: ${hasEnsureModern ? '✓' : '✗'}`,
				`Beat extraction: ${hasBeatExtraction ? '✓' : '✗'}`,
			]);
		}
	}

	private analyzeComponentStructure(): void {
		const componentFiles = this.files.filter(
			(f) => f.path.includes('/components/pictograph/') && f.path.endsWith('.svelte')
		);

		const expectedComponents = [
			'ModernPictograph.svelte',
			'Grid.svelte',
			'Prop.svelte',
			'Arrow.svelte',
			'TKAGlyph.svelte',
		];

		const foundComponents = expectedComponents.filter((expected) =>
			componentFiles.some((f) => f.path.includes(expected))
		);

		const completeness = foundComponents.length / expectedComponents.length;

		// Analyze component quality
		const qualityIssues: string[] = [];

		for (const component of componentFiles) {
			// Check for proper props interface
			if (!component.content.includes('interface Props')) {
				qualityIssues.push(`${component.path}: Missing Props interface`);
			}

			// Check for proper event handling
			if (component.content.includes('onclick') && !component.content.includes('onkeydown')) {
				qualityIssues.push(`${component.path}: Missing keyboard accessibility`);
			}

			// Check for error handling
			if (!component.content.includes('catch') && !component.content.includes('error')) {
				qualityIssues.push(`${component.path}: Limited error handling`);
			}

			// Check for proper runes usage in components
			if (
				component.content.includes('export let') &&
				!component.content.includes('$props') &&
				!component.content.includes('$state')
			) {
				qualityIssues.push(`${component.path}: Not using Svelte 5 props pattern`);
			}
		}

		const status =
			completeness === 1 && qualityIssues.length === 0
				? 'success'
				: completeness >= 0.8 && qualityIssues.length <= 2
					? 'warning'
					: 'error';

		this.addResult(
			'Component Structure',
			status,
			`${Math.round(completeness * 100)}% component completeness`,
			[
				`Found components: ${foundComponents.join(', ')}`,
				`Missing: ${expectedComponents.filter((e) => !foundComponents.includes(e)).join(', ') || 'None'}`,
				`Quality issues: ${qualityIssues.length}`,
				...qualityIssues,
			]
		);
	}

	private analyzeTestCoverage(): void {
		const testFiles = this.files.filter(
			(f) => f.path.includes('test') || f.path.includes('spec')
		);
		const sourceFiles = this.files.filter(
			(f) =>
				!f.path.includes('test') &&
				!f.path.includes('spec') &&
				(f.path.endsWith('.svelte') || f.path.endsWith('.ts'))
		);

		const testTypes = {
			unit: testFiles.filter((f) => f.path.includes('.test.ts')).length,
			integration: testFiles.filter((f) => f.path.includes('.integration.test.ts')).length,
			e2e: testFiles.filter((f) => f.path.includes('.e2e.test.ts')).length,
		};

		const coverage = testFiles.length / Math.max(sourceFiles.length, 1);

		// Analyze test quality
		const testQuality: string[] = [];

		for (const testFile of testFiles) {
			if (testFile.content.includes('describe') && testFile.content.includes('it')) {
				testQuality.push(`${testFile.path}: Proper test structure`);
			}

			if (testFile.content.includes('expect')) {
				testQuality.push(`${testFile.path}: Has assertions`);
			}

			if (testFile.content.includes('mock')) {
				testQuality.push(`${testFile.path}: Uses mocking`);
			}
		}

		const status = coverage >= 0.8 ? 'success' : coverage >= 0.5 ? 'warning' : 'error';

		this.addResult(
			'Test Coverage',
			status,
			`${Math.round(coverage * 100)}% test coverage ratio`,
			[
				`Unit tests: ${testTypes.unit}`,
				`Integration tests: ${testTypes.integration}`,
				`E2E tests: ${testTypes.e2e}`,
				`Total test files: ${testFiles.length}`,
				`Source files: ${sourceFiles.length}`,
				...testQuality.slice(0, 5), // Show first 5 quality indicators
			]
		);
	}

	private analyzePerformance(): void {
		const issues: string[] = [];
		const optimizations: string[] = [];

		for (const file of this.files) {
			// Check for potential performance issues
			if (file.content.includes('JSON.parse(JSON.stringify')) {
				issues.push(`${file.path}: Deep cloning with JSON (performance risk)`);
			}

			if (file.content.includes('new Promise') && file.content.includes('setTimeout')) {
				issues.push(`${file.path}: Manual promise delays (consider alternatives)`);
			}

			// Check for performance optimizations
			if (file.content.includes('$derived')) {
				optimizations.push(`${file.path}: Uses reactive derivations`);
			}

			if (file.content.includes('cache') || file.content.includes('memoiz')) {
				optimizations.push(`${file.path}: Implements caching`);
			}

			if (file.content.includes('lazy') || file.content.includes('defer')) {
				optimizations.push(`${file.path}: Uses lazy loading`);
			}
		}

		const status = issues.length === 0 ? 'success' : issues.length <= 2 ? 'warning' : 'error';

		this.addResult(
			'Performance',
			status,
			`${issues.length} potential performance issues found`,
			['Issues:', ...issues, 'Optimizations:', ...optimizations]
		);
	}

	private analyzeErrorHandling(): void {
		const errorPatterns = {
			tryCatch: 0,
			errorStates: 0,
			fallbacks: 0,
			errorBoundaries: 0,
		};

		const issues: string[] = [];

		for (const file of this.files) {
			errorPatterns.tryCatch += (file.content.match(/try\\s*{[^}]*catch/g) || []).length;
			errorPatterns.errorStates += (
				file.content.match(/error.*state|state.*error/gi) || []
			).length;
			errorPatterns.fallbacks += (file.content.match(/fallback|default/gi) || []).length;

			// Check for unhandled async operations
			if (file.content.includes('async') && !file.content.includes('catch')) {
				issues.push(`${file.path}: Async operations without error handling`);
			}

			// Check for fetch without error handling
			if (file.content.includes('fetch(') && !file.content.includes('.catch')) {
				issues.push(`${file.path}: Fetch calls may lack error handling`);
			}
		}

		const totalErrorHandling = Object.values(errorPatterns).reduce((a, b) => a + b, 0);
		const status =
			totalErrorHandling >= 10 && issues.length === 0
				? 'success'
				: totalErrorHandling >= 5 && issues.length <= 2
					? 'warning'
					: 'error';

		this.addResult(
			'Error Handling',
			status,
			`${totalErrorHandling} error handling patterns found`,
			[
				`Try-catch blocks: ${errorPatterns.tryCatch}`,
				`Error states: ${errorPatterns.errorStates}`,
				`Fallback patterns: ${errorPatterns.fallbacks}`,
				`Issues found: ${issues.length}`,
				...issues,
			]
		);
	}

	private analyzeAccessibility(): void {
		const a11yFeatures = {
			ariaLabels: 0,
			roleAttributes: 0,
			keyboardHandling: 0,
			focusManagement: 0,
		};

		const issues: string[] = [];

		for (const file of this.files.filter((f) => f.path.endsWith('.svelte'))) {
			a11yFeatures.ariaLabels += (file.content.match(/aria-label/g) || []).length;
			a11yFeatures.roleAttributes += (file.content.match(/role=/g) || []).length;
			a11yFeatures.keyboardHandling += (
				file.content.match(/onkey|keydown|keypress/g) || []
			).length;
			a11yFeatures.focusManagement += (file.content.match(/focus|tabindex/g) || []).length;

			// Check for missing alt text on images
			if (file.content.includes('<image') && !file.content.includes('aria-label')) {
				issues.push(`${file.path}: Image elements may lack accessibility labels`);
			}

			// Check for interactive elements without keyboard support
			if (file.content.includes('onclick') && !file.content.includes('onkey')) {
				issues.push(`${file.path}: Interactive elements may lack keyboard support`);
			}
		}

		const totalA11y = Object.values(a11yFeatures).reduce((a, b) => a + b, 0);
		const status =
			totalA11y >= 15 && issues.length === 0
				? 'success'
				: totalA11y >= 8 && issues.length <= 3
					? 'warning'
					: 'error';

		this.addResult('Accessibility', status, `${totalA11y} accessibility features implemented`, [
			`ARIA labels: ${a11yFeatures.ariaLabels}`,
			`Role attributes: ${a11yFeatures.roleAttributes}`,
			`Keyboard handling: ${a11yFeatures.keyboardHandling}`,
			`Focus management: ${a11yFeatures.focusManagement}`,
			`Issues: ${issues.length}`,
			...issues,
		]);
	}

	private analyzeMaintainability(): void {
		const metrics = {
			avgFileSize: 0,
			avgComplexity: 0,
			duplicateCode: 0,
			documentation: 0,
		};

		const largeFiles: string[] = [];
		const complexFunctions: string[] = [];
		const documentation: string[] = [];

		for (const file of this.files) {
			// File size analysis
			if (file.lines > 500) {
				largeFiles.push(`${file.path}: ${file.lines} lines`);
			}

			// Complexity analysis (rough estimate)
			const complexity = (file.content.match(/if|for|while|switch|catch/g) || []).length;
			if (complexity > 20) {
				complexFunctions.push(`${file.path}: ${complexity} complexity points`);
			}

			// Documentation analysis
			const comments = (
				file.content.match(/\/\*\*[^*]*\*+(?:[^/*][^*]*\*+)*\/|<!--[^>]*-->/g) || []
			).length;
			if (comments > 0) {
				documentation.push(`${file.path}: ${comments} doc blocks`);
			}
		}

		metrics.avgFileSize = this.files.reduce((sum, f) => sum + f.lines, 0) / this.files.length;
		metrics.documentation = documentation.length;

		const status =
			largeFiles.length === 0 && complexFunctions.length <= 1
				? 'success'
				: largeFiles.length <= 2 && complexFunctions.length <= 3
					? 'warning'
					: 'error';

		this.addResult(
			'Maintainability',
			status,
			`Average file size: ${Math.round(metrics.avgFileSize)} lines`,
			[
				`Large files (>500 lines): ${largeFiles.length}`,
				`Complex files (>20 complexity): ${complexFunctions.length}`,
				`Documented files: ${metrics.documentation}`,
				...largeFiles,
				...complexFunctions.slice(0, 3),
			]
		);
	}

	private analyzeIntegration(): void {
		const integrationPoints = {
			dataAdapters: false,
			serviceLayer: false,
			componentProps: false,
			eventHandling: false,
			stateManagement: false,
		};

		const issues: string[] = [];

		// Check for data adapter integration
		const hasDataAdapter = this.files.some(
			(f) =>
				f.path.includes('dataAdapter') && f.content.includes('ensureModernPictographData')
		);
		integrationPoints.dataAdapters = hasDataAdapter;

		// Check for service integration
		const hasServiceIntegration = this.files.some(
			(f) => f.content.includes('PictographService') || f.content.includes('beatFrameService')
		);
		integrationPoints.serviceLayer = hasServiceIntegration;

		// Check for proper prop passing
		const hasProperProps = this.files.some(
			(f) => f.path.endsWith('.svelte') && f.content.includes('interface Props')
		);
		integrationPoints.componentProps = hasProperProps;

		// Check for event handling integration
		const hasEventHandling = this.files.some(
			(f) => f.content.includes('onClick') || f.content.includes('onLoaded')
		);
		integrationPoints.eventHandling = hasEventHandling;

		// Check for state management integration
		const hasStateManagement = this.files.some(
			(f) => f.content.includes('$state') || f.content.includes('$derived')
		);
		integrationPoints.stateManagement = hasStateManagement;

		const integrationScore = Object.values(integrationPoints).filter(Boolean).length;

		if (!hasDataAdapter) {
			issues.push('Missing data adapter integration');
		}
		if (!hasServiceIntegration) {
			issues.push('Limited service layer integration');
		}

		const status =
			integrationScore >= 4 ? 'success' : integrationScore >= 3 ? 'warning' : 'error';

		this.addResult('Integration', status, `${integrationScore}/5 integration points covered`, [
			`Data adapters: ${integrationPoints.dataAdapters ? '✓' : '✗'}`,
			`Service layer: ${integrationPoints.serviceLayer ? '✓' : '✗'}`,
			`Component props: ${integrationPoints.componentProps ? '✓' : '✗'}`,
			`Event handling: ${integrationPoints.eventHandling ? '✓' : '✗'}`,
			`State management: ${integrationPoints.stateManagement ? '✓' : '✗'}`,
			...issues,
		]);
	}

	private analyzeCircularDependencies(): void {
		// Simple circular dependency detection
		const imports = new Map<string, string[]>();

		for (const file of this.files) {
			const fileImports =
				file.content
					.match(/import.*from ['"][^'"]*['"]/g)
					?.map((imp) => imp.match(/from ['"]([^'"]*)['"]/)?.[1])
					.filter((item): item is string => Boolean(item)) || [];

			imports.set(file.path, fileImports);
		}

		// Check for obvious circular references
		const circularDeps: string[] = [];
		for (const [file, deps] of imports) {
			for (const dep of deps) {
				const depImports = imports.get(dep) || [];
				if (
					depImports.some((d) =>
						d.includes(file.split('/').pop()?.replace('.ts', '') || '')
					)
				) {
					circularDeps.push(`${file} ↔ ${dep}`);
				}
			}
		}

		if (circularDeps.length === 0) {
			this.addResult('Circular Dependencies', 'success', 'No circular dependencies detected');
		} else {
			this.addResult(
				'Circular Dependencies',
				'warning',
				`${circularDeps.length} potential circular dependencies`,
				circularDeps
			);
		}
	}

	private addResult(
		category: string,
		status: 'success' | 'warning' | 'error',
		message: string,
		details?: string[],
		recommendations?: string[]
	): void {
		const result: AnalysisResult = { category, status, message };
		if (details && details.length) result.details = details;
		if (recommendations && recommendations.length) result.recommendations = recommendations;
		this.results.push(result);
	}

	private printResults(): void {
		console.log('\\n📊 AI ANALYSIS RESULTS\\n');
		console.log('='.repeat(80));

		const statusIcons = {
			success: '✅',
			warning: '⚠️ ',
			error: '❌',
		};

		const statusCounts = { success: 0, warning: 0, error: 0 };

		for (const result of this.results) {
			statusCounts[result.status]++;

			console.log(`\\n${statusIcons[result.status]} ${result.category}: ${result.message}`);

			if (result.details && result.details.length > 0) {
				result.details.forEach((detail) => console.log(`   ${detail}`));
			}

			if (result.recommendations && result.recommendations.length > 0) {
				console.log('   Recommendations:');
				result.recommendations.forEach((rec) => console.log(`   • ${rec}`));
			}
		}

		console.log('\\n' + '='.repeat(80));
		console.log('\\n📈 SUMMARY:');
		console.log(`✅ Success: ${statusCounts.success}`);
		console.log(`⚠️  Warning: ${statusCounts.warning}`);
		console.log(`❌ Error: ${statusCounts.error}`);

		const totalScore = statusCounts.success * 3 + statusCounts.warning * 1;
		const maxScore = this.results.length * 3;
		const percentage = Math.round((totalScore / maxScore) * 100);

		console.log(`\\n🎯 Overall Quality Score: ${percentage}%`);

		if (percentage >= 85) {
			console.log('🌟 EXCELLENT - Ready for production!');
		} else if (percentage >= 70) {
			console.log('👍 GOOD - Minor improvements needed');
		} else if (percentage >= 50) {
			console.log('⚠️  FAIR - Significant improvements needed');
		} else {
			console.log('🔧 NEEDS WORK - Major issues to address');
		}

		console.log('\\n' + '='.repeat(80));
	}
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
	const basePath = process.argv[2] || '.';
	const analyzer = new PictographImplementationAnalyzer(basePath);

	analyzer
		.analyze()
		.then((results) => {
			process.exit(results.some((r) => r.status === 'error') ? 1 : 0);
		})
		.catch((error) => {
			console.error('Analysis failed:', error);
			process.exit(1);
		});
}

export { PictographImplementationAnalyzer };
