var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    mode: "javascript",
    theme: "dracula",
    lineNumbers: true,
    matchBrackets: true,
    autoCloseBrackets: true
});
editor.setSize("800", "250");