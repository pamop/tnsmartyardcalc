<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'

// const pyodide = ref(null)
// const jsVariable = ref('Hello from JavaScript!')

// const loadPyodide = async () => {
//   try {
//     // Load Pyodide
//     pyodide.value = await loadPyodide({
//       indexURL: "https://cdn.jsdelivr.net/pyodide/v0.21.0/full/"
//     });
//     console.log(pyodide)
//     // Load required packages
//     await pyodide.value.loadPackage(['numpy', 'pandas']);
//     console.log('Packages loaded successfully');
//   } catch (error) {
//     console.error('Failed to load Pyodide or packages:', error);
//   }
// }

// // onMounted(async () => {
// //   await loadPyodide();
// // });

// const runPythonCode = async () => {
//   // Ensure Pyodide is loaded
//   if (!pyodide.value) {
//     console.error('Pyodide is not loaded');
//     return;
//   }

//   // Set JavaScript variable to be used in Python
//   pyodide.value.globals.set('js_var', jsVariable.value);

//   // Python code to use the JavaScript variable
//   const pythonCode = `
// import js
// import numpy as np
// import pandas as pd

// js_var = js.js_var
// print(js_var)

// # Example usage of numpy and pandas
// array = np.array([1, 2, 3])
// df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
// print(array)
// print(df)
//   `;

//   // Run the Python code
//   try {
//     await pyodide.value.runPythonAsync(pythonCode);
//   } catch (error) {
//     console.error('Error running Python code:', error);
//   }
// }

// import * as utils from '@/utils.js';
// import { readCSV, DataFrame } from "danfojs"
// import { loadPyodide } from 'pyodide'
// import { loadPyodide } from "@/../public/assets/pyodide.mjs";

// let pyodide
// async function startup_py() {
//     const pyodide = await loadPyodide({
//           indexURL : "https://cdn.jsdelivr.net/pyodide/v0.21.0/full/"
//     });

//     // Load required packages
//     try {
//         await pyodide.loadPackage(['numpy', 'pandas']);
//         console.log('Packages loaded successfully');
//     } catch (error) {
//         console.error('Failed to load packages:', error);
//     }
//   pyodide = await loadPyodide({ packages: ["numpy"] })
//   await pyodide.loadPackage('numpy', {
//     checkIntegrity: false
//   })
// const micropip = pyodide.pyimport("micropip");
// let micropip = pyodide.pyimport('numpy');
// }

// async function hello_python() {
//     // let pyodide = await loadPyodide();
//     // // return pyodide.runPythonAsync(pyscript);
//     // // await pyodide.loadPackage("micropip")
//     pyodide = await loadPyodide()
//     await pyodide.loadPackage(['micropip'])
//     const namespace = pyodide.globals.get('dict')()

//     // return pyodide;
// }
// const someoneelse = null;
const computedValue = ref(0)

let ruslescript
let itreescript

// pyodide.imready(instance){
//   instance.runPython(`
//     import sys
//     sys.version
//   `);
//   console.log("i did it?");
// };

// hello_python().then((mypyodide) => {
//     mypyodide.runPython(pyscript);
//     computedValue.value = mypyodide.globals.get('computed_value');
// });

// // Access computed value from Python
// this.computedValue = pyodide.globals.get('computed_value');

const default_region = 'Kanto'
const default_type = 'Grass'
const default_zip = 37000

const result = ref('')
const heightval = ref(0)

let pyscript

const forminfo = reactive({
  region: default_region,
  type: default_type,
  zipcode: default_zip
})

