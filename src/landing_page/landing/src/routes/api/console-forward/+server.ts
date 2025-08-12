import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const { level, message, timestamp, url } = await request.json();

		// Format the message for terminal output
		const formattedMessage = `[BROWSER ${level.toUpperCase()}] ${timestamp} ${url}: ${message}`;

		// Log to the server console (which appears in VSCode terminal)
		switch (level) {
			case 'error':
				console.error(formattedMessage);
				break;
			case 'warn':
				console.warn(formattedMessage);
				break;
			case 'info':
				console.info(formattedMessage);
				break;
			default:
				console.log(formattedMessage);
		}

		return json({ success: true });
	} catch (error) {
		console.error('[CONSOLE-FORWARD] Error processing request:', error);
		return json({ success: false, error: 'Failed to process console message' }, { status: 500 });
	}
};
