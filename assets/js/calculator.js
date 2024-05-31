const calculator = document.querySelector('.calculator')
const keys = calculator.querySelector('.calculator__keys')
const display = document.querySelector('.calculator__display')


const getKeyType = (key) => {
    const { action } = key.dataset
    if (!action) return 'number'
    if (
      action === 'add' ||
      action === 'subtract' ||
      action === 'multiply' ||
      action === 'divide'
    ) return 'operator'
    // For everything else, return the action
    return action
  }

keys.addEventListener('click', e => {
    if (!e.target.matches('button')) return // only care about button clicks
    const key = e.target // which button they pressed
    const displayedNum = display.textContent // what is currently presented on the calc
  
    // Given this button press, what should the calculator show now?
    const resultString = createResultString(key, displayedNum, calculator.dataset)
  
    // Update states
    display.textContent = resultString
    updateCalculatorState(key, calculator, resultString, displayedNum)
    updateVisualState(key, calculator)
})

const createResultString = (key, displayedNum, state) => {
    const keyContent = key.textContent
    const { action } = key.dataset
    const { firstValue, modValue, operator, previousKeyType } = state

    const keyType = getKeyType(key)
    // console.log(keyType + " in createResultsString")
    if (keyType === 'number') {
        calculator.dataset.previousKeyType = 'number'

        return displayedNum === '0' ||
        previousKeyType === 'operator' ||
        previousKeyType === 'calculate'
        ? keyContent
        : displayedNum + keyContent
        
    }
    if (keyType === 'decimal') {
        calculator.dataset.previousKeyType = 'decimal'
        if (!displayedNum.includes('.')) return displayedNum + '.'
        if (previousKeyType === 'operator' || previousKeyType === 'calculate')
          return '0.'
        return displayedNum
    }
    if (keyType === 'operator') {
        const firstValue = calculator.dataset.firstValue
        const operator = calculator.dataset.operator
        calculator.dataset.previousKeyType = 'operator'
    
        return firstValue &&
          operator &&
          previousKeyType !== 'operator' &&
          previousKeyType !== 'calculate'
          ? calculate(firstValue, operator, displayedNum)
          : displayedNum
    }
    if (keyType === 'clear') {
        if (key.textContent === 'AC') {
            calculator.dataset.firstValue = ''
            calculator.dataset.modValue = ''
            calculator.dataset.operator = ''
            calculator.dataset.previousKeyType = ''
        } else {
            key.textContent = 'AC'
        }

        display.textContent = 0
        calculator.dataset.previousKeyType = 'clear'
        return 0
    }
    if (keyType === 'calculate') {
        calculator.dataset.previousKeyType = 'calculate'

        const firstValue = calculator.dataset.firstValue
        const operator = calculator.dataset.operator
        const modValue = calculator.dataset.modValue
    
        return firstValue
          ? previousKeyType === 'calculate'
            ? calculate(displayedNum, operator, modValue)
            : calculate(firstValue, operator, displayedNum)
          : displayedNum
    }
}

const updateCalculatorState = (
    key,
    calculator,
    calculatedValue,
    displayedNum
) => {
    const keyContent = key.textContent
    const { action } = key.dataset
    const { firstValue, modValue, operator, previousKeyType } = calculator.dataset

    const keyType = getKeyType(key)
    calculator.dataset.previousKeyType = keyType
    // console.log(keyType + " in updateCalculatorState")
    Array.from(key.parentNode.children).forEach(k =>
    k.classList.remove('is-depressed')
  )
    if (keyType === 'number') {
      /* ... */
    }
    if (keyType === 'decimal') {
      /* ... */
    }
    if (keyType === 'operator') {
        let firstValue = calculator.dataset.firstValue
        key.classList.add('is-depressed')
        calculator.dataset.operator = key.dataset.action
        calculator.dataset.firstValue =
          firstValue &&
          operator &&
          previousKeyType !== 'operator' &&
          previousKeyType !== 'calculate'
            ? calculatedValue
            : displayedNum
    }
    if (keyType === 'clear') {
        if (key.textContent === 'AC') {
            calculator.dataset.firstValue = ''
            calculator.dataset.modValue = ''
            calculator.dataset.operator = ''
            calculator.dataset.previousKeyType = ''
          } else {
            key.textContent = 'AC'
          }
    }
    if (keyType === 'calculate') {
        let firstValue = calculator.dataset.firstValue
        // const operator = calculator.dataset.operator
        // let secondValue = displayedNum

        calculator.dataset.modValue =
        firstValue && previousKeyType === 'calculate' ? modValue : displayedNum
    }
    if (keyType !== 'clear') {
        const clearButton = calculator.querySelector('[data-action=clear]')
        clearButton.textContent = 'CE'
    }
}

const updateVisualState = (key, calculator) => {
    const keyType = getKeyType(key)
    Array.from(key.parentNode.children).forEach(k =>
      k.classList.remove('is-depressed')
    )
  
    if (keyType === 'operator') key.classList.add('is-depressed')
  
    if (keyType === 'clear' && key.textContent !== 'AC') {
      key.textContent = 'AC'
    }
  
    if (keyType !== 'clear') {
      const clearButton = calculator.querySelector('[data-action=clear]')
      clearButton.textContent = 'CE'
    }
}

const calculate = (n1, operator, n2) => {
    const firstNum = parseFloat(n1)
    const secondNum = parseFloat(n2)
    if (operator === 'add') return firstNum + secondNum
    if (operator === 'subtract') return firstNum - secondNum
    if (operator === 'multiply') return firstNum * secondNum
    if (operator === 'divide') return firstNum / secondNum
}
