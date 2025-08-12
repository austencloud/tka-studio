import js from '@eslint/js';
import ts from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import prettier from 'eslint-config-prettier';
import importPlugin from 'eslint-plugin-import';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import svelteParser from 'svelte-eslint-parser';

export default [
	// Base JavaScript configuration
	js.configs.recommended,

	// TypeScript configuration
	{
		files: ['**/*.ts', '**/*.tsx'],
		languageOptions: {
			parser: tsParser,
			parserOptions: {
				ecmaVersion: 2022,
				sourceType: 'module',
			},
			globals: {
				...globals.browser,
				...globals.node,
				...globals.es2022,
			},
		},
		plugins: {
			'@typescript-eslint': ts,
			import: importPlugin,
		},
		settings: {
			'import/resolver': {
				typescript: {
					project: './tsconfig.json',
					alwaysTryTypes: true,
				},
			},
			'import/parsers': {
				'@typescript-eslint/parser': ['.ts', '.tsx'],
			},
		},
		rules: {
			...ts.configs.recommended.rules,
			'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
			'@typescript-eslint/no-explicit-any': 'warn',
			'@typescript-eslint/no-non-null-assertion': 'warn',
			'prefer-const': 'error',
			'import/no-unresolved': ['error', { ignore: ['^$app/', '^$env/', '^$service-worker'] }],
			'import/no-absolute-path': 'error',
			'import/named': 'error',
			'import/default': 'error',
		},
	},

	// Svelte configuration
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				parser: tsParser,
				extraFileExtensions: ['.svelte'],
			},
			globals: {
				...globals.browser,
			},
		},
		plugins: {
			svelte,
			'@typescript-eslint': ts,
			import: importPlugin,
		},
		settings: {
			'import/resolver': {
				typescript: {
					project: './tsconfig.json',
					alwaysTryTypes: true,
				},
			},
			'import/parsers': {
				'@typescript-eslint/parser': ['.ts', '.tsx'],
				svelte: ['.svelte'],
			},
			'import/ignore': ['\\.svelte$'],
		},
		rules: {
			...svelte.configs.recommended.rules,
			...ts.configs.recommended.rules,
			'svelte/no-unused-svelte-ignore': 'error',
			'svelte/no-at-html-tags': 'warn',
			'svelte/valid-compile': 'error',
			'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
			// Relax import plugin rules for Svelte single-file components to avoid false positives
			'import/no-unresolved': 'off',
			'import/no-absolute-path': 'error',
			'import/named': 'off',
			'import/default': 'off',
		},
	},

	// Test files configuration
	{
		files: ['**/*.test.ts', '**/*.test.js', '**/*.spec.ts', '**/*.spec.js', 'tests/**/*'],
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node,
				describe: 'readonly',
				it: 'readonly',
				test: 'readonly',
				expect: 'readonly',
				beforeEach: 'readonly',
				afterEach: 'readonly',
				beforeAll: 'readonly',
				afterAll: 'readonly',
				vi: 'readonly',
			},
		},
		rules: {
			'@typescript-eslint/no-explicit-any': 'off',
			'@typescript-eslint/no-non-null-assertion': 'off',
		},
	},

	// Configuration files
	{
		files: ['*.config.js', '*.config.ts', '*.config.mjs'],
		languageOptions: {
			globals: {
				...globals.node,
			},
		},
		rules: {
			'@typescript-eslint/no-var-requires': 'off',
		},
	},

	// Node.js scripts and test files
	{
		files: ['scripts/**/*', 'tests/**/*', '**/*.test.*', '**/*.spec.*'],
		languageOptions: {
			globals: {
				...globals.node,
				console: 'readonly',
				process: 'readonly',
				Buffer: 'readonly',
				__dirname: 'readonly',
				__filename: 'readonly',
				global: 'readonly',
				NodeJS: 'readonly',
			},
		},
		rules: {
			'no-console': 'off',
			'@typescript-eslint/no-unused-vars': 'off',
		},
	},

	// Svelte files with runes
	{
		files: ['**/*.svelte.ts', '**/*.svelte.js'],
		languageOptions: {
			globals: {
				...globals.browser,
				$state: 'readonly',
				$derived: 'readonly',
				$effect: 'readonly',
				$props: 'readonly',
				$bindable: 'readonly',
				$inspect: 'readonly',
			},
		},
	},

	// Browser environment files
	{
		files: ['**/*.svelte', 'src/**/*.ts', 'src/**/*.js'],
		languageOptions: {
			globals: {
				...globals.browser,
				console: 'readonly',
				SVGElement: 'readonly',
				HTMLElement: 'readonly',
				Element: 'readonly',
				Document: 'readonly',
				Window: 'readonly',
				EventListener: 'readonly',
				AddEventListenerOptions: 'readonly',
				EventListenerOptions: 'readonly',
				NodeJS: 'readonly',
				$state: 'readonly',
				$derived: 'readonly',
				$effect: 'readonly',
				$props: 'readonly',
				$bindable: 'readonly',
				$inspect: 'readonly',
			},
		},
	},

	// Root-level JavaScript files (test and utility scripts)
	{
		files: ['*.js', '*.mjs'],
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node,
				console: 'readonly',
				process: 'readonly',
				SVGElement: 'readonly',
				HTMLElement: 'readonly',
				Element: 'readonly',
				Document: 'readonly',
				Window: 'readonly',
			},
		},
		rules: {
			'no-console': 'off',
		},
	},

	// Prettier integration (must be last)
	prettier,

	// Global ignores
	{
		ignores: [
			'node_modules/**',
			'.svelte-kit/**',
			'build/**',
			'dist/**',
			'playwright-report/**',
			'test-results/**',
			'coverage/**',
			'*.min.js',
			'static/**',
			'REFERENCE/**',
			'REMOVED_ANIMATION_BACKUP/**',
			'vitest-setup.ts',
		],
	},
];
