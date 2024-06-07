<script setup>
// import HelloWorld from './components/HelloWorld.vue'
// import TheWelcome from './components/TheWelcome.vue'
// import CalculatorForm from './components/CalculatorForm.vue'
</script>

<template>
  <div>
    <button @click="runPythonCode">Run Python Code</button>
  </div>
  <!-- <CalculatorForm> </CalculatorForm> -->
  <!-- <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="Hello world!" />
    </div>
  </header>

  <main>
    <TheWelcome />
  </main> -->
</template>

<script>
export default {
  data() {
    return {
      pyodide: null,
      jsVariable: 'Hello from JavaScript!'
    };
  },
  async mounted() {
    await this.loadPyodide();
    this.ruslescript = await fetch('calculator_utils/calculator.py').then((response) => response.text());
    const { get, set } = await import(
      "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js"
    );
  },
  methods: {
    async loadPyodide() {
      try {
        // Load Pyodide
        this.pyodide = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.0/full/"
        });

        // Load required packages
        await this.pyodide.loadPackage(['numpy', 'pandas']);
        console.log('Packages loaded successfully');
      } catch (error) {
        console.error('Failed to load Pyodide or packages:', error);
      }
    },
    /**
     * Mount a folder from your native filesystem as the directory
     * `pyodideDirectory`. If `directoryKey` was used previously, then it will reuse
     * the same folder as last time. Otherwise, it will show a directory picker.
     */
    async mountDirectory(pyodideDirectory, directoryKey) {
      let directoryHandle = await get(directoryKey);
      const opts = {
        id: "mountdirid",
        mode: "readwrite",
      };
      if (!directoryHandle) {
        directoryHandle = await showDirectoryPicker(opts);
        await set(directoryKey, directoryHandle);
      }
      const permissionStatus = await directoryHandle.requestPermission(opts);
      if (permissionStatus !== "granted") {
        throw new Error("readwrite access to directory not granted");
      }
      const { syncfs } = await pyodide.mountNativeFS(
        pyodideDirectory,
        directoryHandle,
      );
      return syncfs;
    },
    async runPythonCode() {
      // Ensure Pyodide is loaded
      if (!this.pyodide) {
        console.error('Pyodide is not loaded');
        return;
      }

      // mount the calculator utils folder
      // const root = await navigator.storage.getDirectory();
      // console.log(root)
      // await this.pyodide.mountNativeFS("calc_utils", root);
      const dirHandle = await showDirectoryPicker();
      const permissionStatus = await dirHandle.requestPermission({
        mode: "readwrite",
      });

      if (permissionStatus !== "granted") {
        throw new Error("readwrite access to directory not granted");
      }

      const nativefs = await this.pyodide.mountNativeFS("/mount_dir", dirHandle);


      // Set JavaScript variable to be used in Python
      this.pyodide.globals.set('js_var', this.jsVariable);

      // Python code to use the JavaScript variable
      const pythonCode = `
import js
import numpy as np
import pandas as pd
# import rasterio
import os

print(os.listdir('/mount_dir'))
# js_var = js.js_var # Actually didn't need to do this explicitly
print(js_var)

# Example usage of numpy and pandas
array = np.array([1, 2, 3])
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(array)
print(df)
      `;

      // Run the Python code
      try {
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(pythonCode);
        // console.log(this.pyodide.globals.get('result').toJs());
      } catch (error) {
        console.error('Error running Python code:', error);
      }
    }
  }
};
</script>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
