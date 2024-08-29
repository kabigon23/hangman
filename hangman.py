import PySimpleGUI as sg

class Hangman:
    def __init__(self) -> None:
        layout = [
            [
                self._build_canvas_frame(),
                # self._build_letters_frame(),
            ],
            [
                # self._build_guessed_word_frame(),
            ],
            [
                # self._build_action_buttions_frame(),
            ],
        ]
        self.window = sg.Window(
            title="Hangman",
            layout=layout,
            finalize=True,
            margins=(100, 100),
        )

    def read_event(self):
        event = self.window.read()
        event_id = event[0] if event is not None else None
        return event_id
    
    def close(self):
        self.window.close()

    def _build_canvas_frame(self):
        return sg.Frame(
            "Hangman",
            [
                [
                    sg.Graph(
                        key="-CANVAS-",
                        canvas_size=(200, 400),
                        graph_bottom_left=(0, 0),
                        graph_top_right=(200, 400),
                    )
                ]
            ],
            font="Any 20",
        )

if __name__ == "__main__":
    game = Hangman()
    while True:
        event_id = game.read_event()
        if event_id in {sg.WIN_CLOSED}:
            break
    game.close()
