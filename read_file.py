#!/usr/bin/env python

with open("questions.txt", "r") as questions_file:
    questions = [[{} for _ in range(3)] for _ in range(3)]

    next_line = questions_file.readline()
    state = 0
    # 0 = just read empty line
    # 1 = now reading question lines
    # 2 = now reading response lines
    row = 0
    col = 0
    while next_line:
        next_line = next_line[:-1]
        if state == 0:
            if next_line == "":
                state = 0
                print("Empty line")
                next_line = questions_file.readline()
                continue

            if next_line[0] == "(":
                try:
                    print("Coordinate line")
                    state = 1
                    remaining_line = ""
                    assert(next_line)
                    remaining_line = next_line[1:]
                    row_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        row_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(row_str)
                    row = int(row_str)
                    print("Row: " + str(row))

                    assert(remaining_line[:2] == ", ")
                    remaining_line = remaining_line[2:]
                    col_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        col_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(col_str)
                    col = int(col_str)
                    print("Col: " + str(col))
                    
                    assert(remaining_line == ")")
                except AssertionError as e:
                    raise AssertionError("Invalid tile coordinate in question list: `" + next_line[:-len(remaining_line) if remaining_line else len(next_line)] + "<HERE>" + remaining_line + "`")

                next_line = questions_file.readline()
                continue

        if state == 1:
            assert next_line, "Expected question prompt after tile coordinate"
            state = 2
            print("Question line")

            questions[row][col]["prompt"] = next_line
            next_line = questions_file.readline()
            continue
        
        if state == 2:
            if next_line == "":
                state = 0
                print("Empty line")
                next_line = questions_file.readline()
                continue
            
            try:
                print("Response line")
                remaining_line = ""
                assert(next_line[0] == " ")
                remaining_line = next_line[1:]
                assert(remaining_line[0] == "+" or remaining_line[0] == "-")
            except AssertionError as e:
                raise AssertionError("Invalid response in question list: `" + next_line[:-len(remaining_line) if remaining_line else len(next_line)] + "<HERE>" + remaining_line + "`")

            next_line = questions_file.readline()
            continue

    print(questions)
