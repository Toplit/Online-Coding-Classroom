$(function(){
    // Configurations for the code input CodeMirror
    var editor = CodeMirror.fromTextArea(document.getElementById('editor_input'), {
        mode: "javascript", // Mode gets overwritten in the view
        theme: "dracula",
        lineNumbers: true,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
    });
    editor.setSize("90%", "90%");

    // Configurations for the code output CodeMirror
    var output = CodeMirror.fromTextArea(document.getElementById('editor_output'), {
        mode: "markdown", // Mode is always markdown for consistency
        theme: "dracula",
        lineNumbers: true,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        readOnly: true, // Read only as the user should not change the output 
    });
    output.setSize("90%", "90%");

    
});
