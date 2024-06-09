<script setup>
// import HelloWorld from './components/HelloWorld.vue'
// import TheWelcome from './components/TheWelcome.vue'
// import CalculatorForm from './components/CalculatorForm.vue'
import { get, set } from "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js";
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
      directoryKey: "my-directory-key",
      pyodide: null,
      jsVariable: 'Hello from JavaScript!'
    };
  },
  async mounted() {
    await this.loadPyodide();
    // Access calculator utils
    let zipResponse = await fetch('https://pamop.github.io/tnsmartyardcalc/calculator_utils.zip');
    let zipBinary = await zipResponse.arrayBuffer();
    this.pyodide.unpackArchive(zipBinary, "zip");

    this.pyscript = await fetch('@/calculator_utils/calculator.py').then((response) => response.text());
  },
  methods: {
    async loadPyodide() {
      try {
        // Load Pyodide
        this.pyodide = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.0/full/"
        });

        // Load required packages
        await this.pyodide.loadPackage(['micropip']);
        const micropip = this.pyodide.pyimport('micropip');
        // await micropip.install('/rasterio-1.3.10-cp312-cp312-manylinux2014_x86_64.whl')
        // console.log('Packages loaded successfully');
      } catch (error) {
        console.error('Failed to load Pyodide or packages:', error);
      }
    },
    /**
     * Mount a folder from your native filesystem as the directory
     * `pyodideDirectory`. If `directoryKey` was used previously, then it will reuse
     * the same folder as last time. Otherwise, it will show a directory picker.
     */
     async mountDirectory(pyodide, pyodideDirectory, directoryKey) {
      try {
        let directoryHandle = await get(directoryKey);
        const opts = {
          id: "mountdirid",
          mode: "readwrite",
        };
        if (!directoryHandle) {
          console.log('No directory handle found, requesting a new one...');
          directoryHandle = await showDirectoryPicker(opts);
          await set(directoryKey, directoryHandle);
        } else {
          // Check if the directory is already mounted and unmount it first
          try {
            if (pyodide.FS.isDir(pyodide.FS.lookupPath(pyodideDirectory).node.mode)) {
              pyodide.FS.unmount(pyodideDirectory);
              console.log('Unmounted existing directory at:', pyodideDirectory);
            }
          } catch (e) {
            console.warn('Directory was not mounted:', e);
          }
        }
        const permissionStatus = await directoryHandle.requestPermission(opts);
        if (permissionStatus !== "granted") {
          throw new Error("readwrite access to directory not granted");
        }
        const { syncfs } = await pyodide.mountNativeFS(
          pyodideDirectory,
          directoryHandle
        );
        console.log('Directory mounted at:', pyodideDirectory);
        return syncfs;
      } catch (error) {
        console.error('Failed to mount directory:', error);
        throw error;
      }
    },
    async runPythonCode() {
      // Ensure Pyodide is loaded
      if (!this.pyodide) {
        console.error('Pyodide is not loaded');
        return;
      }

      // // mount the calculator utils folder
      // const dirHandle = await showDirectoryPicker();
      // console.log(dirHandle)
      // const permissionStatus = await dirHandle.requestPermission({
      //   mode: "readwrite",
      // });

      // if (permissionStatus !== "granted") {
      //   throw new Error("readwrite access to directory not granted");
      // }

      // const nativefs = await this.pyodide.mountNativeFS("/mount_dir", dirHandle);

      // const nativefs = await this.mountDirectory(this.pyodide, "/mount_dir", this.directoryKey);

      

      // Set JavaScript variable to be used in Python
      this.pyodide.globals.set('js_var', this.jsVariable);

      // Python code to use the JavaScript variable
      const pythonCode = `
import js
import micropip
import sys
await micropip.install("pandas")
import pandas as pd
import os

print(os.listdir('/home/pyodide/calculator_utils'))
dir_path = '/home/pyodide/calculator_utils'
# js_var = js.js_var # Actually didn't need to do this explicitly
print(js_var)

tnzips = pd.read_csv(dir_path + '/tn_zipcodes.csv') # zip codes and corresponding counties and lat/long coords
lsdf = pd.read_csv(dir_path + '/ls_values.csv') # ls values given slope percent and length

# result = js.forminfo.zipcode.value + 5000
# print(result)
print(tnzips.loc[tnzips['zip']==37212,'county'].values[0])

# Example usage of numpy and pandas
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(df)
      `;

      // Run the Python code
      try {
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(pythonCode);
        // await this.pyodide.runPythonAsync(this.pyscript);
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
