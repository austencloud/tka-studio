/**
 * Download Handler Tests
 *
 * This module tests the download handler functionality.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { downloadSequenceImage } from './DownloadHandler.js';
import * as downloadUtils from '../../../components/Pictograph/export/downloadUtils.js';
import * as toastManager from '../../../components/shared/ToastManager.svelte.js';

// Mock browser environment
vi.mock('$app/environment', () => ({
  browser: true
}));

// Mock the downloadImage function
vi.mock('$lib/components/Pictograph/export/downloadUtils', () => ({
  downloadImage: vi.fn()
}));

// Mock the toast manager
vi.mock('$lib/components/shared/ToastManager.svelte', () => ({
  showError: vi.fn(),
  showSuccess: vi.fn()
}));

describe('DownloadHandler', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();

    // Mock localStorage
    const localStorageMock = {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn()
    };
    Object.defineProperty(window, 'localStorage', { value: localStorageMock });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should download a sequence image successfully', async () => {
    // Arrange
    const options = {
      sequenceName: 'AABB',
      imageResult: {
        dataUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
        width: 100,
        height: 100
      }
    };

    // Mock downloadImage to return success
    vi.mocked(downloadUtils.downloadImage).mockResolvedValue(true);

    // Act
    const result = await downloadSequenceImage(options);

    // Assert
    expect(result).toBe(true);
    expect(downloadUtils.downloadImage).toHaveBeenCalledWith({
      dataUrl: options.imageResult.dataUrl,
      filename: 'AABB.png'
    });
    expect(toastManager.showSuccess).toHaveBeenCalledWith('Image saved successfully');
  });

  it('should handle download failure', async () => {
    // Arrange
    const options = {
      sequenceName: 'AABB',
      imageResult: {
        dataUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
        width: 100,
        height: 100
      }
    };

    // Mock downloadImage to return failure
    vi.mocked(downloadUtils.downloadImage).mockResolvedValue(false);

    // Act
    const result = await downloadSequenceImage(options);

    // Assert
    expect(result).toBe(false);
    expect(downloadUtils.downloadImage).toHaveBeenCalledWith({
      dataUrl: options.imageResult.dataUrl,
      filename: 'AABB.png'
    });
    expect(toastManager.showError).toHaveBeenCalledWith('Failed to download sequence. Please try again.');
  });

  it('should handle user cancellation without showing an error', async () => {
    // Arrange
    const options = {
      sequenceName: 'AABB',
      imageResult: {
        dataUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
        width: 100,
        height: 100
      }
    };

    // Mock downloadImage to throw a cancellation error
    vi.mocked(downloadUtils.downloadImage).mockRejectedValue(new Error('Operation cancelled by user'));

    // Act
    const result = await downloadSequenceImage(options);

    // Assert
    expect(result).toBe(false);
    expect(downloadUtils.downloadImage).toHaveBeenCalledWith({
      dataUrl: options.imageResult.dataUrl,
      filename: 'AABB.png'
    });
    expect(toastManager.showError).not.toHaveBeenCalled();
  });
});
