


function populate_list_with_text(input_id, ul_id){
    let node = document.createElement("LI");
    node.id = "js-propery"
    let subject_text = document.getElementById(input_id)
    if (subject_text.value.length > 0){
        let textnode = document.createTextNode(subject_text.value);         // Create a text node
        node.appendChild(textnode);                      // Append the text to <li>
        document.getElementById(ul_id).appendChild(node);     // Append <li> to <ul> 
        subject_text.value = ""
    }
}

function change_site_setting(setting, Url){
    $(document).ready(function(){
        $("#button").click(function(){
            $.ajax({
                url: Url,
                type: "GET",
                success: function(result){
                    document.getElementById(setting).innerHTML = result
                    console.log(result)
                },
                error: function(error){
                    console.log("didn't work")
                }
            })
        })
    })
    return true
}
