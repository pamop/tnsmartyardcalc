<script setup>
import { get, set } from "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js";
import { ref, reactive } from 'vue';
</script>

<template>
  <div class="font-sans container mx-auto py-4">
    <div class="flex">
      <a href="https://tnyards.utk.edu/"><img src="/tnsy_logo.png" width="400" class="object-center" alt="Tennessee Smart Yard logo"/></a>
    </div>
    <h1 class="text-2xl container">
      Calculate the value of native plants in your Tennessee yard.
    </h1>
    <br>
    <div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="TNSY x SSMV Actions Taken by Zip Code" src="//vanderbilt.maps.arcgis.com/apps/Embed/index.html?webmap=a613aebc697f49039ec2dc7aa3f8cac1&extent=-90.7103,33.9863,-80.9214,37.8029&zoom=true&previewImage=false&scale=true&details=true&legendlayers=true&active_panel=details&disable_scroll=true&theme=light"></iframe></div>
    <br>
    <div container mx-auto px-4>
      <h2 class="text-3xl">
        Erosion calculator
      </h2>
      <FormKit 
        type="form"
        submit-label="Calculate"
        @submit="runErosionCode"
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
        <pre wrap>{{ erosion_response }}</pre>
      </div>
      <div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="Action Hot Spot Map" src="//vanderbilt.maps.arcgis.com/apps/Embed/index.html?webmap=7fbb73aadf754d0f98a63dc98fcd434d&extent=-90.7103,33.9863,-80.9214,37.8029&zoom=true&previewImage=false&scale=true&details=true&legendlayers=true&active_panel=details&disable_scroll=true&theme=light"></iframe></div>
    </div>
    <br>
    <hr>
    <br>
    <div container mx-auto px-4 py-4>
      <h2 class="text-3xl">
        Tree and Native Plants Information
      </h2>
      <p>Learn about the trends of trees and native plants in TN Smart Yards in your zipcode.</p>
      <FormKit 
        type="form"
        submit-label="Submit"
        @submit="runTreeCode"
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
          v-model="treeforminfo.zipcode"
          help="Enter your Tennessee zipcode"
          placeholder="37027"
        />
      </FormKit>
      <div>
        <pre wrap>{{ tree_response }}</pre>
        <br>
        <pre wrap>{{ nativeplant_response }}</pre>
      </div>
    </div>
  </div>
  <hr>
  <br>
  <h1 class="text-2xl container flex justify-center py-2">
    Built by a student team at the School for Science and Math at Vanderbilt.
  </h1>
  <h1 class="text-1xl container flex justify-center">
    <a href="https://github.com/pamop/tnsmartyardcalc">source code on github</a>
  </h1>
  <div class="container flex justify-center items-center py-4">
    <a href="https://www.vanderbilt.edu/cseo-ssmv/"><img src="/ssmv_logo.png" width="400" alt="School for Science and Math at Vanderbilt logo"/></a>
  </div>
  <br>
</template>

<script>
export default {
  data() {
    return {
      directoryKey: "my-directory-key",
      pyodide: null,
      jsVariable: 'Hello from JavaScript!',

      erosion_response: ref(""),
      tree_response: ref(""),
      nativeplant_response: ref(""),

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
      }),

      treeforminfo: reactive({
        zipcode: 37207,
      })
    };
  },
  async mounted() {
    await this.loadPyodide();
    // Access calculator utils
    let zipResponse = await fetch('https://pamop.github.io/tnsmartyardcalc/calculator_utils.zip');
    let zipBinary = await zipResponse.arrayBuffer();
    this.pyodide.unpackArchive(zipBinary, "zip");

    this.ruslescript = await fetch('calculator_utils/ruslecalculator.py').then((response) => response.text());
    this.treescript = await fetch('calculator_utils/treecalculator.py').then((response) => response.text());

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
    async runErosionCode() {
      // Ensure Pyodide is loaded
      if (!this.pyodide) {
        console.error('Pyodide is not loaded');
        return;
      }

      // Set JavaScript variable to be used in Python
      this.pyodide.globals.set('js_var', this.jsVariable);

      this.pyodide.globals.set('zipcode', parseInt(this.forminfo.zipcode));
      this.pyodide.globals.set('area', parseFloat(this.forminfo.area));
      this.pyodide.globals.set('slope_percentage', parseFloat(this.forminfo.slope_percentage));
      this.pyodide.globals.set('slope_length', parseFloat(this.forminfo.slope_length));
      this.pyodide.globals.set('percentNative', parseFloat(this.forminfo.nativeplants)/100);

      // this.pyodide.globals.set('erosion_response', this.erosion_response.value);


      // Run the Python code
      try {
        // await this.pyodide.runPythonAsync(pythonCode);
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(this.ruslescript);
        // console.log(this.pyodide.globals.get('erosion_response').toJs());
        this.erosion_response = this.pyodide.globals.get('erosion_response');

      } catch (error) {
        console.error('Error running Python code:', error);
        this.erosion_response = "Error: please check your inputs are valid!"
      }
    },
    async runTreeCode() {
      // Ensure Pyodide is loaded
      if (!this.pyodide) {
        console.error('Pyodide is not loaded');
        return;
      }

      // Set JavaScript variable to be used in Python
      this.pyodide.globals.set('zipcode', parseInt(this.treeforminfo.zipcode));

      // Run the Python code
      try {
        // await this.pyodide.runPythonAsync(pythonCode);
        // await this.pyodide.runPythonAsync(pythonCode);
        await this.pyodide.runPythonAsync(this.treescript);
        // console.log(this.pyodide.globals.get('erosion_response').toJs());
        this.tree_response = this.pyodide.globals.get('tree_response');
        this.nativeplant_response = this.pyodide.globals.get('nativeplant_response');

      } catch (error) {
        console.error('Error running Python code:', error);
        this.tree_response = "Error: your zip code doesn't appear to be in Tennessee."
      }
    }
  }
};

</script>


<style scoped>
a:link {
  color: teal;
  background-color: transparent;
  text-decoration: underline;
}
a:visited {
  color: darkslategray;
  background-color: transparent;
  text-decoration: none;
}
a:hover {
  color: goldenrod;
  background-color: transparent;
  text-decoration: underline;
}
a:active {
  color: gold;
  background-color: transparent;
  text-decoration: underline;
}

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
