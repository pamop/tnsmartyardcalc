<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'
// import * as utils from '@/utils.js';
// import { readCSV, DataFrame } from "danfojs"
// import { loadPyodide } from "pyodide";
import { loadPyodide } from "../public/assets/pyodide.mjs";

async function hello_python() {
  let pyodide = await loadPyodide();
  return pyodide.runPythonAsync("1+1");
}

hello_python().then((result) => {
  console.log("Python says that 1+1 =", result);
});


// const dfd = require("danfojs")
const default_region = "Kanto"
const default_type = "Grass"

const result = ref("")
const heightval = ref(0)

const forminfo = reactive({
  region: default_region,
  type: default_type,
})


// Form values for dropdowns (non-reactive)
const regions = [
    'Kanto',
    'Johto',
    'Hoen',
    'Sinnoh',
    'Unova',
    'Kalos',
    'Alola',
    'Galar'
]
const types = [
    'Grass',
    'Water',
    'Fire'
]

// twelve games [0,1,2,3,...,11]
const games = [...Array(12).keys()]

/// /// /// /// /// /// /// /// /// /// /// /// /// ///
// // // Form values (reactive)

// get pokemon height from csv
// const filepath = 'pokenmon_longformat.csv' // it's in public/
// // import csv as dataframe using danfo.js
// readCSV("/home/Desktop/titanic.csv")
//   .then(df => {

//    //do something with the CSV file
//    df.head().print()

//   }).catch(err=>{
//      console.log(err);
//   })

// // // GET SESSION INDEX FROM JSON DATA
const filepath = 'pokedata.json'
const pokedata = ref({ dummy: 'nothing' })

const sessions = computed(() => {
  const validsessions = ['any'] // append other sessions to this. if user picks "any", it selects a random environment

  Object.keys(seshindex.value).forEach((x) => {
    if (
      (seshindex.value[x].costCond === forminfo.costCond ||
        forminfo.costCond === 'any') &&
      (seshindex.value[x].resourceCond === forminfo.resourceCond ||
        forminfo.resourceCond === 'any') &&
      (seshindex.value[x].visibilityCond === forminfo.visibilityCond ||
        forminfo.visibilityCond === 'any')
    ) {
      validsessions.push(x)
    }
  })
  return validsessions
})

onMounted(async () => {
    // axios
    //     .get('/pokemon_longformat.csv',{ responseType: 'blob',})
    //     .then((response) => {
    //     pokedata = response.data
    //     })

    //     pokedata.text().then((csvStr) => {
    //         console.log(csvStr);
    //     })
    const response = await fetch(filepath)
    pokedata.value = await response.json()
    console.log(pokedata.value)
    console.log(pokedata.value.filter(item => item.region == "Galar"))
    
})

// const result = computed((reg,typ) => {

// })
// in component
function calculatePokeHeight() {
    console.log("Calculating...")
    // regionrows = pokedata.value.filter(item => item.region == forminfo.region) // Finds all rows that satisfy this condition
    // typeinregion = regionrows.value.find(item => item.type == forminfo.type) // Finds the first "row" that satisfies this condition
    heightval.value = pokedata.value.filter(item => item.region == forminfo.region).find(item => item.type == forminfo.type)
    console.log(heightval.value)
    result.value = 'For a ' + forminfo.type + ' pokemon in ' + forminfo.region + ' region, the height is: ' + heightval.value.height
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
    <div class="formcontent">
      <h3>Pokemon height calculator</h3>
      <br />
      <p class="is-size-6">
        Select a region and a type and I'll tell you the average height of the pokemon. I think it's in meters. 
      </p>
      <div class="formstep">
        
        <FormKit
        type="select"
        label="Region"
        name="region"
        v-model="forminfo.region"
        placeholder=default_region
        :options="regions"
        />

        <FormKit
        type="select"
        label="Type"
        name="type"
        v-model="forminfo.type"
        placeholder=default_type
        :options="types"
        />
        <br>
        <hr />
        <br>
        <button
            class="button"
            id="calculate"
            @click="calculatePokeHeight"
        >
            Calculate!
        </button>

        <br>
        <br>

        <p>{{result}}</p>
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