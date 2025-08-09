// Temporary auth service stub to fix build issues
import { writable } from 'svelte/store';

// Simple auth store
export const isAuthenticated = writable(false);

// Stub OAuth callback handler
export async function handleOAuthCallback(platform: string, code: string): Promise<void> {
  console.log(`OAuth callback received for ${platform} with code: ${code}`);
  // TODO: Implement actual OAuth handling
  isAuthenticated.set(true);
}

// Stub login function
export async function login(platform: string): Promise<void> {
  console.log(`Login attempted for platform: ${platform}`);
  // TODO: Implement actual login
}

// Stub logout function
export async function logout(): Promise<void> {
  console.log('Logout attempted');
  isAuthenticated.set(false);
}
