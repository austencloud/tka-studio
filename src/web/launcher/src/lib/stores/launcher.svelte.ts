import type {
	Version,
	ServerInfo,
	LauncherSettings,
	PerformanceMetrics,
	ComparisonResult,
	LogEntry,
	RealTimeEvent,
	AccessibilitySettings,
	PWAInstallPrompt
} from '../types/launcher.types.js';
import { versionDetector } from '../services/version-detector.js';
import { devServerManager } from '../services/dev-server-manager.js';
import { portManager } from '../services/port-manager.js';
import { realTimeService } from '../services/real-time-service.js';
import { accessibilityService } from '../services/accessibility-service.js';
import { pwaService } from '../services/pwa-service.js';

export class ModernLauncherState {
	// Core reactive state with enhanced typing
	versions = $state<Version[]>([]);
	runningServers = $state<Map<string, ServerInfo>>(new Map());
	activeVersion = $state<string | null>(null);
	isLoading = $state(false);
	error = $state<string | null>(null);
	isInitialized = $state(false);

	// UI state with accessibility features
	selectedVersions = $state<string[]>([]);
	showComparison = $state(false);
	showLogs = $state(false);
	showPerformanceMetrics = $state(true);
	viewMode = $state<'grid' | 'list' | 'compact'>('grid');
	focusedVersionId = $state<string | null>(null);

	// Enhanced settings with accessibility
	settings = $state<LauncherSettings>({
		autoStart: false,
		defaultVersion: null,
		theme: 'system',
		showPerformanceMetrics: true,
		logLevel: 'info',
		accessibility: {
			reduceMotion: false,
			highContrast: false,
			screenReaderAnnouncements: true,
			keyboardNavigationHelp: true,
			fontSize: 'medium'
		},
		pwa: {
			enableNotifications: true,
			enableBackgroundSync: true,
			autoUpdate: true,
			installPromptShown: false,
			installPromptDismissed: false,
			offlineMode: true
		}
	});

	// Real-time capabilities
	isConnected = $state(false);
	connectionStatus = $state<'connected' | 'disconnected' | 'connecting' | 'error'>('disconnected');
	realTimeEvents = $state<RealTimeEvent[]>([]);
	collaborators = $state<Map<string, { name: string; lastSeen: Date }>>(new Map());

	// Performance tracking with advanced metrics
	performanceMetrics = $state<Map<string, PerformanceMetrics>>(new Map());
	comparisonResults = $state<ComparisonResult[]>([]);
	systemMetrics = $state({
		cpuUsage: 0,
		memoryUsage: 0,
		networkLatency: 0,
		batteryLevel: 100,
		isOnline: true
	});

	// Enhanced logging with filtering
	logs = $state<Map<string, LogEntry[]>>(new Map());
	logFilters = $state({
		level: 'all' as 'all' | 'error' | 'warn' | 'info' | 'debug',
		search: '',
		timeRange: '1h' as '5m' | '15m' | '1h' | '6h' | '24h' | 'all'
	});

	// PWA features
	installPrompt = $state<PWAInstallPrompt | null>(null);
	isInstalled = $state(false);
	updateAvailable = $state(false);
	offlineCapable = $state(false);

	// Accessibility state
	announcements = $state<
		Array<{ message: string; priority: 'polite' | 'assertive'; timestamp: Date }>
	>([]);
	keyboardNavigationMode = $state(false);

	// Advanced derived state with performance optimizations
	availableVersions = $derived(
		this.versions.filter((v) => v.status === 'available' || v.status === 'running')
	);

	runningVersions = $derived(this.versions.filter((v) => v.status === 'running'));

	hasRunningServers = $derived(this.runningServers.size > 0);

	canCompare = $derived(
		this.selectedVersions.length === 2 &&
			this.selectedVersions.every(
				(id) => this.versions.find((v) => v.id === id)?.status === 'running'
			)
	);

	filteredLogs = $derived(() => {
		const allLogs = Array.from(this.logs.values()).flat();
		return allLogs
			.filter((log) => {
				if (this.logFilters.level !== 'all' && log.level !== this.logFilters.level) {
					return false;
				}
				if (
					this.logFilters.search &&
					!log.message.toLowerCase().includes(this.logFilters.search.toLowerCase())
				) {
					return false;
				}
				if (this.logFilters.timeRange !== 'all') {
					const timeRangeMs = this.getTimeRangeMs(this.logFilters.timeRange);
					if (Date.now() - log.timestamp.getTime() > timeRangeMs) {
						return false;
					}
				}
				return true;
			})
			.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
	});

