let {VM} = require("vm2");
const vm = new VM();

$(function(){

    $("#run").click(function(){
        vm.run('console.log(1+2);');
    });
});