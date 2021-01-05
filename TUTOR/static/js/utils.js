


function populate_list_with_text(input_id, ul_id){
    let node = document.createElement("LI");
    let subject_text = document.getElementById(input_id)
    if (subject_text.value.length > 0){
        let textnode = document.createTextNode(subject_text.value);         // Create a text node
        node.appendChild(textnode);                      // Append the text to <li>
        document.getElementById(ul_id).appendChild(node);     // Append <li> to <ul> 
        subject_text.value = ""
    }
}
