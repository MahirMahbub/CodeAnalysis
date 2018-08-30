import re


def modification_for_control_flow_graph(path):
    with open(path, 'rb') as f:  # opening the given file using path.
        data = f.read()  # reading raw data
        text = data.decode('utf-8')  # Decoding the data in a "file string" using utf-8 mode.

    with open('raw2.txt', 'wb') as f:  # writting back text to a temporary Simple text file.
        f.write(text.encode('utf-8'))

    text = open('raw2.txt', 'r+')  # opening the text file to modify the content for further use
    #temp1 = text.read().replace("}", "\n}\n")  # Erasing newline feed/quotation.
    temp1 = text.read()
    temp1 = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", temp1)  # remove all comments (/*COMMENT */) from string
    temp1 = re.sub(re.compile("//.*?\n"), "", temp1)  # remove all singleline comments (//COMMENT\n ) from string
    replace = re.compile(r'\s+{')
    temp2 = replace.sub(' {', temp1)
    #temp2 = temp1.replace("{", "{\n")
    #temp2 = temp2.replace("{/n", "{")
    # temp2 = temp2.replace(";", ";\n")
    # temp2 = temp2.replace(";", ";\n")
    # temp2 = temp2.replace(";", ";\n")
    #replaceit = re.compile(r'/n{')
    #temp2 = replace.sub('{', temp1)
    temp3 = temp2.replace("}", "\n}\n")
    replacespace = re.compile(r'\n$')  # r'='Replacing two or more continuous space by a single space
    temp4 = replacespace.sub('', temp3)
    spacereplace = re.compile(r'^\s')
    temp5 = spacereplace.sub("",temp4)
    #spacereplace = re.compile(r'\s\(')  # Replacing " (" with "("
    # temp4 = replace.sub('(', temp3)
    #print(temp5)
    with open('modifiedText.txt', 'wb') as f:  # writting back text to a temporary Simple text file.
        f.write(temp5.encode('utf-8'))
    parsing()

def userDefinedFunctionSeperation(temp):

    userFunction = re.compile(
        r'(public|protected|private|static|\s)+[\w\<[A-Za-z,\]*\>\[\]]*\s+(\w+) *\(([^\)]*)\) *(\({?|[^;])')
    #previously used REGEX1 with fault(public|private|protected)* (void|int|float|double|String|\w+)* (\w+)\(
    #previously used REGEX1 with fault(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])

    '''seperating userDefined functions in a list named "userdefined" '''
    ara = userFunction.findall(temp)
    #print(ara)
    #userdefined=[]
    for i in range(len(ara)):
        # print(ara[i][-1])
        #if ara[i][-1] == "{" and not ara[i][-3] == 'main' and not ara[i][-3] == 'toString' and not ara[i][-3] == 'Main' :
        if ara[i][-1] == "{" :
            if not ara[i][-3] in javaKeyword:
            #Seperate Userdefined Function as Class.User_Defined_function at list named userdefined
                userdefined.append(ara[i][-3])
    #print(userdefined)



def function_body_seperation(temp):
    replace = re.compile(r'\(')
    temp22 = replace.sub(' ( ', temp)
    # replace = re.compile(r'\.')
    # temp22 = replace.sub(' . ', temp)
    dictionary = {}
    # print(userdefined)
    for userfunc in userdefined:  # iterate the "userdefined" (User Defined func name list)
        stack = []
        tempfuncname = userfunc
        try:
            indexxpos = temp22.index(tempfuncname)
        except ValueError:
            indexxpos = -1
        if indexxpos >= 0:
            lastindex = None
            firstindex = None
            while indexxpos < len(temp22):

                if temp22[indexxpos] == '{':
                    stack.append(['{', indexxpos])
                elif temp22[indexxpos] == '}':

                    if (len(stack) == 1):
                        lastindex = indexxpos
                        firstindex = stack[0][1]
                        # print(temp22[firstindex:lastindex+1])
                        dictionary[userfunc] = temp22[firstindex:lastindex + 1]
                        break
                    elif (len(stack) > 1):

                        stack.pop()
                    else:
                        pass
                indexxpos += 1

        else:
            pass
    #print(dictionary)
    return dictionary
