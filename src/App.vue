<script setup>
import { get, set } from "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js";
import { ref, reactive } from 'vue';
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
        @submit="runPythonCode"
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
          v-model="forminfo.zipcode"
          help="Enter your Tennessee zipcode."
          placeholder="default_zip"
        />
        <FormKit
          type="number"
          name="area"
          id="area"
          validation="required|not:Admin"
          label="Area (sq ft)"
          v-model="forminfo.area"
          help="Enter the area of your land in square feet."
          placeholder="default_area"
        />
        <FormKit
          type="number"
          name="slopepercent"
          id="slopepercent"
          step="1"
          validation="required|not:Admin"
          label="Slope percentage"
          v-model="forminfo.slope_percentage"
          help="Enter your slope percentage in a number (e.g., 40% = 40)."
          placeholder="default_slope_percentage"
        />
        <FormKit
          type="number"
          name="slopelength"
          id="slopelength"
          step="1"
          validation="required|not:Admin"
          label="Slope length (ft)"
          v-model="forminfo.slope_length"
          help="Enter the length of your slope in feet."
          placeholder="default_slope_length"
        />
        <FormKit
          type="number"
          name="nativeplants"
          id="nativeplants"
          step="1"
          validation="required|not:Admin"
          label="Percentage of land covered in native plants"
          v-model="forminfo.nativeplants"
          help="Enter the percentage of your land that has native plants growing on it."
          placeholder="default_nativeplants"
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
        {{ erosion_response }}
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
        @submit="runPythonCode"
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
      jsVariable: 'Hello from JavaScript!',

      erosion_response: ref(""),

      default_zip: 37235,
      default_area: 2500,
      default_slope_percentage: 40,
      default_slope_length: 300,
      default_nativeplants: 20,

      forminfo: reactive({
        zipcode: 37235,
        area: 2500,
        slope_percentage: 40,
        slope_length: 300,
        nativeplants: 20
      })
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

      this.pyodide.globals.set('zipcode', this.forminfo.zipcode);
      this.pyodide.globals.set('area', parseFloat(this.forminfo.area));
      this.pyodide.globals.set('slope_percentage', parseFloat(this.forminfo.slope_percentage));
      this.pyodide.globals.set('slope_length', parseFloat(this.forminfo.slope_length));
      this.pyodide.globals.set('percentNative', parseFloat(this.forminfo.nativeplants));

      // this.pyodide.globals.set('erosion_response', this.erosion_response.value);


      // Run the Python code
      try {
        // await this.pyodide.runPythonAsync(pythonCode);
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(this.pyscript);
        // console.log(this.pyodide.globals.get('erosion_response').toJs());
        this.erosion_response = this.pyodide.globals.get('erosion_response');

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
