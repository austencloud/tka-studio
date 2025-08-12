export interface Version {
  id: string
  name: string
  description: string
  path: string
  port: number
  packageManager: 'npm' | 'pnpm' | 'yarn'
  startCommand: string
  buildCommand?: string
  healthCheck: string
  status: VersionStatus
  lastStarted?: Date
  lastChecked?: Date
  version?: string
  performance?: PerformanceMetrics
  features?: string[]
  techStack?: string[]
}

export type VersionStatus =
  | 'available'
  | 'starting'
  | 'running'
  | 'stopping'
  | 'stopped'
  | 'error'
  | 'not-found'
  | 'manual-start-required'

export interface ServerInfo {
  pid?: number
  port: number
  url: string
  startTime: Date
  status: VersionStatus
  logs: LogEntry[]
}

export interface LogEntry {
  timestamp: Date
  level: 'info' | 'warn' | 'error' | 'debug'
  message: string
  source: string
}

export interface PerformanceMetrics {
  fps?: number
  memory?: {
    used: number
    total: number
  }
  loadTime?: number
  bundleSize?: number
  lastUpdated: Date
  timestamp: Date
  score?: number
}

export interface VersionConfig {
  id: string
  name: string
  description: string
  path: string
  port: number
  packageManager: 'npm' | 'pnpm' | 'yarn'
  startCommand: string
  buildCommand?: string
  healthCheck: string
  features?: string[]
  techStack?: string[]
}

export interface LauncherSettings {
  autoStart: boolean
  defaultVersion: string | null
  theme: 'light' | 'dark' | 'system'
  showPerformanceMetrics: boolean
  logLevel: 'debug' | 'info' | 'warn' | 'error'
  accessibility: AccessibilitySettings
  pwa: PWASettings
}

export interface AccessibilitySettings {
  reduceMotion: boolean
  highContrast: boolean
  screenReaderAnnouncements: boolean
  keyboardNavigationHelp: boolean
  fontSize: 'small' | 'medium' | 'large' | 'xl'
}

export interface PWASettings {
  enableNotifications: boolean
  enableBackgroundSync: boolean
  autoUpdate: boolean
  installPromptShown: boolean
  installPromptDismissed: boolean
  offlineMode: boolean
}

export interface PWAInstallPrompt {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

export interface RealTimeEvent {
  type: 'version-status' | 'performance-update' | 'log-entry' | 'server-info' | 'version-status-change' | 'collaborator-joined' | 'collaborator-left'
  versionId?: string
  data: any
  timestamp: Date
}

export interface ComparisonResult {
  versions: [string, string]
  metrics: {
    performance: PerformanceComparison
    features: FeatureComparison
    techStack: TechStackComparison
  }
  recommendations?: string[]
  timestamp: Date
}

export interface PerformanceComparison {
  fps: [number, number]
  memory: [number, number]
  loadTime: [number, number]
  bundleSize: [number, number]
  score: [number, number]
}

export interface FeatureComparison {
  common: string[]
  unique: [string[], string[]]
  missing: [string[], string[]]
}

export interface TechStackComparison {
  dependencies: {
    common: string[]
    unique: [string[], string[]]
    versions: Record<string, [string, string]>
  }
  devDependencies: {
    common: string[]
    unique: [string[], string[]]
    versions: Record<string, [string, string]>
  }
}

export interface DevServerManager {
  start(version: Version): Promise<ServerInfo>
  stop(versionId: string): Promise<void>
  restart(versionId: string): Promise<ServerInfo>
  getStatus(versionId: string): Promise<VersionStatus>
  getLogs(versionId: string): Promise<LogEntry[]>
  getPerformanceMetrics(versionId: string): Promise<PerformanceMetrics | null>
  openApp(versionId: string): Promise<void>
}

export interface VersionDetector {
  detectVersions(): Promise<Version[]>
  validateVersion(path: string): Promise<boolean>
  getVersionInfo(path: string): Promise<Partial<Version> | null>
}

export interface PortManager {
  findAvailablePort(startPort: number): Promise<number>
  isPortAvailable(port: number): Promise<boolean>
  getUsedPorts(): Promise<number[]>
}
