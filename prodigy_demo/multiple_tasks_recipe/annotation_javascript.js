// Code to set the first label of the NER task as default
let prevHash = null
document.addEventListener('prodigyupdate', v => {
    const { task } = event.detail
    // Select the label input for the given default label
    const defaultLabel = document.querySelector('input[value="Weather"]')
    if (task._task_hash !== prevHash) {  // the displayed task has changed
        defaultLabel.click()  // simulate click
        prevHash = task._task_hash
    }

})

// Implementing the keybinding for the chekbox
// if user clicks 's' then it checks the checkbox
document.querySelector('#root').addEventListener('keyup', function(event) {
    if (event.keyCode === 83) {  // key code for character "s": https://www.cambiaresearch.com/articles/15/javascript-char-codes-key-codes
        document.getElementById("sarcasm").click();
    }
})