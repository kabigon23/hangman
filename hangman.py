import PySimpleGUI as sg
from string import ascii_uppercase

class Hangman:
    def __init__(self) -> None:
        layout = [
            [
                self._build_canvas_frame(),
                self._build_letters_frame(),
            ],
            [
                self._build_guessed_word_frame(),
            ],
            [
                self._build_action_buttons_frame(),
            ],
        ]
        self._window = sg.Window(
            title="Hangman",
            layout=layout,
            finalize=True,
            margins=(100, 100),
        )
        self._canvas = self._window["-CANVAS-"]
        self._draw_scaffold()

    def read_event(self):
        event = self._window.read()
        event_id = event[0] if event is not None else None
        return event_id
    
    def close(self):
        self._window.close()

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
    
    def _build_letters_frame(self):
        letter_groups = [
            ascii_uppercase[i : i + 4]
            for i in range(0, len(ascii_uppercase), 4)
        ]
        letter_buttons = [
            [
                sg.Button(
                    button_text=f" {letter} ",
                    font="Courier 20",
                    border_width=0,
                    button_color=(None, sg.theme_background_color()),
                    key=f"-letter-{letter}-",
                    enable_events=True,
                )
                for letter in letter_group
            ]
            for letter_group in letter_groups
        ]
        return sg.Column(
            [
                [
                    sg.Frame(
                        "Letters",
                        letter_buttons,
                        font="Any 20",
                    ),
                    sg.Sizer(),
                ]
            ]
        )
    
    def _build_guessed_word_frame(self):
        return sg.Frame(
            "",
            [
                [
                    sg.Text(
                        key="-DISPLAY-WORD-",
                        font="Courier 20",
                    )
                ]
            ],
            element_justification="center",
        )
    
    def _build_action_buttons_frame(self):
        return sg.Frame(
            "",
            [
                [
                    sg.Sizer(h_pixels=90),
                    sg.Button(
                        button_text="New",
                        key="-NEW-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Restart",
                        key="-RESTART-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Quit",
                        key="-QUIT-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=90),
                ]
            ],
            font="Any 20",
        )

    def _draw_scaffold(self):
        lines = [
            ((40, 55), (180, 55), 10),
            ((165, 60), (165, 365), 10),
            ((160, 360), (100, 360), 10),
            ((100, 365), (100, 330), 10),
            ((100, 330), (100, 310), 1),
        ]
        for *points, width in lines:
            self._canvas.DrawLine(*points, color="black", width=width)

if __name__ == "__main__":
    game = Hangman()
    while True:
        event_id = game.read_event()
        if event_id in {sg.WIN_CLOSED}:
            break
    game.close()
