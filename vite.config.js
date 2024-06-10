import { fileURLToPath, URL } from 'node:url'

import { createLogger, defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


const logger = createLogger();
const loggerWarn = logger.warn;

logger.warn = (msg, options) => {
  // Ignore warnings from pyodide distribution
  if (msg.includes("pyodide")) return;
  loggerWarn(msg, options);
};

// https://vitejs.dev/config/
export default defineConfig({
  base: "/tnsmartyardcalc/",
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  customLogger: logger,
  optimizeDeps: { exclude: ["pyodide"] }
})
