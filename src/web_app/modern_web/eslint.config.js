import js from '@eslint/js';
import ts from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import prettier from 'eslint-config-prettier';
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
		},
		rules: {
			...ts.configs.recommended.rules,
			'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
			'@typescript-eslint/no-explicit-any': 'warn',
			'@typescript-eslint/no-non-null-assertion': 'warn',
			'prefer-const': 'error',
		},
	},

	// Svelte configuration
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				parser: tsParser,
				project: './tsconfig.json',
				extraFileExtensions: ['.svelte'],
			},
			globals: {
				...globals.browser,
			},
		},
		plugins: {
			svelte,
			'@typescript-eslint': ts,
		},
		rules: {
			...svelte.configs.recommended.rules,
			...ts.configs.recommended.rules,
			'svelte/no-unused-svelte-ignore': 'error',
			'svelte/no-at-html-tags': 'warn',
			'svelte/valid-compile': 'error',
			'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
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
		],
	},
];
