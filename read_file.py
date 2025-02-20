#!/usr/bin/env python

def read_questions_file(questions_file):
    questions = [[{"title": "", "questions": [[{} for _ in range(3)] for _ in range(3)]} for _ in range(3)] for _ in range(3)]

    next_line = questions_file.readline()
    state = 0
    # 0 = just read empty line
    # 1 = now reading question lines
    # 2 = now reading response lines
    primary_row = 0
    secondary_row = 0
    primary_col = 0
    secondary_col = 0
    current_question = {"prompt": "", "answers": {"correct": "", "incorrect": []}}
    while next_line:
        next_line = next_line[:-1]
        if state == 0:
            if next_line == "":
                state = 0
                next_line = questions_file.readline()
                continue

            if next_line[0] == "#":
                next_line = questions_file.readline()
                continue

            if next_line[0] == "*":
                try:
                    remaining_line = ""
                    assert(next_line)
                    remaining_line = next_line[1:]
                    assert(remaining_line[:2] == " (")
                    remaining_line = remaining_line[2:]

                    primary_row_str = ""
                    while remaining_line[0].isdigit():
                        primary_row_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(primary_row_str)
                    primary_row = int(primary_row_str)

                    assert(remaining_line[:2] == ", ")
                    remaining_line = remaining_line[2:]
                    primary_col_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        primary_col_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(primary_col_str)
                    primary_col = int(primary_col_str)

                    assert(remaining_line[:2] == ") ")
                    remaining_line = remaining_line[2:]

                    assert(remaining_line)
                    questions[primary_row][primary_col]["title"] = remaining_line

                except AssertionError as e:
                    raise AssertionError(e.args[0] if e.args else "Invalid category coordinate in question list: `" + next_line[:-len(remaining_line) if remaining_line else len(next_line)] + "<HERE>" + remaining_line + "`")

                next_line = questions_file.readline()
                continue

            if next_line[0] == "(":
                try:
                    state = 1
                    current_question = {"prompt": "", "answers": {"correct": "", "incorrect": []}}
                    remaining_line = ""
                    assert(next_line)
                    remaining_line = next_line[1:]
                    assert(remaining_line)

                    primary_row_str = ""
                    while remaining_line[0].isdigit():
                        primary_row_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(primary_row_str)
                    primary_row = int(primary_row_str)

                    assert(remaining_line[:2] == ", ")
                    remaining_line = remaining_line[2:]
                    primary_col_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        primary_col_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(primary_col_str)
                    primary_col = int(primary_col_str)

                    assert(remaining_line[:2] == ")(")
                    remaining_line = remaining_line[2:]

                    secondary_row_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        secondary_row_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(secondary_row_str)
                    secondary_row = int(secondary_row_str)

                    assert(remaining_line[:2] == ", ")
                    remaining_line = remaining_line[2:]
                    secondary_col_str = ""
                    assert(remaining_line)
                    while remaining_line[0].isdigit():
                        secondary_col_str += remaining_line[0]
                        remaining_line = remaining_line[1:]
                        assert(remaining_line)
                    assert(secondary_col_str)
                    secondary_col = int(secondary_col_str)

                    assert(remaining_line == ")")
                except AssertionError as e:
                    raise AssertionError(e.args[0] if e.args else "Invalid subtile coordinate in question list: `" + next_line[:-len(remaining_line) if remaining_line else len(next_line)] + "<HERE>" + remaining_line + "`") from None

                next_line = questions_file.readline()
                continue

        if state == 1:
            assert next_line, "Expected question prompt after tile coordinate"
            state = 2

            current_question["prompt"] = next_line
            next_line = questions_file.readline()
            continue
        
        if state == 2:
            if next_line == "":
                state = 0
                questions[primary_row][primary_col]["questions"][secondary_row][secondary_col] = current_question
                next_line = questions_file.readline()
                continue

            try:
                remaining_line = ""
                assert(next_line[0] == " ")
                remaining_line = next_line[1:]
                assert(remaining_line[0] == "+" or remaining_line[0] == "-")
                correct = (remaining_line[0] == "+")
                remaining_line = remaining_line[1:]
                assert(remaining_line)
                while remaining_line[0] == " ":
                    remaining_line = remaining_line[1:]
                    assert(remaining_line)

                if correct:
                    if current_question["answers"]["correct"]:
                        raise AssertionError("Question list contains multiple correct responses for a single prompt (the maximum is one)")
                    current_question["answers"]["correct"] = remaining_line
                else:
                    current_question["answers"]["incorrect"].append(remaining_line)
            except AssertionError as e:
                raise AssertionError(e.args[0] if e.args else "Invalid response in question list: `" + next_line[:-len(remaining_line) if remaining_line else len(next_line)] + "<HERE>" + remaining_line + "`") from None

            next_line = questions_file.readline()
            continue

    try:
        assert(state == 0 or state == 2)
        if state == 2:
            assert(current_question["answers"]["correct"])
            questions[primary_row][primary_col]["questions"][secondary_row][secondary_col] = current_question
    except AssertionError as e:
        raise AssertionError("Unexpectedly reached end of questions file")
    return questions
