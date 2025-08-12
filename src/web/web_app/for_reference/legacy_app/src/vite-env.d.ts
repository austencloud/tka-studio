/// <reference types="vite/client" />
/// <reference types="vite-plugin-pwa/client" />

interface ImportMetaEnv {
  readonly VITE_SILENT_MODE: string;
  readonly VITE_SOME_OPTION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface Window {
  deferredPrompt: any;
}
