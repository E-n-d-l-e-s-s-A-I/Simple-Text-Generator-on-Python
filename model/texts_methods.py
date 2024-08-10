from view.main_window import MainWindow


def add_line_feed(phrase: str) -> None:
    """Add line break characters to a phrase according to the size of the output window from Mainwindow."""
    phrase_with_line_feed = []
    rest_of_phrase = phrase
    while len(rest_of_phrase) > MainWindow.get_output_width():
        space_index = rest_of_phrase[MainWindow.get_output_width()-1::-1].find(" ")
        list_rest_of_phrase = list(rest_of_phrase)
        list_rest_of_phrase[MainWindow.get_output_width()-space_index-1] = "\n"

        phrase_with_line_feed.append("".join(list_rest_of_phrase[:MainWindow.get_output_width()-space_index]))
        rest_of_phrase = rest_of_phrase[MainWindow.get_output_width()-space_index:]
    phrase_with_line_feed.append(rest_of_phrase)
    return "".join(phrase_with_line_feed)
