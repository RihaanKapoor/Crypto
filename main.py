import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure Pillow is installed: pip install pillow

# Path to card images (Ensure you have "cards/card_1.png" to "cards/card_13.png" in this folder)
CARD_IMAGE_PATH = "cards/"

def play_card_game():
    def load_card_images():
        """Loads card images (1–13) into a dictionary."""
        images = {}
        for i in range(1, 14):
            try:
                img = Image.open(f"{CARD_IMAGE_PATH}card_{i}.png")
                img = img.resize((100, 150))  # Resize for consistency
                images[i] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading card_{i}.png: {e}")
        return images

    def generate_cards():
        """Generates random cards and updates the display, limited to 3 reshuffles."""
        if game_state["reshuffle_count"] >= 3:
            messagebox.showwarning("Reshuffle Limit Reached", "You have used all 3 reshuffles!")
            return

        game_state["reshuffle_count"] += 1  # Increase counter

        cards = [random.randint(1, 13) for _ in range(6)]
        game_state["answer_card"] = cards[-1]
        game_state["normal_cards"] = cards[:-1]

        for i, card in enumerate(game_state["normal_cards"]):
            normal_card_labels[i].config(image=card_images[card])

        answer_card_label.config(image=card_images[game_state["answer_card"]])
        equation_entry.delete(0, tk.END)

        # Update reshuffle count display
        reshuffle_label.config(text=f"Reshuffles Left: {3 - game_state['reshuffle_count']}")

        # Disable button after 3 uses
        if game_state["reshuffle_count"] >= 3:
            generate_button.config(state=tk.DISABLED)

    def check_equation():
        """Checks if the equation correctly forms the answer card."""
        equation = equation_entry.get()

        # Handle special cases
        if equation.lower() == "reshuffle":
            generate_cards()
            return
        elif equation.lower() == "exit":
            root.destroy()
            return

        # Ensure all normal cards are used
        if not all(str(card) in equation for card in game_state["normal_cards"]):
            messagebox.showerror("Incorrect Input", "You must use all the normal cards. Try again.")
            return

        try:
            result = eval(equation)  # Evaluate user input

            if result == game_state["answer_card"]:
                messagebox.showinfo("Congratulations!", "You made the answer card!")

                # Correct answer → Ask if the player wants to play again
                if messagebox.askyesno("Play Again?", "Would you like to play again?"):
                    reset_game()
                else:
                    root.destroy()
            else:
                messagebox.showerror("Incorrect", "The equation does not result in the answer card. Try again.")  
                # ❌ Prevents resetting the game on incorrect answers

        except (TypeError, SyntaxError, NameError, ZeroDivisionError) as e:
            messagebox.showerror("Invalid Input", f"Invalid input. Try again. Error: {e}")

    def reset_game():
        """Resets the game and allows reshuffling again."""
        game_state["reshuffle_count"] = 0
        generate_button.config(state=tk.NORMAL)  # Enable reshuffle button
        reshuffle_label.config(text="Reshuffles Left: 3")
        generate_cards()

    def open_game_window():
        """Opens the game window and closes the title screen."""
        title_page.destroy()

        global root
        root = tk.Toplevel()
        root.title("Crypto Card Game")

        instructions_label = tk.Label(
            root,
            text="""Rules:
- Use all the normal cards to create an equation.
- The equation must result in the Answer Card.
- You can use +, -, *, and /.
- You can reshuffle up to 3 times.
- Type 'reshuffle' to get new cards.
- Type 'exit' to quit the game.""",
            font=("Arial", 12)
        )
        instructions_label.pack()

        global normal_card_labels
        normal_card_labels = []
        normal_cards_frame = tk.Frame(root)
        normal_cards_frame.pack()

        for _ in range(5):
            lbl = tk.Label(normal_cards_frame, image=card_back)
            lbl.pack(side="left", padx=5)
            normal_card_labels.append(lbl)

        global answer_card_label
        answer_card_label = tk.Label(root, image=card_back)
        answer_card_label.pack(pady=10)

        global reshuffle_label
        reshuffle_label = tk.Label(root, text="Reshuffles Left: 3", font=("Arial", 12, "bold"))
        reshuffle_label.pack(pady=5)

        global equation_entry
        equation_entry = tk.Entry(root, width=50)
        equation_entry.pack()
        equation_entry.bind("<Return>", lambda event: check_equation())

        check_button = tk.Button(root, text="Check Equation", command=check_equation)
        check_button.pack()

        global generate_button
        generate_button = tk.Button(root, text="Generate New Cards", command=generate_cards)
        generate_button.pack()

        reset_game()

    global card_images
    card_images = load_card_images()

    try:
        card_back = Image.open(f"{CARD_IMAGE_PATH}card_back.png")
        card_back = card_back.resize((100, 150))
        card_back = ImageTk.PhotoImage(card_back)
    except Exception as e:
        print(f"Error loading card_back.png: {e}")
        card_back = None

    # ✅ FIX: Use a dictionary to store `reshuffle_count`
    global game_state
    game_state = {
        "reshuffle_count": 0,
        "normal_cards": [],
        "answer_card": 0
    }

    title_page = tk.Tk()
    title_page.title("Crypto Card Game")

    tk.Label(title_page, text="Welcome to Crypto Card Game", font=("Arial", 24, "bold")).pack(pady=50)
    tk.Button(title_page, text="Start Game", command=open_game_window, font=("Arial", 14)).pack(pady=20)

    title_page.mainloop()

# Start the game
play_card_game()