	overallPerformanceScore = $derived(() => {
		if (this.performanceMetrics.size === 0) return 0;
		const scores = Array.from(this.performanceMetrics.values()).map((metrics) => {
			const fpsScore = Math.min(((metrics.fps || 60) / 60) * 100, 100);
			const memoryScore = Math.max(
				100 - ((metrics.memory?.used || 50) / (metrics.memory?.total || 100)) * 100,
				0
			);
			const loadTimeScore = Math.max(100 - (metrics.loadTime || 1000) / 50, 0);
			return (fpsScore + memoryScore + loadTimeScore) / 3;
		});
		return Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length);
	});

	// Enhanced viewport and device detection
	viewport = $state({
		width: 0,
		height: 0,
		isMobile: false,
		isTablet: false,
		isDesktop: false,
		orientation: 'portrait' as 'portrait' | 'landscape',
		pixelRatio: 1,
		isTouch: false
	});

	constructor() {
		// Enhanced initialization with accessibility detection
		if (typeof window !== 'undefined') {
			this.loadSettings();
			this.detectAccessibilityPreferences();
			this.initializeViewport();
			this.setupNetworkDetection();
		}
	}

	// Enhanced setup with real-time capabilities
	setupEffects() {
		// Auto-refresh versions with adaptive interval
		$effect(() => {
			const interval = this.isConnected ? 60000 : 30000; // Slower refresh when connected to WebSocket
			const timer = setInterval(() => {
				if (document.visibilityState === 'visible') {
					this.refreshVersions();
				}
			}, interval);

			return () => clearInterval(timer);
		});

		// Real-time performance monitoring
		$effect(() => {
			if (this.settings.showPerformanceMetrics && this.hasRunningServers) {
				const interval = setInterval(() => {
					this.updatePerformanceMetrics();
					this.updateSystemMetrics();
				}, 2000);

				return () => clearInterval(interval);
			}
		});

		// Settings persistence with validation
		$effect(() => {
			if (typeof window !== 'undefined' && this.isInitialized) {
				try {
					localStorage.setItem('launcher-settings', JSON.stringify(this.settings));
				} catch (error) {
					console.warn('Failed to save settings:', error);
					this.announceToScreenReader('Settings could not be saved', 'assertive');
				}
			}
		});

		// Real-time connection management
		$effect(() => {
			if (this.isInitialized) {
				this.establishRealTimeConnection();
			}

			return () => {
				realTimeService.disconnect();
			};
		});

		// PWA installation detection
		$effect(() => {
			pwaService.onInstallPrompt((prompt) => {
				if (!this.settings.pwa.installPromptDismissed) {
					this.installPrompt = prompt;
				}
			});

			pwaService.onInstalled(() => {
				this.isInstalled = true;
				this.announceToScreenReader('Application installed successfully', 'polite');
			});

			pwaService.onUpdateAvailable(() => {
				this.updateAvailable = true;
				this.announceToScreenReader('Application update available', 'polite');
			});
		});

		// Accessibility announcements cleanup
		$effect(() => {
			if (this.announcements.length > 0) {
				const timer = setTimeout(() => {
					this.announcements = this.announcements.slice(0, -1);
				}, 5000);
				return () => clearTimeout(timer);
			}
		});

		// Keyboard navigation detection
		$effect(() => {
			const handleKeyDown = (event: KeyboardEvent) => {
				if (event.key === 'Tab') {
					this.keyboardNavigationMode = true;
				}
			};

			const handleMouseDown = () => {
				this.keyboardNavigationMode = false;
			};

			if (typeof window !== 'undefined') {
				window.addEventListener('keydown', handleKeyDown);
				window.addEventListener('mousedown', handleMouseDown);

				return () => {
					window.removeEventListener('keydown', handleKeyDown);
					window.removeEventListener('mousedown', handleMouseDown);
				};
			}
		});
	}

	// Enhanced initialization with error recovery
	async initialize(): Promise<void> {
		if (this.isInitialized) return;

		this.isLoading = true;
		this.error = null;

		try {
			// Initialize core services
			await Promise.all([this.refreshVersions(), this.initializePWA(), this.loadUserPreferences()]);

			// Auto-start default version with validation
			if (this.settings.autoStart && this.settings.defaultVersion) {
				const defaultVersion = this.versions.find((v) => v.id === this.settings.defaultVersion);
				if (defaultVersion?.status === 'available') {
					await this.startVersion(defaultVersion.id);
				}
			}

			this.isInitialized = true;
			this.announceToScreenReader('Launcher initialized successfully', 'polite');
		} catch (error) {
			this.error = error instanceof Error ? error.message : 'Failed to initialize launcher';
			console.error('Launcher initialization failed:', error);
			this.announceToScreenReader(`Initialization failed: ${this.error}`, 'assertive');
		} finally {
			this.isLoading = false;
		}
	}

	// Enhanced version management with real-time updates
	async refreshVersions(): Promise<void> {
		try {
			const detectedVersions = await versionDetector.detectVersions();

			// Smart update: preserve running status and maintain selection
			const updatedVersions = detectedVersions.map((detected) => {
				const existing = this.versions.find((v) => v.id === detected.id);
				if (existing) {
					return {
						...detected,
						status: existing.status === 'running' ? 'running' : detected.status,
						lastStarted: existing.lastStarted
					};
				}
				return detected;
			});

			// Detect removed versions
			const removedVersions = this.versions.filter(
				(existing) => !detectedVersions.find((detected) => detected.id === existing.id)
			);

			// Clean up removed versions
			for (const removed of removedVersions) {
				if (removed.status === 'running') {
					this.runningServers.delete(removed.id);
					this.performanceMetrics.delete(removed.id);
					this.logs.delete(removed.id);
				}
				this.selectedVersions = this.selectedVersions.filter((id) => id !== removed.id);
			}

			this.versions = updatedVersions;

			// Broadcast version changes
			if (this.isConnected) {
				const event: RealTimeEvent = {
					type: 'server-info',
					data: {
						versions: this.versions.length,
						running: this.runningVersions.length
					},
					timestamp: new Date()
				};
				realTimeService.broadcast(event);
			}
		} catch (error) {
			console.error('Failed to refresh versions:', error);
			this.error = 'Failed to detect versions';
			this.announceToScreenReader('Failed to refresh version list', 'assertive');
		}
	}

	// Enhanced version lifecycle with better error handling
	async startVersion(versionId: string): Promise<void> {
		const version = this.versions.find((v) => v.id === versionId);
		if (!version) {
			throw new Error(`Version ${versionId} not found`);
		}

		if (version.status === 'running') {
			this.announceToScreenReader(`${version.name} is already running`, 'polite');
			return;
		}

		try {
			version.status = 'starting';
			this.announceToScreenReader(`Starting ${version.name}`, 'polite');

			const serverInfo = await devServerManager.start(version);

			version.status = 'running';
			version.lastStarted = new Date();
			this.runningServers.set(versionId, serverInfo);
			this.activeVersion = versionId;

			// Initialize monitoring
			await Promise.all([
				this.startLogCollection(versionId),
				this.startPerformanceMonitoring(versionId)
			]);

			this.announceToScreenReader(
				`${version.name} started successfully on port ${serverInfo.port}`,
				'polite'
			);

			// Broadcast real-time event
			if (this.isConnected) {
				const event: RealTimeEvent = {
					type: 'version-status',
					versionId,
					data: {
						name: version.name,
						port: serverInfo.port,
						status: 'running'
					},
					timestamp: new Date()
				};
				realTimeService.broadcast(event);
			}
		} catch (error) {
			version.status = 'error';
			const errorMessage = error instanceof Error ? error.message : 'Unknown error';
			this.announceToScreenReader(`Failed to start ${version.name}: ${errorMessage}`, 'assertive');
			throw error;
		}
	}

	async stopVersion(versionId: string): Promise<void> {
		const version = this.versions.find((v) => v.id === versionId);
		if (!version) {
			throw new Error(`Version ${versionId} not found`);
		}

		try {
			version.status = 'stopping';
			this.announceToScreenReader(`Stopping ${version.name}`, 'polite');

			await devServerManager.stop(versionId);

			version.status = 'available';
			this.runningServers.delete(versionId);
			this.performanceMetrics.delete(versionId);
			this.logs.delete(versionId);

			if (this.activeVersion === versionId) {
				this.activeVersion = this.runningVersions[0]?.id || null;
			}

			this.announceToScreenReader(`${version.name} stopped successfully`, 'polite');

			// Broadcast real-time event
			if (this.isConnected) {
				const event: RealTimeEvent = {
					type: 'version-status',
					versionId,
					data: {
						name: version.name,
						status: 'stopped'
					},
					timestamp: new Date()
				};
				realTimeService.broadcast(event);
			}
		} catch (error) {
			version.status = 'error';
			const errorMessage = error instanceof Error ? error.message : 'Unknown error';
			this.announceToScreenReader(`Failed to stop ${version.name}: ${errorMessage}`, 'assertive');
			throw error;
		}
	}

	async restartVersion(versionId: string): Promise<void> {
		const version = this.versions.find((v) => v.id === versionId);
		if (!version) return;

		this.announceToScreenReader(`Restarting ${version.name}`, 'polite');

		await this.stopVersion(versionId);
		await new Promise((resolve) => setTimeout(resolve, 1500)); // Longer delay for clean restart
		await this.startVersion(versionId);
	}

	// Enhanced comparison with detailed analysis
	async compareVersions(version1Id: string, version2Id: string): Promise<void> {
		const v1 = this.versions.find((v) => v.id === version1Id);
		const v2 = this.versions.find((v) => v.id === version2Id);

		if (!v1 || !v2) {
			throw new Error('One or both versions not found');
		}

		this.announceToScreenReader(`Comparing ${v1.name} and ${v2.name}`, 'polite');

		// Ensure both versions are running
		const startPromises = [];
		if (v1.status !== 'running') {
			startPromises.push(this.startVersion(version1Id));
		}
		if (v2.status !== 'running') {
			startPromises.push(this.startVersion(version2Id));
		}

		if (startPromises.length > 0) {
			await Promise.all(startPromises);
			// Wait for metrics to stabilize
			await new Promise((resolve) => setTimeout(resolve, 3000));
		}

		// Collect comprehensive comparison data
		const metrics1 = this.performanceMetrics.get(version1Id);
		const metrics2 = this.performanceMetrics.get(version2Id);

		if (metrics1 && metrics2) {
			const comparison: ComparisonResult = {
				versions: [version1Id, version2Id],
				metrics: {
					performance: {
						fps: [metrics1.fps || 0, metrics2.fps || 0],
						memory: [metrics1.memory?.used || 0, metrics2.memory?.used || 0],
						loadTime: [metrics1.loadTime || 0, metrics2.loadTime || 0],
						bundleSize: [metrics1.bundleSize || 0, metrics2.bundleSize || 0],
						score: [
							this.calculatePerformanceScore(metrics1),
							this.calculatePerformanceScore(metrics2)
						]
					},
					features: {
						common: v1.features?.filter((f) => v2.features?.includes(f)) || [],
						unique: [
							v1.features?.filter((f) => !v2.features?.includes(f)) || [],
							v2.features?.filter((f) => !v1.features?.includes(f)) || []
						],
						missing: [[], []]
					},
					techStack: {
						dependencies: {
							common: v1.techStack?.filter((t) => v2.techStack?.includes(t)) || [],
							unique: [
								v1.techStack?.filter((t) => !v2.techStack?.includes(t)) || [],
								v2.techStack?.filter((t) => !v1.techStack?.includes(t)) || []
							],
							versions: {}
						},
						devDependencies: {
							common: [],
							unique: [[], []],
							versions: {}
						}
					}
				},
				recommendations: this.generateComparisonRecommendations(metrics1, metrics2, v1, v2),
				timestamp: new Date()
			};

			this.comparisonResults.unshift(comparison);

			// Keep only last 10 comparisons
			if (this.comparisonResults.length > 10) {
				this.comparisonResults.splice(10);
			}

			this.announceToScreenReader('Comparison completed successfully', 'polite');
		}

		this.selectedVersions = [version1Id, version2Id];
		this.showComparison = true;
	}

	// Enhanced selection management
	toggleVersionSelection(versionId: string): void {
		const version = this.versions.find((v) => v.id === versionId);
		if (!version || version.status === 'not-found') return;

		const index = this.selectedVersions.indexOf(versionId);
		const wasSelected = index >= 0;

		if (wasSelected) {
			this.selectedVersions.splice(index, 1);
			this.announceToScreenReader(`${version.name} deselected`, 'polite');
		} else if (this.selectedVersions.length < 2) {
			this.selectedVersions.push(versionId);
			this.announceToScreenReader(`${version.name} selected`, 'polite');
		} else {
			// Replace first selection with new one
			const oldSelection = this.versions.find((v) => v.id === this.selectedVersions[0]);
			this.selectedVersions[0] = this.selectedVersions[1];
			this.selectedVersions[1] = versionId;
			this.announceToScreenReader(
				`${oldSelection?.name} deselected, ${version.name} selected`,
				'polite'
			);
		}

		// Auto-enable comparison mode when two versions selected
		if (this.selectedVersions.length === 2 && this.canCompare) {
			this.showComparison = true;
		}
	}

	// Real-time connection management
	private async establishRealTimeConnection(): Promise<void> {
		try {
			this.connectionStatus = 'connecting';

			await realTimeService.connect({
				onConnected: () => {
					this.isConnected = true;
					this.connectionStatus = 'connected';
					this.announceToScreenReader('Real-time connection established', 'polite');
				},
				onDisconnected: () => {
					this.isConnected = false;
					this.connectionStatus = 'disconnected';
					this.announceToScreenReader('Real-time connection lost', 'assertive');
				},
				onError: (error) => {
					this.connectionStatus = 'error';
					console.error('Real-time connection error:', error);
				},
				onEvent: (event) => {
					this.handleRealTimeEvent(event);
				}
			});
		} catch (error) {
			this.connectionStatus = 'error';
			console.error('Failed to establish real-time connection:', error);
		}
	}

	private handleRealTimeEvent(event: RealTimeEvent): void {
		this.realTimeEvents.unshift(event);

		// Keep only recent events
		if (this.realTimeEvents.length > 100) {
			this.realTimeEvents.splice(100);
		}

		// Handle specific event types
		switch (event.type) {
			case 'performance-update':
				if (event.data.versionId && event.data.metrics) {
					this.performanceMetrics.set(event.data.versionId, event.data.metrics);
				}
				break;
			case 'version-status-change':
				const version = this.versions.find((v) => v.id === event.data.versionId);
				if (version && event.data.status) {
					version.status = event.data.status;
					this.announceToScreenReader(
						`${version.name} status changed to ${event.data.status}`,
						'polite'
					);
				}
				break;
			case 'collaborator-joined':
				if (event.data.collaborator) {
					this.collaborators.set(event.data.collaborator.id, {
						name: event.data.collaborator.name,
						lastSeen: new Date()
					});
				}
				break;
			case 'collaborator-left':
				if (event.data.collaboratorId) {
					this.collaborators.delete(event.data.collaboratorId);
				}
				break;
		}
	}

	// Enhanced performance monitoring
	private async updatePerformanceMetrics(): Promise<void> {
		const updatePromises = Array.from(this.runningServers.keys()).map(async (versionId) => {
			try {
				const metrics = await devServerManager.getPerformanceMetrics(versionId);
				if (metrics) {
					this.performanceMetrics.set(versionId, {
						...metrics,
						timestamp: new Date(),
						score: this.calculatePerformanceScore(metrics)
					});

					// Broadcast if connected
					if (this.isConnected) {
						const event: RealTimeEvent = {
							type: 'performance-update',
							versionId,
							data: { metrics },
							timestamp: new Date()
						};
						realTimeService.broadcast(event);
					}
				}
			} catch (error) {
				console.warn(`Failed to get metrics for ${versionId}:`, error);
			}
		});

		await Promise.all(updatePromises);
	}

	private async updateSystemMetrics(): Promise<void> {
		try {
			// Modern browser APIs for system monitoring
			if ('navigator' in window) {
				this.systemMetrics.isOnline = navigator.onLine;

				// @ts-ignore - Experimental API
				if ('connection' in navigator) {
					const connection = (navigator as any).connection;
					this.systemMetrics.networkLatency = connection.rtt || 0;
				}

				// @ts-ignore - Battery API
				if ('getBattery' in navigator) {
					const battery = await (navigator as any).getBattery();
					this.systemMetrics.batteryLevel = Math.round(battery.level * 100);
				}
			}

			// Performance observer for CPU/Memory if available
			if ('performance' in window && 'memory' in window.performance) {
				const memory = (window.performance as any).memory;
				this.systemMetrics.memoryUsage = Math.round(
					(memory.usedJSHeapSize / memory.totalJSHeapSize) * 100
				);
			}
		} catch (error) {
			console.warn('Failed to update system metrics:', error);
		}
	}

	// Enhanced logging with real-time streaming
	private async startLogCollection(versionId: string): Promise<void> {
		const collectLogs = async () => {
			try {
				const logs = await devServerManager.getLogs(versionId);
				this.logs.set(versionId, logs);

				// Broadcast new logs if connected
				if (this.isConnected && logs.length > 0) {
					const latestLogs = logs.slice(-5); // Send only recent logs
					const event: RealTimeEvent = {
						type: 'log-entry',
						versionId,
						data: { logs: latestLogs },
						timestamp: new Date()
					};
					realTimeService.broadcast(event);
				}
			} catch (error) {
				console.warn(`Failed to collect logs for ${versionId}:`, error);
			}
		};

		// Initial collection
		await collectLogs();

		// Set up real-time collection
		const interval = setInterval(collectLogs, 1000);

		// Store cleanup function for proper resource management
		const cleanup = () => {
			clearInterval(interval);
		};

		// Clean up when server stops (improved cleanup management)
		const checkServerStatus = () => {
			if (!this.runningServers.has(versionId)) {
				cleanup();
			} else {
				setTimeout(checkServerStatus, 1000);
			}
		};
		setTimeout(checkServerStatus, 1000);
	}

	// PWA methods
	async installPWA(): Promise<void> {
		if (this.installPrompt) {
			try {
				await pwaService.install(this.installPrompt);
				this.installPrompt = null;
				this.announceToScreenReader('Application installation started', 'polite');
			} catch (error) {
				console.error('Failed to install PWA:', error);
				this.announceToScreenReader('Application installation failed', 'assertive');
			}
		}
	}

	dismissInstallPrompt(): void {
		this.installPrompt = null;
		this.settings.pwa.installPromptDismissed = true;
		this.announceToScreenReader('Installation prompt dismissed', 'polite');
	}

	async updatePWA(): Promise<void> {
		try {
			await pwaService.update();
			this.updateAvailable = false;
			this.announceToScreenReader('Application updated successfully', 'polite');
		} catch (error) {
			console.error('Failed to update PWA:', error);
			this.announceToScreenReader('Application update failed', 'assertive');
		}
	}

	// Accessibility methods
	announceToScreenReader(message: string, priority: 'polite' | 'assertive' = 'polite'): void {
		if (this.settings.accessibility.screenReaderAnnouncements) {
			this.announcements.unshift({
				message,
				priority,
				timestamp: new Date()
			});
		}
	}

	setFocus(versionId: string): void {
		this.focusedVersionId = versionId;
		const version = this.versions.find((v) => v.id === versionId);
		if (version) {
			this.announceToScreenReader(`Focused on ${version.name}`, 'polite');
		}
	}

	// Settings management with validation
	updateSettings(updates: Partial<LauncherSettings>): void {
		const oldSettings = { ...this.settings };
		Object.assign(this.settings, updates);

		// Validate critical settings
		if (updates.accessibility?.reduceMotion !== oldSettings.accessibility?.reduceMotion) {
			this.announceToScreenReader(
				`Motion ${updates.accessibility?.reduceMotion ? 'reduced' : 'enabled'}`,
				'polite'
			);
		}

		if (updates.theme && updates.theme !== oldSettings.theme) {
			this.announceToScreenReader(`Theme changed to ${updates.theme}`, 'polite');
		}
	}

	// Enhanced utility methods
	private calculatePerformanceScore(metrics: PerformanceMetrics): number {
		const fpsScore = Math.min(((metrics.fps || 60) / 60) * 100, 100);
		const memoryScore = Math.max(
			100 - ((metrics.memory?.used || 50) / (metrics.memory?.total || 100)) * 100,
			0
		);
		const loadTimeScore = Math.max(100 - (metrics.loadTime || 1000) / 50, 0);
		return Math.round((fpsScore + memoryScore + loadTimeScore) / 3);
	}

	private generateComparisonRecommendations(
		metrics1: PerformanceMetrics,
		metrics2: PerformanceMetrics,
		v1: Version,
		v2: Version
	): string[] {
		const recommendations: string[] = [];

		// Performance recommendations
		const score1 = this.calculatePerformanceScore(metrics1);
		const score2 = this.calculatePerformanceScore(metrics2);

		if (Math.abs(score1 - score2) > 10) {
			const better = score1 > score2 ? v1.name : v2.name;
			recommendations.push(`${better} shows significantly better performance`);
		}

		// Memory recommendations
		const mem1 = metrics1.memory?.used || 0;
		const mem2 = metrics2.memory?.used || 0;
		if (Math.abs(mem1 - mem2) > 50) {
			const efficient = mem1 < mem2 ? v1.name : v2.name;
			recommendations.push(`${efficient} uses less memory`);
		}

		// Load time recommendations
		const load1 = metrics1.loadTime || 0;
		const load2 = metrics2.loadTime || 0;
		if (Math.abs(load1 - load2) > 500) {
			const faster = load1 < load2 ? v1.name : v2.name;
			recommendations.push(`${faster} loads faster`);
		}

		return recommendations;
	}

	private getTimeRangeMs(range: string): number {
		switch (range) {
			case '5m':
				return 5 * 60 * 1000;
			case '15m':
				return 15 * 60 * 1000;
			case '1h':
				return 60 * 60 * 1000;
			case '6h':
				return 6 * 60 * 60 * 1000;
			case '24h':
				return 24 * 60 * 60 * 1000;
			default:
				return Infinity;
		}
	}

	private loadSettings(): void {
		try {
			const saved = localStorage.getItem('launcher-settings');
			if (saved) {
				const parsed = JSON.parse(saved);
				Object.assign(this.settings, parsed);
			}
		} catch (error) {
			console.warn('Failed to load settings:', error);
		}
	}

	private detectAccessibilityPreferences(): void {
		if (typeof window === 'undefined') return;

		// Detect user preferences
		const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		const prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches;

		this.settings.accessibility.reduceMotion = prefersReducedMotion;
		this.settings.accessibility.highContrast = prefersHighContrast;
	}

	private initializeViewport(): void {
		if (typeof window === 'undefined') return;

		const updateViewport = () => {
			this.viewport = {
				width: window.innerWidth,
				height: window.innerHeight,
				isMobile: window.innerWidth < 768,
				isTablet: window.innerWidth >= 768 && window.innerWidth < 1024,
				isDesktop: window.innerWidth >= 1024,
				orientation: window.innerWidth > window.innerHeight ? 'landscape' : 'portrait',
				pixelRatio: window.devicePixelRatio || 1,
				isTouch: 'ontouchstart' in window
			};
		};

		updateViewport();
		window.addEventListener('resize', updateViewport);
		window.addEventListener('orientationchange', updateViewport);
	}

	private setupNetworkDetection(): void {
		if (typeof window === 'undefined') return;

		const updateNetworkStatus = () => {
			this.systemMetrics.isOnline = navigator.onLine;
		};

		updateNetworkStatus();
		window.addEventListener('online', updateNetworkStatus);
		window.addEventListener('offline', updateNetworkStatus);
	}

	private async initializePWA(): Promise<void> {
		try {
			await pwaService.initialize();
			this.isInstalled = pwaService.isInstalled();
			this.offlineCapable = pwaService.isOfflineCapable();
		} catch (error) {
			console.warn('PWA initialization failed:', error);
		}
	}

	private async loadUserPreferences(): Promise<void> {
		try {
			const preferences = await accessibilityService.loadUserPreferences();
			if (preferences) {
				this.updateSettings({ accessibility: preferences });
			}
		} catch (error) {
			console.warn('Failed to load user preferences:', error);
		}
	}

	private async startPerformanceMonitoring(versionId: string): Promise<void> {
		// Start collecting performance metrics immediately
		setTimeout(() => this.updatePerformanceMetrics(), 1000);
	}

	// Public utility methods
	clearError(): void {
		this.error = null;
	}

	closeComparison(): void {
		this.showComparison = false;
		this.selectedVersions = [];
		this.announceToScreenReader('Comparison closed', 'polite');
	}

	toggleLogs(): void {
		this.showLogs = !this.showLogs;
		this.announceToScreenReader(`Logs ${this.showLogs ? 'opened' : 'closed'}`, 'polite');
	}

	setViewMode(mode: 'grid' | 'list' | 'compact'): void {
		this.viewMode = mode;
		this.announceToScreenReader(`View mode changed to ${mode}`, 'polite');
	}

	async openApp(versionId: string): Promise<void> {
		try {
			await devServerManager.openApp(versionId);
			const version = this.versions.find((v) => v.id === versionId);
			this.announceToScreenReader(`Opening ${version?.name || 'application'} in browser`, 'polite');
		} catch (error) {
			console.error(`Failed to open app ${versionId}:`, error);
			this.announceToScreenReader('Failed to open application', 'assertive');
			throw error;
		}
	}
}

export const launcherState = new ModernLauncherState();
