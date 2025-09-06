/**
 * Download Utilities Tests
 *
 * This module tests the download utilities.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { downloadImage } from './downloadUtils';

// Mock browser environment
vi.mock('$app/environment', () => ({
	browser: true
}));

describe('downloadUtils', () => {
	// Mock DOM elements and functions
	let mockLink: any;
	let mockAppendChild: any;
	let mockRemoveChild: any;
	let mockCreateObjectURL: any;
	let mockRevokeObjectURL: any;
	let mockShowSaveFilePicker: any;
	let mockFileHandle: any;
	let mockWritable: any;

	beforeEach(() => {
		// Mock link element
		mockLink = {
			href: '',
			download: '',
			style: { display: 'none' },
			click: vi.fn(),
			getBoundingClientRect: vi.fn()
		};

		// Mock document methods
		mockAppendChild = vi.fn();
		mockRemoveChild = vi.fn();
		document.body.appendChild = mockAppendChild;
		document.body.removeChild = mockRemoveChild;
		document.body.contains = vi.fn().mockReturnValue(true);
		document.createElement = vi.fn().mockReturnValue(mockLink);

		// Mock URL methods
		mockCreateObjectURL = vi.fn().mockReturnValue('blob:mock-url');
		mockRevokeObjectURL = vi.fn();
		URL.createObjectURL = mockCreateObjectURL;
		URL.revokeObjectURL = mockRevokeObjectURL;

		// Mock File System Access API
		mockWritable = {
			write: vi.fn().mockResolvedValue(undefined),
			close: vi.fn().mockResolvedValue(undefined)
		};
		mockFileHandle = {
			createWritable: vi.fn().mockResolvedValue(mockWritable)
		};
		mockShowSaveFilePicker = vi.fn().mockResolvedValue(mockFileHandle);
		window.showSaveFilePicker = mockShowSaveFilePicker;

		// Mock setTimeout
		vi.useFakeTimers();
	});

	afterEach(() => {
		vi.clearAllMocks();
		vi.useRealTimers();
	});

	it('should use File System Access API when available', async () => {
		// Arrange
		const dataUrl =
			'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
		const filename = 'test.png';

		// Act
		const result = await downloadImage({ dataUrl, filename });

		// Assert
		expect(mockShowSaveFilePicker).toHaveBeenCalledWith({
			suggestedName: filename,
			types: [
				{
					description: 'Image Files',
					accept: {
						'image/png': ['.png'],
						'image/jpeg': ['.jpg', '.jpeg']
					}
				}
			],
			startIn: 'downloads'
		});
		expect(mockFileHandle.createWritable).toHaveBeenCalled();
		expect(mockWritable.write).toHaveBeenCalled();
		expect(mockWritable.close).toHaveBeenCalled();
		expect(result).toBe(true);
	});

	it('should fall back to traditional download when File System Access API fails', async () => {
		// Arrange
		const dataUrl =
			'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
		const filename = 'test.png';

		// Mock File System Access API to fail
		window.showSaveFilePicker = vi.fn().mockRejectedValue(new Error('User cancelled'));

		// Mock setTimeout to execute immediately
		vi.spyOn(global, 'setTimeout').mockImplementation((callback: any) => {
			callback();
			return 0 as any;
		});

		// Act
		const result = await downloadImage({ dataUrl, filename });

		// Assert
		expect(window.showSaveFilePicker).toHaveBeenCalled();
		expect(mockLink.href).toBe('blob:mock-url');
		expect(mockLink.download).toBe(filename);
		expect(mockLink.click).toHaveBeenCalled();
		expect(result).toBe(true);
	}, 10000);
});
