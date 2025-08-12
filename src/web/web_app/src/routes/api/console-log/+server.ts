import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const { level, message, timestamp } = await request.json();

		// Format the log message for the server console
		const formattedMessage = `[BROWSER-${level}] ${timestamp} ${message}`;

		// Output to server console based on level
		switch (level) {
			case 'ERROR':
				console.error(formattedMessage);
				break;
			case 'WARN':
				console.warn(formattedMessage);
				break;
			default:
				console.log(formattedMessage);
				break;
		}

		return json({ success: true });
	} catch (error) {
		console.error('[SERVER] Failed to log browser message:', error);
		return json({ success: false }, { status: 500 });
	}
};
