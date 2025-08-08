# Troubleshooting Guide

## Vite Dependency Optimization Issues

### "504 Outdated Optimize Dep" Error

If you encounter a "504 Outdated Optimize Dep" error in your Vite application, this indicates that Vite's dependency optimization system has detected that a dependency has changed but the optimized version hasn't been updated.

#### What Causes This Error?

1. **Dependency Changes**: When you install or update dependencies, Vite needs to re-optimize them.
2. **Vite Cache Issues**: Sometimes Vite's cache becomes corrupted or out of sync.
3. **Dynamic Imports**: Dynamic imports (`import()`) can sometimes cause issues with Vite's optimization system, especially for large libraries.
4. **HMR Timeouts**: Hot Module Replacement (HMR) timeouts can occur when processing large dependencies.

#### How to Fix It

1. **Clear Vite's Cache**:

   ```bash
   # Use our custom script for a deep clean
   npm run clean:deep

   # Or use the standard clean script
   npm run clean
   ```

2. **Restart the Development Server**:

   ```bash
   # With a clean cache
   npm run dev:reset

   # Or standard restart
   npm run dev
   ```

3. **Update Vite Configuration**:

   - Make sure the problematic dependency is included in the `optimizeDeps.include` array in `vite.config.ts`.
   - Consider increasing timeouts for HMR and other operations.

4. **Avoid Dynamic Imports for Problematic Libraries**:
   - Use direct imports instead of dynamic imports for libraries that cause issues.
   - For example, use `import html2canvas from 'html2canvas'` instead of `const html2canvas = await import('html2canvas')`.

## html2canvas Specific Issues

html2canvas is a complex library that can cause issues with Vite's dependency optimization system. Here are some specific troubleshooting steps:

### Loading Failures

If html2canvas fails to load, try these approaches:

1. **Use Direct Import**:

   ```typescript
   import html2canvas from "html2canvas";
   ```

2. **CDN Fallback**:

   ```typescript
   // If the bundled version fails, load from CDN
   const loadFromCDN = () => {
     const script = document.createElement("script");
     script.src =
       "https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js";
     document.head.appendChild(script);
     return new Promise((resolve) => {
       script.onload = () => resolve(window.html2canvas);
     });
   };
   ```

3. **Pre-bundle the Library**:
   - Add html2canvas to the `optimizeDeps.include` array in `vite.config.ts`.
   - Use the `build.rollupOptions.output.manualChunks` option to create a separate chunk for html2canvas.

### Rendering Issues

If html2canvas renders incorrectly or not at all:

1. **Check Element Visibility**:

   - Make sure the element you're trying to render is visible in the DOM.
   - Elements with `display: none` or zero dimensions won't render properly.

2. **Cross-Origin Issues**:

   - Set `useCORS: true` and `allowTaint: true` in the html2canvas options.
   - Make sure any images or resources used in the element have proper CORS headers.

3. **Styling Issues**:
   - Some CSS features may not be supported by html2canvas.
   - Test with simpler styling to isolate the issue.

## Dynamic Import Failures

If you encounter errors with dynamic imports:

1. **Use Static Imports**: Replace dynamic imports with static imports where possible.

2. **Preload Important Modules**: Use Vite's `modulePreload` option to preload important modules.

3. **Check for Circular Dependencies**: Circular dependencies can cause issues with dynamic imports.

## General Vite Troubleshooting

1. **Check for Vite Updates**:

   ```bash
   npm update vite @sveltejs/kit @sveltejs/vite-plugin-svelte
   ```

2. **Inspect Network Requests**:

   - Use the browser's developer tools to inspect network requests.
   - Look for 404, 500, or other error responses.

3. **Enable Verbose Logging**:

   - Set `logLevel: 'info'` in `vite.config.ts` to see more detailed logs.

4. **Check for Plugin Conflicts**:

   - Disable plugins one by one to identify if a specific plugin is causing issues.

5. **Rebuild Node Modules**:
   ```bash
   rm -rf node_modules
   npm install
   ```

## When All Else Fails

If you've tried all the above and still have issues:

1. **Create a Minimal Reproduction**: Create a minimal project that reproduces the issue.

2. **Check GitHub Issues**: Check if others have reported similar issues on the Vite or html2canvas GitHub repositories.

3. **Ask for Help**: Post your issue on Stack Overflow or the Vite Discord server with a clear description and reproduction steps.