// Form values for dropdowns (non-reactive)
const regions = ['Kanto', 'Johto', 'Hoen', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Galar']
const types = ['Grass', 'Water', 'Fire']

// twelve games [0,1,2,3,...,11]
const games = [...Array(12).keys()]

/// /// /// /// /// /// /// /// /// /// /// /// /// ///
// // // Form values (reactive)

// // // GET SESSION INDEX FROM JSON DATA
const filepath = 'pokedata.json'
const pokedata = ref({ dummy: 'nothing' })

// const sessions = computed(() => {
//   const validsessions = ['any'] // append other sessions to this. if user picks "any", it selects a random environment

//   Object.keys(seshindex.value).forEach((x) => {
//     if (
//       (seshindex.value[x].costCond === forminfo.costCond ||
//         forminfo.costCond === 'any') &&
//       (seshindex.value[x].resourceCond === forminfo.resourceCond ||
//         forminfo.resourceCond === 'any') &&
//       (seshindex.value[x].visibilityCond === forminfo.visibilityCond ||
//         forminfo.visibilityCond === 'any')
//     ) {
//       validsessions.push(x)
//     }
//   })
//   return validsessions
// })

onMounted(async () => {
  // in here, do the await data fetching
  const response = await fetch(filepath)
  pokedata.value = await response.json()

  //   await loadPyodide();

  // let pyodide = await loadPyodide();
  // pyscript = await fetch('example.py')
  //     .then(response => response.text())

  //   startup_py().then(() => {
  //     console.log('pyodide initiated')
  //   })

  //   pyodide.runPython(`
  //         import sys
  //         sys.version
  //     `)
  //   console.log('i did it?')

  ruslescript = await fetch('calculator_utils/calculator.py').then((response) => response.text())

  // console.log(ruslescript);

  // pyodide.runPython(pyscript);
  // // Access computed value from Python
  // computedValue.value = pyodide.globals.get('computed_value');

  // // const pyscript = await fetch('/example.py')
  // // fetch('/example.py')
  // //     .then(response => response.text())
  // //     .then(script => {
  // //     pyodide.runPython(script);
  // //     // Access computed value from Python
  // //     computedValue.value = pyodide.globals.get('computed_value');
  // //     })
})

// in component
function calculateRUSLEValues() {
  // use zipcode from form into python script

  console.log('Calculating...')
  runPythonCode()
  // hello_python().then(() => {
  //     pyodide.runPython(ruslescript);
  //     computedValue.value = pyodide.globals.get('computed_value');

  // });
  console.log(result)
  return
}

// in component
function calculatePokeHeight() {
  console.log('Calculating...')
  // regionrows = pokedata.value.filter(item => item.region == forminfo.region) // Finds all rows that satisfy this condition
  // typeinregion = regionrows.value.find(item => item.type == forminfo.type) // Finds the first "row" that satisfies this condition
  heightval.value = pokedata.value
    .filter((item) => item.region == forminfo.region)
    .find((item) => item.type == forminfo.type)
  console.log(heightval.value)
  result.value =
    'For a ' +
    forminfo.type +
    ' pokemon in ' +
    forminfo.region +
    ' region, the height is: ' +
    heightval.value.height
  return
}
// // default randomly select game from eligible list
// const selectedgame = computed(() => {
//   const seshlist = sessions.value
//   seshlist.shift()
//   const whichgame = {
//     session: seshlist[Math.floor(seshlist.length * Math.random())],
//     gamenum: games[Math.floor(games.length * Math.random())],
//   }

//   // SET SESSION if selected
//   if (forminfo.session !== 'any') {
//     whichgame.session = forminfo.session
//     console.log('which game?')
//     console.log(whichgame)
//   }

//   // SET GAMENUM
//   // if chose env, get game num via counterbalance
//   if (
//     forminfo.chooseby === 'Choose by environment' &&
//     forminfo.environment !== 'any'
//   ) {
//     const gameorder = getGameOrder(
//       seshindex.value[whichgame.session].counterbalance
//     )
//     whichgame.gamenum = gameorder.findIndex((x) => x === forminfo.environment)
//     console.log('which game?')
//     console.log(whichgame)
//   } else if (
//     forminfo.chooseby === 'Choose by game number' &&
//     forminfo.gamenum !== 'any'
//   ) {
//     // if chose gamenum, set
//     // console.log(gamenums)
//     whichgame.gamenum = gamenums.findIndex((x) => x === forminfo.gamenum) - 1
//     console.log('which game?')
//     console.log(whichgame)
//   } else {
//     console.log('truly random')
//     console.log(whichgame)
//   }

//   return whichgame
// })
</script>

<template>
  <div class="page">
    <div>
      <button @click="runPythonCode">Run Python Code</button>
    </div>
    <div class="formcontent">
      <div>
        <p>Computed value from Python: {{ computedValue }}</p>
      </div>
      <h3>Pokemon height calculator</h3>
      <br />
      <p class="is-size-6">
        Select a region and a type and I'll tell you the average height of the pokemon. I think it's
        in meters.
      </p>
      <div class="formstep">
        <FormKit
          type="text"
          label="Zip code (Tennessee only)"
          number
          name="zipcode"
          help="My value will be a number if it can be parsed by parseFloat"
          value="37000"
        />
        <FormKit
          type="select"
          label="Region"
          name="region"
          v-model="forminfo.region"
          placeholder="default_region"
          :options="regions"
        />

        <FormKit
          type="select"
          label="Type"
          name="type"
          v-model="forminfo.type"
          placeholder="default_type"
          :options="types"
        />
        <br />
        <hr />
        <br />
        <button class="button" id="calculate" @click="calculatePokeHeight">Calculate!</button>
        <button class="button" id="calculate" @click="calculateRUSLEValues">RUSLE!</button>
        <br />
        <br />

        <p>{{ result }}</p>
      </div>
    </div>
  </div>
</template>

<style>
.formstep {
  margin-top: 40px;
}

:root {
  --fk-bg-input: #fff;
  --fk-max-width-input: 100%;
}

.formbox {
  border: 1px solid #dfdfdf;
  text-align: left;
  background-color: rgb(248, 248, 248);
}

.formkit-input select {
  background-color: #fff;
}

.formcontent {
  width: 80%;
  margin: auto;
  margin-bottom: 40px;
  padding-bottom: 200px;
  text-align: left;
}
.formsectionexplainer {
  text-align: left;
  color: #777;
}
</style>
