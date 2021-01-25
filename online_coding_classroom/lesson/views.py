from django.shortcuts import render
from django.http import JsonResponse
from node_vm2 import VM, NodeVM


def select_language(request):
    """ View for Select Language page """
    context = {}

    return render(request, 'lesson/select_language.html', context)

def select_lesson(request):
    """ View for Select Lesson page """
    context = {
        # title = selected language + " Lessons"
    }

    return render(request, 'lesson/select_lesson.html', context)

def lesson(request):
    """ View for the lesson itself """



    # input_code = request.POST.get("editor_input")
    # print(input_code)
    # output_code = ""
    # Compile the inputCode
    # Store result in context
    context = {}
    return render(request, 'lesson/lesson_base.html', context) 
   
def compile_basic_code(request):
    """ Function for compiling basic code """
    print("Compiling Code\n")

    untrustedCode = request.GET.get('untrustedCode')

    js = "exports.func = " + untrustedCode

    with NodeVM.code(js) as module:
        result = module.call_member("func")

        #stringResult = ' '.join(map(str, result))
        data = {'output': result}
    return JsonResponse(data)

def compile_array_code(request):
    """ Function for compiling code that returns an array """
    print("Compiling Code\n")

    untrustedCode = request.GET.get('untrustedCode')

    js = "exports.func = " + untrustedCode

    with NodeVM.code(js) as module:
        result = module.call_member("func")

        stringResult = ' '.join(map(str, result))
        data = {'output': result}
    return JsonResponse(data)

    ###
    #  node_vm2 code examples 
    ###

    ### For JavaScript without functions - below:
            #     let arr = [4,3,2,1];
            # for(let i=0; i < arr.length; i++){
            #     for(let j=0; j < arr.length; j++){
            #         if(arr[j] > arr[j+1]){
            #             let tmp = arr[j];
            #             arr[j] = arr[j+1];
            #             arr[j+1] = tmp;
            #         }
            #     } 
            # }

    ### Use this Python:
            # with VM() as vm:
            #     vm.run(untrustedCode)
            #     print(vm.run("arr"))
            #     result = vm.run("arr")
            #     stringResult = ' '.join(map(str, result))
            #     data = {'output': stringResult}
            # return JsonResponse(data)


    ### For normal JavaScript functions - below:
            #     function bubble(){
            #     let arr = [4,3,2,1];
            #     for(let i=0; i < arr.length; i++){
            #         for(let j=0; j < arr.length; j++){
            #             if(arr[j] > arr[j+1]){
            #                 let tmp = arr[j];
            #                 arr[j] = arr[j+1];
            #                 arr[j+1] = tmp;
            #             }
            #         }
            #     }
            #     return arr;
            # }

    ### Use this Python - Set the function as an export and its returned value is output:
            # def compile_code(request):
            # print("Working\n")
            # untrustedCode = request.GET.get('untrustedCode')

            # js = "exports.bubbleFunc = " + untrustedCode

            # with NodeVM.code(js) as module:
            #     result = module.call_member("bubbleFunc")

            #     print(result)

            #     stringResult = ' '.join(map(str, result))
            #     data = {'output': stringResult}
            # return JsonResponse(data)