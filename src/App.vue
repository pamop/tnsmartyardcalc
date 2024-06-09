<script setup>
// import CalculatorForm from './components/CalculatorForm.vue'
import { get, set } from "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js";
</script>

<template>
  <div class="font-sans container mx-auto py-4">
  <h1 class="text-3xl container">
    Tennessee Smart Yards Calculator
  </h1>
  <h1 class="text-2xl container">
    NOTE: Under construction!
  </h1>
  <br>
  <div container mx-auto px-4>
    <h2 class="text-2xl">
      Erosion calculator
    </h2>
  <!-- <div>
    <button @click="runPythonCode">Run Python Code</button>
  </div> -->
  <FormKit 
    type="form"
    submit-label="Calculate"
    @submit = "runPythonCode"
    :submit-attrs="{
      inputClass: 'my-input-class',
      wrapperClass: 'my-wrapper-class',
      'data-theme': `dark`,
      ignore: false
    }"
  >
    <FormKit
      type="text"
      name="zipcode"
      id="zipcode"
      validation="required|not:Admin"
      label="Zipcode"
      help="Enter your Tennessee zipcode."
      placeholder="37235"
    />
    <FormKit
      type="number"
      name="area"
      id="area"
      validation="required|not:Admin"
      label="Area (sq ft)"
      help="Enter the area of your land in square feet."
      placeholder="2500"
    />
    <FormKit
      type="number"
      name="slopepercent"
      id="slopepercent"
      step="1"
      validation="required|not:Admin"
      label="Slope percentage"
      help="Enter your slope percentage in a number (e.g., 40% = 40)."
      placeholder="40"
    />
    <FormKit
      type="number"
      name="slopelength"
      id="slopelength"
      step="1"
      validation="required|not:Admin"
      label="Slope length (ft)"
      help="Enter the length of your slope in feet."
      placeholder="2500"
    />
    <FormKit
      type="number"
      name="nativeplants"
      id="nativeplants"
      step="1"
      validation="required|not:Admin"
      label="Percentage of land covered in native plants"
      help="Enter the percentage of your land that has native plants growing on it."
      placeholder="2500"
    />
    <!-- <FormKit
      type="select"
      label="Class"
      name="class"
      id="class"
      placeholder="Select a class"
      :options="['Warrior', 'Mage', 'Assassin']"
    /> -->
    </FormKit>
    <div>
      Result from calculation: Under Construction
    </div>
  </div>
  <br>
  <hr>
  <br>
  <div container mx-auto px-4 py-4>
    <h2 class="text-2xl">
      Tree information calculator
    </h2>
  <!-- <div>
    <button @click="runPythonCode">Run Python Code</button>
  </div> -->
  <FormKit 
    type="form"
    submit-label="Submit"
    @submit = "runPythonCode"
    :submit-attrs="{
      inputClass: 'my-input-class',
      wrapperClass: 'my-wrapper-class',
      'data-theme': `dark`,
      ignore: false
    }"
    >
    <FormKit
      type="text"
      name="zipcode"
      id="zipcode"
      validation="required|not:Admin"
      label="Zipcode"
      help="Enter your Tennessee zipcode"
      placeholder="37235"
    />
    </FormKit>
    <div>
      Result from calculation:
    </div>
  </div>
  </div>

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

    this.pyscript = await fetch('calculator_utils/calculator.py').then((response) => response.text());
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
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(this.pyscript);
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
