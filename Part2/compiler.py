##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################



def checkGrammar(tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed

    def handle_section_error(tokens, index, ops, i_e_count):
        def print_error_message(message):
            print(f"Syntax error: {message}")
        
        curr_tok = tokens[index]
        prev_tok = tokens[index - 1] if index >= 1 else None
        next_tok = tokens[index + 1] if index < len(tokens) - 1 else None
        before_prev_token = tokens[index - 2] if index >= 2 else None
        after_next_token = tokens[index + 2] if index < len(tokens) - 2 else None

        if curr_tok[1] == "if":
            if next_tok == None:
                print_error_message("IF WITHOUT CONDITION")
                return False
            
            if next_tok[1] == "if" or next_tok[1] == "else":
                print_error_message("IF WITHOUT CONDITION")
                return False
            
            if next_tok[1] in ops:
                print_error_message("IF WITHOUT CONDITION")
                return False
            
            else:
                return True
        
        elif curr_tok[1] == "else":
            if i_e_count < 0:
                print_error_message("ELSE WITHOUT IF")
                return False
            if prev_tok == None:
                print_error_message("EXPECTED EXPRESSION BEFORE ELSE")
                return False
            if next_tok == None:
                print_error_message("EXPECTED EXPRESSION AFTER ELSE")
                return False
            if next_tok[1] == "if" or next_tok[1] == "else":
                print_error_message("EXPECTED STATEMENT AFTER ELSE")
                return False
            if next_tok[1] in ops:
                print_error_message("EXPECTED STATEMENT AFTER ELSE, BUT GOT OPERATION")
                return False
            if prev_tok[1] == "if" or prev_tok[1] == "else":
                print_error_message("EXPECTED STATEMENT BEFORE ELSE")
                return False
            if prev_tok[1] in ops:
                print_error_message("EXPECTED STATEMENT BEFORE ELSE, BUT GOT OPERATION")
                return False
            else:
                return True
        
        elif curr_tok[1] in ops:
            if before_prev_token == None:
                print_error_message("CONDITION CAN ONLY BE FOLLOWED BY AN IF, BUT THERE IS NONE")
                return False
            if prev_tok == None or next_tok == None:
                print_error_message("EXPECTED EXPRESSION BEFORE AND AFTER OPERAND, GOT NONE")
                return False
            if prev_tok[1] == "if" or prev_tok[1] == "else":
                print_error_message("EXPECTED EXPRESSION BEFORE OPERAND, GOT IF/ELSE")
                return False
            if prev_tok[1] in ops:
                print_error_message("EXPECTED EXPRESSION BEFORE OPERAND, GOT OPERATION")
                return False
            if next_tok[1] == "if" or next_tok[1] == "else":
                print_error_message("EXPECTED EXPRESSION AFTER OPERAND, GOT IF/ELSE")
                return False
            if next_tok[1] in ops:
                print_error_message("EXPECTED EXPRESSION AFTER OPERAND, GOT OPERATION")
                return False
            if before_prev_token != "if":
                print_error_message("CONDITION CAN ONLY BE FOLLOWED BY AN IF")
                return False
            if after_next_token == None:
                print_error_message("CONDITION MUST BE FOLLOWED BY A STATEMENT, BUT THERE IS NONE")
                return False
            if after_next_token[1] != "if" or after_next_token[1] != "else" or after_next_token[1] not in ops:
                return True
            else:
                print_error_message("CONDITION MUST BE FOLLOWED BY A STATEMENT")
                return False

    def handleError(tokens, ops):
        # maintain count of if-elses
        i_e_count = 0
        if_encountered = False

        for i in range(len(tokens)):
            if tokens[i][1] == "if":
                i_e_count += 1
                if_encountered = True
                if(handle_section_error(tokens, i, ops, i_e_count) == False):
                    return False
            elif tokens[i][1] == "else":
                if if_encountered == False:
                    print("Syntax error: ELSE WITHOUT IF")
                    return False
                i_e_count -= 1
                if(handle_section_error(tokens, i, ops, i_e_count) == False):
                    return False
            elif tokens[i][1] in ops:
                if(handle_section_error(tokens, i, ops, i_e_count) == False):
                    return False
        return True


    # cross product
    def crossProd(a, b):
        return {i + j for i in a for j in b if a and b}

    # main function that implements CYK algorithm
    def cyk(tokens, ops, tr, vr):
        if len(tokens) == 0:
            print("Syntax error: EMPTY STATEMENT")
            return False
        
        # create a triangular dp matrix for CYK algo
        DP = [[set() for _ in range(len(tokens) - i)] for i in range(len(tokens))]
        # lhs and rhs of the variable rules
        lhs = [var[0] for var in vr]
        rhs = [var[1] for var in vr]

        for i in range(len(tokens)):
            for rule in tr:
                tl = rule[1]
                if tl == "y":
                    if tokens[i][1] == "if" or tokens[i][1] == "else":
                        flag = False
                    elif tokens[i][1] in ops:
                        flag = False
                    else:
                        flag = True
                elif tl == "r":
                    val = 0
                    if tokens[i][0] == "INTEGER":
                        val = int(tokens[i][1])
                    elif tokens[i][0] == "FLOAT":
                        val = float(tokens[i][1])
                    else:
                        flag = False
                    if val >= 0:
                        flag = True
                    else:
                        flag = False
                elif tl == "else" or tl == "if":
                    if tokens[i][1] == tl:
                        flag = True
                    else:
                        flag = False
                elif tl == "s":
                    if tokens[i][1] in ops:
                        flag = True
                    else:
                        flag = False
                else:
                    flag = False
                
                if flag:
                    DP[0][i].add(rule[0])
        
        for i in range(1, len(tokens)):
            for j in range(len(tokens) - i):
                for k in range(i):
                    cross = crossProd(DP[k][j], DP[i - k - 1][j + k + 1])
                    for com in cross:
                        if com in rhs:
                            matching_indices = []
                            for idx, ele in enumerate(rhs):
                                if ele == com:
                                    matching_indices.append(idx)
                            
                            for idx in matching_indices:
                                DP[i][j].add(lhs[idx])

        if "S" in DP[len(tokens) - 1][0]:
            return True
        else:
            return False


    # main implementation
    rules = {
        ("S", "y"),("G", "y"),("X", "y"),("I", "if"),("E", "else"),("O", "s"),("Z", "y"),
        ("S", "IA"),("S", "ZZ"),("Z", "IA"),("Z", "ZZ"),("A", "GZ"),("A", "GB"),("G", "XC"),("C", "OX"),("X", "XC"),("B", "ZF"),("F", "EZ"),
    }

    ops = ["+","-","*","/","<",">","=","^"]
    vr = []
    tr = []
    # put all the lower rhs values in tr and upper rhs values in vr
    for rule in rules:
        if rule[1].islower():
            tr.append(rule)
        else:
            vr.append(rule)

    if cyk(tokens, ops, tr, vr):
        return True
    else:
        handleError(tokens, ops)
    
    pass


# Test the tokenizer
if __name__ == "__main__":
    # source_code = "if 1+2 if 2+3 print ho else print hello"
    # source_code = "if 1-2 if 2-3 print ho else print hello else print wow"
    # source_code = "if 1-2 print hi else if 2-3 print hi else print hello"
    # source_code = "if 1-2 print ho else print hello if 2-3 print hi else print hello"
    # source_code = "if 1-2 print ho print hi"
    # source_code = "if 2+print print 5"
    # source_code = "if 1-2 if 2-3 print ho else print hello else print wow else print yay"

    tokens = tokenize(source_code)
    # You are tasked with implementing the function checkGrammar(tokens) that takes in a list of tokens and returns True if the grammar is correct, and False otherwise
    logs = checkGrammar(tokens)

    if logs:
        for token in tokens:
            print(f"Token Type: {token[0]}, Token Value: {token[1]}")