def function_seperation(text):
    leftindex = text.find("{");  # find first "{"
    rightindex = text.rfind("}");  # and last "}" for class body

    # print(temp5[leftindex + 1:rightindex])
    class_body = text[leftindex + 1:rightindex]
    #print(class_body)
    userDefinedFunctionSeperation(class_body)
    function_body_dict = function_body_seperation(class_body)
    control_flow_graph(function_body_dict)

def flow_sequence(text_list):
    sequence_dict = [[]]
    #print(text_list)
    final_list = []
    identifier = [("start", 0)]
    if_found = -1
    index = 0
    #final = []
    #print(text_list)
    for index, line in enumerate(text_list):
        if index == 0:
            continue
        if "if " in line and  not "else if " in line:
            sequence_dict.append([])
            identifier.append(("if", index))
            if_found = index
        if "for " in line :
            sequence_dict.append([])
            identifier.append(("for", index))
        if "do " in line :
            sequence_dict.append([])
            identifier.append(("do", index))
        if 'while ' in line:
            sequence_dict.append([])
            identifier.append(("while", index))

        if 'else if ' in  line :
            if not if_found == -1:
                sequence_dict.append([if_found])
                identifier.append(("else if", index))
        elif 'else' in line:
            if not if_found == -1:
                sequence_dict.append([if_found])
                if_found = -1
                identifier.append(("else", index))
        if '}' in line:
            for i in sequence_dict:
                i.append(index)
                #print(index)
            try:
                iden = identifier.pop()
                final = sequence_dict.pop()

            except IndexError:
                continue

            if iden[0] == "for":
                #print("YEAH", index+1)
                #final.insert(-2,index+1)
                #final.append(index)
                final.append(final[0])
            if iden[0] == "while":
                final.append(final[0])
                final.append(index + 1)
            if iden[0] == "do":
                final.append(final[0])
                final.append(index + 1)
            final_list.append(final)
        else:
            for i in sequence_dict:
                #print(index+1)
                i.append(index)
                #print("


                # Sequence" + str(sequence_dict))
    #
    for i in sequence_dict:
        i.append(index+1)
    for i in sequence_dict:
        final_list.append(i)


        # elif 'break' in line:
        #     mini = []
        #     try:
        #         indexs  = identifier[::-1].index("for")
        #         mini.append((len(identifier) - 1 - indexs , "for"))
        #     except IndexError:
        #         pass
        #     try:
        #         indexs  = identifier[::-1].index("while")
        #         mini.append((len(identifier) - 1 - indexs , "while"))
        #     except IndexError:
        #         pass
        #
        #     try:
        #         indexs  = identifier[::-1].index("do")
        #         mini.append((len(identifier) - 1 - indexs , "do"))
        #     except IndexError:
        #         pass
        #     big = sorted(mini)[-1]
    print(text_list)
    print(final_list)

    #
    #
    # sequence_dict.pop()
    # final_list.append(identifier.pop())

def control_flow_graph(function_body_dict):
    for key, funcbody in function_body_dict.items():
        #print(key)
        # print()
        import io
        buf = io.StringIO(funcbody)
        lines = buf.readlines()
        lines_list = []
        for i in lines:
            replace = re.compile(r'^\s+')
            i = replace.sub('', i)
            if not i == '' or i == ' ':
                #print(i, end= '')
                lines_list.append(i)

                #print(*lines_list)
        flow_sequence(lines_list)
        print()


def parsing():
    text = open('modifiedText.txt', 'r+')
    text_body = text.read()
    function_seperation(text_body)

javaKeyword = ["catch", "continue", "for", "new", "switch", "default", "goto", "package", "synchronized", "do",
                   "if", "private", "this", "double", "implements", "protected", "throw", "else", "import", "public",
                   "throws", "enum", "instanceof", "return", "transient", "extends", "int", "short", "try", "final",
                   "interface", "static", "void", "finally", "long", "strictfp", "volatile", "float", "native","while"]
userdefined = []
modification_for_control_flow_graph(r"E:\6th Semester\604-Artificial Intelligence\alpha\spam\src\spam\Hyp.java")
