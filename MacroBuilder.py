from tkinter import Tk, Button, Label, Frame, PhotoImage
import webbrowser
import os
from collections import deque


class MacroBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("TFC Anvil Macro Builder")

        self.sequence = deque()  # Stores the button presses
        self.button_labels = ["-3", "-6", "+2", "+7", "-9", "-15", "+13", "+16"]
        self.image_files = ["icons/-3.png", "icons/-6.png", "icons/+2.png", "icons/+7.png", "icons/-9.png",
                            "icons/-15.png", "icons/+13.png", "icons/+16.png"]
        self.images = [PhotoImage(file=img) for img in self.image_files]  # Load images

        self.create_ui()

    def create_ui(self):
        self.link_label = Label(self.root, text="TFC Anvil Helper", fg="blue", cursor="hand2",
                                font=("Arial", 12, "underline"))
        self.link_label.pack(pady=5)
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open_new(
            "https://www.curseforge.com/minecraft/texture-packs/tfc-anvil-helper"))

        self.credit_label = Label(self.root,
                                  text="Icons attributed to TFC Anvil Helper, designed for use in conjunction with it.",
                                  font=("Arial", 10))
        self.credit_label.pack(pady=2)

        self.frame = Frame(self.root)
        self.frame.pack(pady=10)

        # 2x4 Grid of image buttons
        self.buttons = []
        for i in range(2):
            for j in range(4):
                index = i * 4 + j
                btn = Button(self.frame, image=self.images[index], bg="gray", activebackground="darkgray",
                             command=lambda i=index: self.add_to_sequence(i))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        # Display sequence preview
        self.sequence_label = Label(self.root, text="Sequence: ", font=("Arial", 12))
        self.sequence_label.pack(pady=5)

        # Controls
        self.undo_button = Button(self.root, text="Undo", bg="lightblue", activebackground="blue", command=self.undo)
        self.undo_button.pack(side="left", padx=10)

        self.reset_button = Button(self.root, text="Reset", bg="lightcoral", activebackground="red",
                                   command=self.reset_sequence)
        self.reset_button.pack(side="right", padx=10)

        self.export_button = Button(self.root, text="Export Macro", bg="lightgreen", activebackground="green",
                                    command=self.export_macro)
        self.export_button.pack(pady=10)

    def add_to_sequence(self, index):
        if self.sequence and self.sequence[-1][0] == self.button_labels[index]:
            self.sequence[-1][1] += 1  # Increase count if the last action is the same
        else:
            self.sequence.append([self.button_labels[index], 1])  # Add new action
        self.update_sequence_display()

    def update_sequence_display(self):
        sequence_str = ",".join(f"{i[0]}x{i[1]}" for i in self.sequence)
        self.sequence_label.config(text=f"Sequence: {sequence_str}")

    def undo(self):
        if self.sequence:
            if self.sequence[-1][1] > 1:
                self.sequence[-1][1] -= 1
            else:
                self.sequence.pop()
            self.update_sequence_display()

    def reset_sequence(self):
        self.sequence.clear()
        self.update_sequence_display()

    def export_macro(self):
        folder = "macro_parts"
        header = self.read_file(os.path.join(folder, "header.txt"))
        footer = self.read_file(os.path.join(folder, "footer.txt"))
        loop_header_1 = self.read_file(os.path.join(folder, "loop_header_1.txt"))
        loop_header_2 = self.read_file(os.path.join(folder, "loop_header_2.txt"))
        loop_footer_1 = self.read_file(os.path.join(folder, "loop_footer_1.txt"))
        loop_footer_2 = self.read_file(os.path.join(folder, "loop_footer_2.txt"))
        click = self.read_file(os.path.join(folder, "click.txt"))

        macro_content = [header]

        for action, count in self.sequence:
            move_content = self.read_file(os.path.join(folder, f"{action}.txt"))
            macro_content.append(move_content)
            macro_content.append(loop_header_1)
            macro_content.append(str(count))
            macro_content.append(loop_header_2)
            macro_content.append(click)
            macro_content.append(loop_footer_1)
            macro_content.append(str(count))
            macro_content.append(loop_footer_2)

        macro_content.append(footer)

        with open("exported_macro.xml", "w") as f:
            f.write("\n".join(macro_content))

    def read_file(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read().strip()
        return ""


if __name__ == "__main__":
    root = Tk()
    app = MacroBuilder(root)
    root.mainloop()
