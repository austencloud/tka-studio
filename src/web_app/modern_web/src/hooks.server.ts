import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	// Handle console forwarding endpoint
	if (event.url.pathname === '/api/console-forward') {
		if (event.request.method === 'POST') {
			try {
				const body = await event.request.text();
				const data = JSON.parse(body);
				
				// Write directly to stdout (terminal)
				const timestamp = new Date().toLocaleTimeString();
				const logLine = `[${timestamp}] BROWSER ${data.level}: ${data.message}`;
				process.stdout.write(logLine + '\n');
				
				return new Response('OK', { status: 200 });
			} catch (error) {
				return new Response('Error', { status: 500 });
			}
		}
	}

	return resolve(event);
};
