
const colour_codes = {
   "BLACK":"[30m",
   "RED":"[31m",
   "GREEN":"[32m",
   "YELLOW":"[33m",
   "BLUE":"[34m",
   "MAGENTA":"[35m",
   "CYAN":"[36m",
   "WHITE":"[37m",
   "GREY":"[90m",
   "BOLD":"[1m",
   "DIM":"[2m",
   "ITALIC":"[3m",
   "UNDERLINE":"[4m",
   "BLINK":"[5m",
   "INVERT":"[7m",
   "STRIKETHROUGH":"[9m",
   "RESET":"[0m",
}


let input_buffer = ""
let temp_input_buffer = ""
let is_inputting = false

const input_prompt = document.getElementById("input_prompt");
const input_box = document.getElementById("input");
const output_div = document.getElementById("output")
const input_container = document.getElementsByClassName("quiz-input-container")[0]
function translate_colours(text){
    // Loop through the colour codes
    for (const [key, value] of Object.entries(colour_codes)) {
        while (text.includes(value)){
            text = text.replace(value, `<span class="colour-code-${key.toLowerCase()}">`)
            text += "</span>"
        }
    }
    return text
}

function print(text){

    // Log the text to console
    console.log(text);

    // Convert the ANSI colour codes into html spans
    text = translate_colours(text)

    // Create a new line
    output_div.innerHTML += text + "<br>";
}
eel.expose(print);

function clear_screen(){
    // Clear the output
    output_div.innerHTML = ""
    
    // Scroll to top
    output_div.scrollIntoView()
}
eel.expose(clear_screen);

function get_input(prompt){
    // Set the prompt
    input_prompt.innerHTML = translate_colours(prompt)

    // If not waiting for the user to press enter
    if (!is_inputting){

        // Define a handler
        function input_handler(e){

            // Update the input buffer with the new input
            temp_input_buffer = input_box.value
             
            // If the key is not enter then continue
            if (e.key != "Enter"){
                return
             }

             // Store the input
             input_buffer = input_box.value
             
             // If the user has entered nothing 
             if (input_buffer == ""){
                 // Make sure the loop breaks as the python side input waits for the input buffer to not be empty
                 input_buffer = " "
             }

            // Stop listing to keypress as no longer waiting for input 
            input_box.removeEventListener("keypress", input_handler)
            is_inputting = false
        }

        // Register the handler as a listener
        input_box.addEventListener("keypress", input_handler)

        // Wait for input
        is_inputting = true
    }

    // Return the input to python
    return input_buffer

}
eel.expose(get_input);

function force_get_input(){
    // Returns what ever is already in the input box
    return temp_input_buffer
}
eel.expose(force_get_input);

function clear_input_buffer(){
    input_buffer = ""
    temp_input_buffer = ""
    document.getElementById("input").value = ""
}
eel.expose(clear_input_buffer)

function choose_item(option){
    // Set the input buffer to the id of the button that was pressed
    input_buffer = option.id
    temp_input_buffer = input_buffer
    document.getElementById("input").value = input_buffer
    
    // Scroll to the input
    document.getElementById("input").scrollIntoView()
}

function close_window(){
    // Called by python to close the window
    window.close()
}
eel.expose(close_window)

function set_title(title){
    // Called by python to set the title of the menu
    document.title = "Quiz Game UI | " + title
}
eel.expose(set_title)

// Make sure the window is big enough
if (window.outerWidth < 1600 || window.outerHeight < 900){
    window.resizeTo(1600, 900);
}

function close_python_and_window(){
    // Initiate the python shutdown
    eel.close_python()
}


function highlight_input(){
    addTargetingClass();
    
    setTimeout(function() {
        removeTargetingClass();
    }, 3000);
  }
eel.expose(highlight_input);

input_box.click(highlight_input);
  
  function addTargetingClass() {
    input_container.classList.add('target-highlight');
  }
  
  function removeTargetingClass() {
    input_container.classList.remove('target-highlight');
  }