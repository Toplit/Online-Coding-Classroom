// $(function(){
//     $("#run_code").click(function(){
//         var test = '{% url ',get_code' %}';
//         //var untrusted_code = $("#editor_input").val();
//         var editor_input = $(".CodeMirror")[0].CodeMirror;
//         var untrusted_code = editor_input.getValue();
//         console.log("Button works");

//         $.ajax({
//             url: '{% url 'get_code' %}',
//             data: {
//                 'untrustedCode': untrusted_code
//             },
//             dataType: 'json',
//             success: function (data) {
//                 var result = data["output"]
//                 var editor_output = $(".CodeMirror")[1].CodeMirror;

//                 editor_output.setValue(result);
//             }
//         });
//     });
// });