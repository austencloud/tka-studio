/**
 * Type definitions for the File System Access API
 *
 * These types are based on the File System Access API specification:
 * https://wicg.github.io/file-system-access/
 */

interface FileSystemHandle {
	readonly kind: 'file' | 'directory';
	readonly name: string;
	isSameEntry(other: FileSystemHandle): Promise<boolean>;
}

interface FileSystemFileHandle extends FileSystemHandle {
	readonly kind: 'file';
	getFile(): Promise<File>;
	createWritable(options?: FileSystemCreateWritableOptions): Promise<FileSystemWritableFileStream>;
}

interface FileSystemDirectoryHandle extends FileSystemHandle {
	readonly kind: 'directory';
	getFileHandle(name: string, options?: FileSystemGetFileOptions): Promise<FileSystemFileHandle>;
	getDirectoryHandle(
		name: string,
		options?: FileSystemGetDirectoryOptions
	): Promise<FileSystemDirectoryHandle>;
	removeEntry(name: string, options?: FileSystemRemoveOptions): Promise<void>;
	resolve(possibleDescendant: FileSystemHandle): Promise<string[] | null>;
	keys(): AsyncIterableIterator<string>;
	values(): AsyncIterableIterator<FileSystemHandle>;
	entries(): AsyncIterableIterator<[string, FileSystemHandle]>;
}

interface FileSystemCreateWritableOptions {
	keepExistingData?: boolean;
}

interface FileSystemGetFileOptions {
	create?: boolean;
}

interface FileSystemGetDirectoryOptions {
	create?: boolean;
}

interface FileSystemRemoveOptions {
	recursive?: boolean;
}

interface FileSystemWritableFileStream extends WritableStream {
	write(data: FileSystemWriteChunkType): Promise<void>;
	seek(position: number): Promise<void>;
	truncate(size: number): Promise<void>;
}

type FileSystemWriteChunkType =
	| BufferSource
	| Blob
	| string
	| { type: 'write'; position?: number; data: BufferSource | Blob | string }
	| { type: 'seek'; position: number }
	| { type: 'truncate'; size: number };

interface SaveFilePickerOptions {
	suggestedName?: string;
	types?: FilePickerAcceptType[];
	excludeAcceptAllOption?: boolean;
	startIn?:
		| FileSystemHandle
		| 'desktop'
		| 'documents'
		| 'downloads'
		| 'music'
		| 'pictures'
		| 'videos';
	mode?: 'save';
}

interface FilePickerAcceptType {
	description?: string;
	accept: Record<string, string[]>;
}

interface Window {
	showOpenFilePicker(options?: OpenFilePickerOptions): Promise<FileSystemFileHandle[]>;
	showSaveFilePicker(options?: SaveFilePickerOptions): Promise<FileSystemFileHandle>;
	showDirectoryPicker(options?: DirectoryPickerOptions): Promise<FileSystemDirectoryHandle>;
}

interface OpenFilePickerOptions {
	multiple?: boolean;
	types?: FilePickerAcceptType[];
	excludeAcceptAllOption?: boolean;
	startIn?:
		| FileSystemHandle
		| 'desktop'
		| 'documents'
		| 'downloads'
		| 'music'
		| 'pictures'
		| 'videos';
}

interface DirectoryPickerOptions {
	startIn?:
		| FileSystemHandle
		| 'desktop'
		| 'documents'
		| 'downloads'
		| 'music'
		| 'pictures'
		| 'videos';
	mode?: 'read' | 'readwrite';
}
