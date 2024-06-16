import customtkinter as ctk
import tkinter as tk
from CTkMenuBar import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import subprocess
import tkinter.messagebox as messagebox
import datetime
from tkinter import filedialog
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from customtkinter import CTkInputDialog
import math
import CTkListbox as ctkl

def quiz_main():
    def start_quiz():
        try:
            selected_quiz = quiz_listbox.get(quiz_listbox.curselection())
            quiz_page(selected_quiz)
        except tk.TclError:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Quiz aus der Liste.")

    # Create the main quiz window
    quiz_main_window = ctk.CTkToplevel(root)
    quiz_main_window.title("Quiz")
    quiz_main_window.geometry("700x400")

    # Frame for the quiz list
    list_frame = ctk.CTkFrame(quiz_main_window)
    list_frame.pack(padx=10, pady=10)

    # Label for the quiz list title
    list_label = ctk.CTkLabel(list_frame, text="Quizliste", font=("Arial", 14))
    list_label.pack(pady=5)

    # Listbox to display quiz names
    quiz_listbox = ctkl.CTkListbox(list_frame)
    quiz_listbox.pack(pady=5)

    # Read quiz filenames from the 'Quiz' directory and add to the listbox
    quiz_directory = 'Quiz'
    if not os.path.exists(quiz_directory):
        os.makedirs(quiz_directory)

    for filename in os.listdir(quiz_directory):
        if filename.endswith(".json"):
            quiz_name = os.path.splitext(filename)[0]  # Remove the .json extension
            quiz_listbox.insert(tk.END, quiz_name)

    try:
        quiz_listbox.select(0)
    except:
        pass

    # Frame for the instructions
    instruction_frame = ctk.CTkFrame(quiz_main_window)
    instruction_frame.pack(padx=10, pady=10)

    # Label for instructions
    instructions = """
    Anleitung:
    Wählen Sie die richtige Antwort aus und verbessern Sie so ihre Kenntnisse über Raketen und Mondlandungen.
    """
    instruction_label = ctk.CTkLabel(instruction_frame, text=instructions, font=("Arial", 12))
    instruction_label.pack(pady=5, padx=5)

    # Start Quiz button
    start_button = ctk.CTkButton(quiz_main_window, text="Start Quiz", command=start_quiz)
    start_button.pack(pady=10)

def quiz_page(quiz_name):
    # Load quiz data from the selected file
    quiz_file = os.path.join('Quiz', f'{quiz_name}.json')
    if not os.path.exists(quiz_file):
        messagebox.showerror("Fehler", "Die ausgewählte Quiz-Datei existiert nicht.")
        return

    with open(quiz_file, 'r') as file:
        quiz_data = json.load(file)

    # Create the quiz window
    quiz_window = ctk.CTkToplevel(root)
    quiz_window.title(f"Quiz: {quiz_name}")
    quiz_window.geometry("600x400")
    quiz_window.attributes('-topmost', True)

    # Initialize question index and score
    question_index = 0
    score = 0

    # Function to display the current question
    def display_question():
        nonlocal question_index
        if question_index < len(quiz_data["questions"]):
            question = quiz_data["questions"][question_index]

            question_label.configure(text=question["question"])

            for i, answer_button in enumerate(answer_buttons):
                answer_button.configure(text=question["answers"][i], state=tk.NORMAL)

            feedback_label.configure(text="")  # Clear previous feedback
            next_button.configure(state=tk.DISABLED)
        else:
            show_final_score()

    # Function to handle answer selection
    def select_answer(selected_answer):
        nonlocal question_index, score
        question = quiz_data["questions"][question_index]
        correct_answer = question["correct"]

        for answer_button in answer_buttons:
            answer_button.configure(state=tk.DISABLED)

        if selected_answer == correct_answer:
            feedback_label.configure(text="Richtig!", fg_color="green")
            score += 1
        else:
            feedback_label.configure(text=f"Falsch! Die richtige Antwort war: {question['answers'][correct_answer]}",
                                     fg_color="red")

        question_index += 1
        next_button.configure(state=tk.NORMAL)

    # Function to show the final score
    def show_final_score():
        question_label.configure(text=f"Quiz beendet! Dein Punktestand: {score}/{len(quiz_data['questions'])}")
        for answer_button in answer_buttons:
            answer_button.pack_forget()
        feedback_label.pack_forget()
        next_button.pack_forget()

    # Create UI elements
    question_label = ctk.CTkLabel(quiz_window, text="", font=("Arial", 14))
    question_label.pack(pady=20)

    answer_buttons = []
    for i in range(4):  # Assuming each question has 4 possible answers
        button = ctk.CTkButton(quiz_window, text="", width=400, command=lambda i=i: select_answer(i))
        button.pack(pady=5)
        answer_buttons.append(button)

    feedback_label = ctk.CTkLabel(quiz_window, text="", font=("Arial", 12))
    feedback_label.pack(pady=10)

    next_button = ctk.CTkButton(quiz_window, text="Nächste Frage", command=display_question, state=tk.DISABLED)
    next_button.pack(pady=20)

    # Display the first question
    display_question()

def load_constants(file_path):
    with open(file_path, 'r') as file:
        constants = json.load(file)
    return constants

def save_constants(file_path, constants):
    with open(file_path, 'w') as file:
        json.dump(constants, file, indent=4)

def load_settings(file_path):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {"dark_mode": False}
    return settings

def save_settings(file_path, settings):
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

def reset_constants():
    default_values = load_constants('Json_settings/default_values.json')
    save_constants('Json_settings/current_values.json', default_values)
    update_entries()

def update_entries():
    if 'entries' in globals():
        constants = load_constants('Json_settings/current_values.json')
        for key, value in constants.items():
            entry = entries.get(key)
            if entry:
                entry.delete(0, ctk.END)
                entry.insert(0, str(value))

def save_update_parameters_settings(entry_value):
    settings = load_settings("Json_settings/settings.json")
    settings["update_parameters_settings"] = entry_value
    with open("Json_settings/settings.json", 'w') as file:
        json.dump(settings, file, indent=4)

def set_dark_mode(value):
    settings = load_settings('Json_settings/settings.json')
    if value:
        ctk.set_appearance_mode("dark")
        settings["dark_mode"] = True
        color = 'black'
    else:
        ctk.set_appearance_mode("light")
        settings["dark_mode"] = False
        color="#f2fafc"
    save_settings('Json_settings/settings.json', settings)

def open_advanced_settings():
    advanced_window = ctk.CTkToplevel(root)
    advanced_window.title("Erweiterte Einstellungen")
    advanced_window.attributes('-topmost', 'true')
    advanced_window.resizable(False, False)  # Width, Height

    constants = load_constants('Json_settings/current_values.json')

    global entries
    entries = {}

    for key, value in constants.items():
        frame = ctk.CTkFrame(advanced_window)
        frame.pack(pady=5)
        label = ctk.CTkLabel(frame, text=key)
        label.pack(side="left", padx=5)
        entry = ctk.CTkEntry(frame)
        entry.insert(0, str(value))
        entry.pack(side="right", padx=5)
        entries[key] = entry

    def apply_changes():
        for key, entry in entries.items():
            try:
                constants[key] = float(entry.get())
            except ValueError:
                messagebox.showerror("Fehler", f"Ungültiger Wert für {key}")
                return
        save_constants('Json_settings/current_values.json', constants)

    def reset_to_defaults():
        reset_constants()
        update_entries()

    apply_button = ctk.CTkButton(advanced_window, text="Übernehmen", command=apply_changes)
    apply_button.pack(pady=10)

    reset_button = ctk.CTkButton(advanced_window, text="Zurücksetzen", command=reset_to_defaults)
    reset_button.pack(pady=10)

    dark_mode_var = ctk.StringVar(value="off")



    def toggle_dark_mode():
        set_dark_mode(dark_mode_var.get() == "on")

    settings = load_settings('Json_settings/settings.json')
    dark_mode_var.set("on" if settings["dark_mode"] else "off")

    dark_mode_check = ctk.CTkCheckBox(advanced_window, text="Dark Mode", variable=dark_mode_var, onvalue="on", offvalue="off", command=toggle_dark_mode)
    dark_mode_check.pack(pady=10)

    dark_label = ctk.CTkLabel(advanced_window,
                              text="Nach dem Wechsel zu dark oder light mode \n das Programm neu starten\nHinweis: Der Export ist ebenfalls betroffen von dieser Einstellung")
    dark_label.pack(pady=10, padx=10)

    value = load_settings("Json_settings/settings.json").get("update_parameters_settings")
    frame_para = ctk.CTkFrame(advanced_window)
    frame_para.pack(pady=5, padx=5)
    label = ctk.CTkLabel(frame_para, text="In einer Sekunde sollen")
    label.pack(side="left", padx=5)
    entry = ctk.CTkEntry(frame_para)
    entry.insert(0, str(value))
    entry.pack(side="left", padx=5)
    label = ctk.CTkLabel(frame_para, text="Sekunden angezeigt werden")
    label.pack(side="right", padx=5)
    button = ctk.CTkButton(frame_para, text="Speichern", command=lambda: save_update_parameters_settings(entry.get()))
    button.pack(pady=5)

    label = ctk.CTkLabel(advanced_window,
                         text="Eine höhere Zahl bedeutet mehr Leistung. Bei Problemen bitte die Zahl verringern.\nEmpfohlen sind Werte zwischen 1 und 10. Standard: 1")
    label.pack(padx=5, pady=5)

def export_project():
    if hasattr(show_graphs, 'fig'):
        fig = show_graphs.fig
        # Step 1: Prompt user for the project name using CustomTkinter input dialog
        dialog = CTkInputDialog(text="Name des Projektes eingeben:", title="Projekt Name")
        project_name = dialog.get_input()
        if not project_name:
            messagebox.showerror("Fehler", "Kein Projektname vorhanden")
            return

        # Step 2: Create a directory for the project if it doesn't exist
        project_directory = os.path.join("Full Projects", project_name)
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        # Step 3: Save input values as JSON
        input_values = {
            "Fläche": input_A.get(),
            "Strömungswiderstand": input_Cw.get(),
            "Geschwindigkeit": input_v.get(),
            "Dauer": input_duration.get(),
            "Schrittweite": input_steps.get(),
            "Initial Mass": input_initial_mass.get(),
            "Ausstoßgeschwindigkeit": input_v_e.get(),
            "Fuel Mass": input_fuel_mass.get(),
            "Burn Rate": input_burn_rate.get(),
            "Fläche 2": "",
            "Ausstoßgeschwindigkeit 2": "",
            "Fuel Mass 2": "",
            "Burn Rate 2": ""
        }

        with open(os.path.join(project_directory, f"{project_name}.json"), "w") as json_file:
            json.dump(input_values, json_file, indent=4)

        save_folder = "Saves"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Save input values to a JSON file
        file_path = os.path.join(save_folder, f"{project_name}.json")
        with open(file_path, 'w') as json_file:
            json.dump(input_values, json_file, indent=4)

        # Step 4: Create a PDF with diagrams and input values
        pdf_path = os.path.join(project_directory, f"{project_name}.pdf")
        with PdfPages(pdf_path) as pdf:
            # Add the figure to the PDF
            pdf.savefig(fig)

        #Images
        project_folder = os.path.join("Full Projects", project_name)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
        for i, ax in enumerate(fig.get_axes()):
            # Create a new figure containing only the current subplot
            new_fig = plt.figure(figsize=(5, 5))  # Adjust figure size as needed
            new_ax = new_fig.add_subplot(111)
            new_ax.plot(ax.get_lines()[0].get_xdata(), ax.get_lines()[0].get_ydata())  # Copy data from original subplot
            new_ax.set_title(ax.get_title())
            new_ax.set_xlabel(ax.get_xlabel())
            new_ax.set_ylabel(ax.get_ylabel())
            new_fig.tight_layout()

            # Save the new figure as an image
            new_fig.savefig(os.path.join(project_folder, f"subplot_{i + 1}.png"), bbox_inches='tight')
            plt.close(new_fig)  # Close the figure to release memory

        subprocess.Popen(["explorer", project_folder])
    elif hasattr(show_graphs_two_stage, 'fig'):
        fig = show_graphs_two_stage.fig
        # Step 1: Prompt user for the project name using CustomTkinter input dialog
        dialog = CTkInputDialog(text="Name des Projektes eingeben:", title="Projekt Name")
        project_name = dialog.get_input()
        if not project_name:
            messagebox.showerror("Fehler", "Kein Projektname vorhanden")
            return

        # Step 2: Create a directory for the project if it doesn't exist
        project_directory = os.path.join("Full Projects", project_name)
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        # Step 3: Save input values as JSON
        input_values = {
            "Fläche": input_A.get(),
            "Strömungswiderstand": input_Cw.get(),
            "Geschwindigkeit": input_v.get(),
            "Dauer": input_duration.get(),
            "Schrittweite": input_steps.get(),
            "Initial Mass": input_initial_mass.get(),
            "Ausstoßgeschwindigkeit": input_v_e.get(),
            "Fuel Mass": input_fuel_mass.get(),
            "Burn Rate": input_burn_rate.get(),
            "Fläche 2": input_A_stage2.get(),
            "Ausstoßgeschwindigkeit 2": input_v_e_stage2.get(),
            "Fuel Mass 2": input_fuel_mass_stage2.get(),
            "Burn Rate 2": input_burn_rate_stage2.get()
        }

        with open(os.path.join(project_directory, f"{project_name}.json"), "w") as json_file:
            json.dump(input_values, json_file, indent=4)

        save_folder = "Saves"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Save input values to a JSON file
        file_path = os.path.join(save_folder, f"{project_name}.json")
        with open(file_path, 'w') as json_file:
            json.dump(input_values, json_file, indent=4)

        # Step 4: Create a PDF with diagrams and input values
        pdf_path = os.path.join(project_directory, f"{project_name}.pdf")
        with PdfPages(pdf_path) as pdf:
            # Add the figure to the PDF
            pdf.savefig(fig)

        #Images
        project_folder = os.path.join("Full Projects", project_name)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
        for i, ax in enumerate(fig.get_axes()):
            # Create a new figure containing only the current subplot
            new_fig = plt.figure(figsize=(5, 5))  # Adjust figure size as needed
            new_ax = new_fig.add_subplot(111)
            new_ax.plot(ax.get_lines()[0].get_xdata(), ax.get_lines()[0].get_ydata())  # Copy data from original subplot
            new_ax.set_title(ax.get_title())
            new_ax.set_xlabel(ax.get_xlabel())
            new_ax.set_ylabel(ax.get_ylabel())
            new_fig.tight_layout()

            # Save the new figure as an image
            new_fig.savefig(os.path.join(project_folder, f"subplot_{i + 1}.png"), bbox_inches='tight')
            plt.close(new_fig)  # Close the figure to release memory

        subprocess.Popen(["explorer", project_folder])
    else:
        messagebox.showerror("Fehler", "Keine Graphen zum Exportieren")

def import_json():
    # Open a file dialog to select the JSON file
    file_path = filedialog.askopenfilename(initialdir="Saves", title="Datei auswählen",
                                           filetypes=[("JSON files", "*.json")])

    if not file_path:
        # No file selected
        return

    try:
        # Load data from the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Clear existing input field values
        input_A.delete(0, tk.END)
        input_Cw.delete(0, tk.END)
        input_v.delete(0, tk.END)
        input_duration.delete(0, tk.END)
        input_steps.delete(0, tk.END)
        input_initial_mass.delete(0, tk.END)
        input_v_e.delete(0, tk.END)
        input_fuel_mass.delete(0, tk.END)
        input_burn_rate.delete(0, tk.END)
        input_A_stage2.delete(0, tk.END)
        input_v_e.delete(0, tk.END)
        input_fuel_mass_stage2.delete(0, tk.END)
        input_burn_rate_stage2.delete(0, tk.END)

        # Fill input fields with loaded data
        input_A.insert(tk.END, data.get("Fläche", ""))
        input_Cw.insert(tk.END, data.get("Strömungswiderstand", ""))
        input_v.insert(tk.END, data.get("Geschwindigkeit", ""))
        input_duration.insert(tk.END, data.get("Dauer", ""))
        input_steps.insert(tk.END, data.get("Schrittweite", ""))
        input_initial_mass.insert(tk.END, data.get("Initial Mass", ""))
        input_v_e.insert(tk.END, data.get("Ausstoßgeschwindigkeit", ""))
        input_fuel_mass.insert(tk.END, data.get("Fuel Mass", ""))
        input_burn_rate.insert(tk.END, data.get("Burn Rate", ""))
        input_A_stage2.insert(tk.END, data.get("Fläche 2", ""))
        input_v_e_stage2.insert(tk.END, data.get("Ausstoßgeschwindigkeit 2", ""))
        input_fuel_mass_stage2.insert(tk.END, data.get("Fuel Mass 2", ""))
        input_burn_rate_stage2.insert(tk.END, data.get("Burn Rate 2", ""))

        show_select()

    except Exception as e:
        # Error while loading or processing JSON file
        messagebox.showerror("Fehler", f"Fehler beim Importieren der Daten: {str(e)}")

def save():
    # Get input values
    input_values = {
        "Fläche": input_A.get(),
        "Strömungswiderstand": input_Cw.get(),
        "Geschwindigkeit": input_v.get(),
        "Dauer": input_duration.get(),
        "Schrittweite": input_steps.get(),
        "Initial Mass": input_initial_mass.get(),
        "Ausstoßgeschwindigkeit": input_v_e.get(),
        "Fuel Mass": input_fuel_mass.get(),
        "Burn Rate": input_burn_rate.get(),
        "Fläche 2": input_A_stage2.get(),
        "Ausstoßgeschwindigkeit 2": input_v_e_stage2.get(),
        "Fuel Mass 2": input_fuel_mass_stage2.get(),
        "Burn Rate 2": input_burn_rate_stage2.get()
    }

    # Create an input dialog to name the JSON file
    dialog = ctk.CTkInputDialog(text="Geben Sie den Dateinamen ein (ohne Erweiterung):", title="Dateiname")
    filename = dialog.get_input()

    if not filename:
        messagebox.showerror("Fehler", "Dateiname nicht angegeben.")
        return

    # Create "Saves" folder if it doesn't exist
    save_folder = "Saves"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save input values to a JSON file
    file_path = os.path.join(save_folder, f"{filename}.json")
    with open(file_path, 'w') as json_file:
        json.dump(input_values, json_file, indent=4)

    messagebox.showinfo("Erfolg", "Die Eingaben wurden erfolgreich gespeichert.")

def show_log():
    log_window = ctk.CTkToplevel(root, fg_color="white")
    log_window.title("Log-Datei")
    log_window.attributes("-topmost", True)  # Set log window to always stay on top

    log_text = ctk.CTkTextbox(log_window, wrap=tk.WORD)
    log_text.pack(fill=tk.BOTH, expand=True)
    log_text.configure(state="disabled")  # Disable editing again

    def update_log():
        # Save the current scroll position
        current_scroll_position = log_text.yview()

        # Read contents of log file and display in text widget
        with open("txt Files/graph_log.txt", "r") as log_file:
            log_entries = log_file.readlines()
            log_text.configure(state="normal")  # Enable editing temporarily
            log_text.delete("1.0", tk.END)  # Clear existing content
            log_text.insert(tk.END, "".join(log_entries))
            log_text.configure(state="disabled")  # Disable editing again

        # Restore the previous scroll position
        log_text.yview_moveto(current_scroll_position[0])

        # Schedule the next update
        log_window.after(500, update_log)

    # Call update_log function to start updating the log
    update_log()

def log_graphs(steps, duration):
    log_entry = f"Graphen gezeigt um {datetime.datetime.now()}\n"
    log_entry += f"Interval: {steps}, Länge: {duration}\n\n"

    # Read existing contents of log file
    with open("txt Files/graph_log.txt", "r") as log_file:
        existing_logs = log_file.read()

    # Prepend new log entry to existing logs
    updated_logs = log_entry + existing_logs

    # Write updated logs back to file
    with open("txt Files/graph_log.txt", "w") as log_file:
        log_file.write(updated_logs)

def log_error(message):
    log_entry = f"ERROR: Versuch um {datetime.datetime.now()} mit dem Fehler: {message}\n\n"

    # Read existing contents of log file
    with open("txt Files/graph_log.txt", "r") as log_file:
        existing_logs = log_file.read()

    # Prepend new log entry to existing logs
    updated_logs = log_entry + existing_logs

    # Write updated logs back to file
    with open("txt Files/graph_log.txt", "w") as log_file:
        log_file.write(updated_logs)

def impressum():
    impressum_window = ctk.CTkToplevel(root)
    impressum_window.title("Impressum")
    impressum_window.geometry("400x445")
    impressum_window.resizable(False, False)  # Width, Height

    impressum_text = ctk.CTkTextbox(impressum_window, wrap=tk.WORD)
    impressum_text.pack(fill=tk.BOTH, expand=True)

    # Insert impressum text
    impressum_text.insert(tk.END, "\nWas ist AstralSim?\n")
    impressum_text.insert(tk.END, "Erlebe die Faszination des Raumflugs mit AstralSim! Unsere App ermöglicht dir, Raketenstarts in Echtzeit zu simulieren und dabei interaktiv die Kontrolle zu übernehmen. Lerne mehr über Raketenwissenschaft, steuere verschiedene Parameter und gestalte deine eigenen Raketenstarts. Egal ob du ein Enthusiast oder ein Lernender bist, AstralSim bietet dir eine spannende und lehrreiche Erfahrung. Starte jetzt und hebe ab in die unendlichen Weiten des Weltraums!\n\n")

    impressum_text.insert(tk.END, "CEO:\n")
    impressum_text.insert(tk.END, "Maximilian Schmidt\n\n")

    impressum_text.insert(tk.END, "Backend Developer:\n")
    impressum_text.insert(tk.END, "Sara Wagner Villadangos\n\n")

    impressum_text.insert(tk.END, "Frontend Developer:\n")
    impressum_text.insert(tk.END, "Sebastian Leo Morawietz\n\n")

    impressum_text.insert(tk.END, "UI:\n")
    impressum_text.insert(tk.END, "Nishant Rostewitz\n\n")

    impressum_text.insert(tk.END, "Tastenkombination:\n")
    impressum_text.insert(tk.END, "Strg+S - Speichern\n")
    impressum_text.insert(tk.END, "Strg+L - Datei Importieren\n")
    impressum_text.insert(tk.END, "F5     - Ausführen\n")

    # Disable editing
    impressum_text.configure(state="disabled")

def leika():
    # Create a new top-level window
    leika_window = ctk.CTkToplevel(root)
    leika_window.title("Leika's Information")
    leika_window.geometry("600x325")
    leika_window.resizable(False, False)  # Width, Height

    # Information about Leika
    leika_info = """
Name: Leika
Rasse: Mischling (Husky, Terrier, möglicherweise weitere Rassen)
Alter: ungefähr 3,5 Jahre
Herkunft: Sowjetunion
Besondere Merkmale: 
• Leika war die erste Hündin im Weltraum und damit eine Pionierin der Raumfahrt. Sie war Teil des sowjetischen Weltraumprogramms und wurde speziell für die Mission ins All ausgewählt.
• Aufgabe: Leika wurde in den Weltraum geschickt, um die Auswirkungen von Weltraumbedingungen auf lebende Organismen zu erforschen. Während ihres Fluges trug sie einen Sensoranzug, der ihre Vitalparameter überwachte, und war an Bord der sowjetischen Raumsonde Sputnik 2.
• Besonderheiten: Leika war ein Symbol für den Fortschritt der Raumfahrt und wurde weltweit bekannt. Ihr Flug in den Weltraum war jedoch tragisch, da sie die Mission nicht überlebte. Aufgrund des Mangels an Wiedereintrittsfähigkeit wurde sie nicht zurück zur Erde gebracht.
• Nachwirkung: Leika's Beitrag zur Raumfahrtgeschichte wird bis heute gewürdigt. Ihr mutiger Flug trug dazu bei, wichtige Erkenntnisse über die Auswirkungen von Raumfahrtbedingungen auf Lebewesen zu gewinnen und den Weg für weitere bemannte Weltraummissionen zu ebnen.
    """

    # Create a text box to display Leika's information with bullet points
    leika_textbox = ctk.CTkTextbox(leika_window, width=600, height=325, wrap="word")
    leika_textbox.pack(pady=10)
    leika_textbox.insert(ctk.END, leika_info)
    leika_textbox.configure(state="disabled")  # Disable editing

def open_path():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(["explorer", script_folder])

def save_subplots_as_images(fig, folder_name):
    project_folder = os.path.join("Project", folder_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    for i, ax in enumerate(fig.get_axes()):
        # Create a new figure containing only the current subplot
        new_fig = plt.figure(figsize=(5, 5))  # Adjust figure size as needed
        new_ax = new_fig.add_subplot(111)
        new_ax.plot(ax.get_lines()[0].get_xdata(), ax.get_lines()[0].get_ydata())  # Copy data from original subplot
        new_ax.set_title(ax.get_title())
        new_ax.set_xlabel(ax.get_xlabel())
        new_ax.set_ylabel(ax.get_ylabel())
        new_fig.tight_layout()

        # Save the new figure as an image
        new_fig.savefig(os.path.join(project_folder, f"subplot_{i+1}.png"), bbox_inches='tight')
        plt.close(new_fig)  # Close the figure to release memory
    subprocess.Popen(["explorer", project_folder])

def burn_fuel(current_mass, fuel_mass, burn_rate, exhaust_velocity, time_step):
    if fuel_mass <= 0:
        return current_mass, fuel_mass, 0

    fuel_burned = min(burn_rate * time_step, fuel_mass)
    fuel_mass -= fuel_burned
    new_mass = current_mass - fuel_burned

    if new_mass > 0:
        delta_v = exhaust_velocity * np.log(current_mass / new_mass)
    else:
        delta_v = 0
    return new_mass, fuel_mass, delta_v

def simulate_rocket(initial_mass, fuel_mass, exhaust_velocity, burn_rate, total_time, time_step, g, T0, rho0, M, R, cw, A, v):
    current_mass = initial_mass
    velocity = 0
    acceleration_values = g
    distance = 0
    luftwiderstand_werte=[]

    times = np.arange(0, total_time, time_step)
    masses = []
    velocities = [0]
    accelerations=[]
    distances=[0]

    for t in times:
        current_mass, fuel_mass, delta_v = burn_fuel(current_mass, fuel_mass, burn_rate, exhaust_velocity, time_step)
        velocity += delta_v
        velocities.append(velocity)
        masses.append(current_mass)

        if t != 0:
            acceleration_values = (velocities[int(t)] - velocities[int(t - 1)]) / (times[int(t)] - times[int(t - 1)])
            # Berechnung der zurückgelegten Strecke über die Zeit (vereinfacht zu s = v * t)
            distance = velocity * t + 0.5 * acceleration_values * t ** 2

        luftwiderstand_werte.append(luftwiderstand(T0, rho0, g, M, R, cw, A, v, t))

        accelerations.append(acceleration_values)
        distances.append(distance)

    return np.array(times), np.array(masses), np.array(velocities), np.array(accelerations), np.array(distances), np.array(luftwiderstand_werte)

def luftdichte(T0, rho0, g, M, R, cw, A, v, h):
    T = T0 - 0.0065 * h  # Temperatur in Kelvin
    rho = rho0 * math.exp(-g * M * h / (R * T))
    return rho

def luftwiderstand(T0, rho0, g, M, R, cw, A, v, h):
    rho = luftdichte(T0, rho0, g, M, R, cw, A, v, h)
    FL = 0.5 * cw * rho * A * v ** 2
    return FL

def animate(i, times, masses, velocities, luftwiderstand_werte, accelerations, distances, axs):
    if i < len(times):
        for ax in axs.flatten():
            ax.clear()  # Clear the previous plot
        # Raketen-Simulationsgrafiken in den ersten beiden Subplots plotten
        axs[0, 2].plot(times[:i], masses[:i])
        axs[0, 2].set_title('Raketenmasse über Zeit')
        axs[0, 2].set_xlabel('Zeit (s)')
        axs[0, 2].set_ylabel('Masse (kg)')

        axs[0, 1].plot(times[:i], velocities[:i])
        axs[0, 1].set_title('Raketen-Geschwindigkeit über Zeit')
        axs[0, 1].set_xlabel('Zeit (s)')
        axs[0, 1].set_ylabel('Geschwindigkeit (m/s)')

        # Luftwiderstand
        axs[1, 0].plot(times[:i], luftwiderstand_werte[:i])
        axs[1, 0].set_title('Luftwiderstand während des Raketenstarts')
        axs[1, 0].set_xlabel('Zeit (s)')
        axs[1, 0].set_ylabel('Luftwiderstand (N)')

        axs[1, 1].plot(times[:i], accelerations[:i])
        axs[1, 1].set_title('Beschleunigung über Zeit')
        axs[1, 1].set_xlabel('Zeit (s)')
        axs[1, 1].set_ylabel('Beschleunigung (m/s²)')

        axs[0, 0].plot(times[:i], distances[:i])
        axs[0, 0].set_title('Zurückgelegte Strecke über Zeit')
        axs[0, 0].set_xlabel('Zeit (s)')
        axs[0, 0].set_ylabel('Distanz (m)')

def animate_two_stage(i, times, masses, velocities, luftwiderstand_werte, accelerations, distances, axs):
    if i < len(times):
        for ax in axs.flatten():
            ax.clear()  # Clear the previous plot
        # Raketen-Simulationsgrafiken in den ersten beiden Subplots plotten
        axs[0, 2].plot(times[:i], masses[:i])
        axs[0, 2].set_title('Raketenmasse über Zeit')
        axs[0, 2].set_xlabel('Zeit (s)')
        axs[0, 2].set_ylabel('Masse (kg)')

        axs[0, 1].plot(times[:i], velocities[:i])
        axs[0, 1].set_title('Raketen-Geschwindigkeit über Zeit')
        axs[0, 1].set_xlabel('Zeit (s)')
        axs[0, 1].set_ylabel('Geschwindigkeit (m/s)')

        # Luftwiderstand
        axs[1, 0].plot(times[:i], luftwiderstand_werte[:i])
        axs[1, 0].set_title('Luftwiderstand während des Raketenstarts')
        axs[1, 0].set_xlabel('Zeit (s)')
        axs[1, 0].set_ylabel('Luftwiderstand (N)')

        np.round(accelerations, 4)
        axs[1, 1].plot(times[:i], accelerations[:i])
        axs[1, 1].set_title('Beschleunigung über Zeit')
        axs[1, 1].set_xlabel('Zeit (s)')
        axs[1, 1].set_ylabel('Beschleunigung (m/s²)')

        axs[0, 0].plot(times[:i], distances[:i])
        axs[0, 0].set_title('Zurückgelegte Strecke über Zeit')
        axs[0, 0].set_xlabel('Zeit (s)')
        axs[0, 0].set_ylabel('Distanz (m)')

def show_graphs():
    # Rocket simulation Daten generieren
    constants = load_constants('Json_settings/current_values.json')
    settings = load_settings('Json_settings/settings.json')
    update_time = int(1000 / int(settings["update_parameters_settings"]))

    g = constants["g"]
    M = constants["molar_mass_air"]
    R = constants["gas_constant"]
    T0 = constants["temperature_sea_level"]
    rho0 = constants["air_density_sea_level"]

    try:
        initial_mass = float(input_initial_mass.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Anfangsmasse muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        fuel_mass = float(input_fuel_mass.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Treibstoffmasse muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        exhaust_velocity = float(input_v_e.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Ausstoßgeschwindigkeit muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        burn_rate = float(input_burn_rate.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Brennrate muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        total_time = float(input_duration.get().replace(".", "").replace(",", ".")) + 1
    except ValueError:
        message = "Die Dauer muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        time_step = float(input_steps.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Zeitschrittgröße muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        cw = float(input_Cw.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Der Strömungswiderstand muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        A = float(input_A.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Fläche muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        v = float(input_v.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Geschwindigkeit muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    times, masses, velocities, accelerations, distances, luftwiderstand_werte = simulate_rocket(initial_mass, fuel_mass, exhaust_velocity, burn_rate, total_time, time_step, g, T0, rho0, M, R, cw, A, v)

    # Erstelle eine Matplotlib-Figur mit einem Raster von 6 Subplots (3x2)
    fig = Figure(figsize=(10, 15), dpi=100)
    axs = fig.subplots(2, 3)  # 3x2 Raster von Subplots erstellen
    fig.delaxes(axs[1, 2])

    # Lösche das show_frame bevor neuer Inhalt hinzugefügt wird
    for widget in show_frame.winfo_children():
        widget.destroy()

    # Erstelle eine Leinwand, um die Figur im customtkinter Fenster anzuzeigen
    canvas = FigureCanvasTkAgg(fig, master=show_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Animation initialisieren und speichern in einer Attribute des show_graphs
    show_graphs.ani = FuncAnimation(fig, animate, frames=len(times), fargs=(times, masses, velocities, luftwiderstand_werte, accelerations, distances, axs), interval=update_time, repeat=False)

    # Figur für späteren Gebrauch speichern
    show_graphs.fig = fig
    log_graphs(time_step, total_time)
    update_parameters(0, times, masses, velocities, accelerations, distances)

def show_graphs_two_stage():
    # Rocket simulation Daten generieren
    constants = load_constants('Json_settings/current_values.json')
    settings = load_settings('Json_settings/settings.json')
    update_time = int(1000 / int(settings["update_parameters_settings"]))

    g = constants["g"]
    M = constants["molar_mass_air"]
    R = constants["gas_constant"]
    T0 = constants["temperature_sea_level"]
    rho0 = constants["air_density_sea_level"]

    try:
        initial_mass = float(input_initial_mass.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Anfangsmasse muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        fuel_mass_stage1 = float(input_fuel_mass.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Treibstoffmasse der ersten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        exhaust_velocity_stage1 = float(input_v_e.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Ausstoßgeschwindigkeit der ersten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        burn_rate_stage1 = float(input_burn_rate.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Brennrate der ersten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        fuel_mass_stage2 = float(input_fuel_mass_stage2.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Treibstoffmasse der zweiten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        exhaust_velocity_stage2 = float(input_v_e_stage2.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Ausstoßgeschwindigkeit der zweiten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        burn_rate_stage2 = float(input_burn_rate_stage2.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Brennrate der zweiten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        total_time = float(input_duration.get().replace(".", "").replace(",", ".")) + 1
    except ValueError:
        message = "Die Dauer muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        time_step = float(input_steps.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Zeitschrittgröße muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        cw = float(input_Cw.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Der Strömungswiderstand muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        A = float(input_A.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Fläche muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        v = float(input_v.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Geschwindigkeit muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    try:
        A_stage2 = float(input_A_stage2.get().replace(".", "").replace(",", "."))
    except ValueError:
        message = "Die Fläche der zweiten Stufe muss eine Zahl sein."
        messagebox.showerror("Fehler", message)
        log_error(message)
        return

    # Run the simulation
    times, masses, velocities, accelerations, distances, luftwiderstand_werte = simulate_rocket_two_stages(
        initial_mass, fuel_mass_stage1, exhaust_velocity_stage1, burn_rate_stage1,
        fuel_mass_stage2, exhaust_velocity_stage2, burn_rate_stage2, total_time, time_step, g, cw, A, A_stage2, rho0, T0, M, R, v
    )

    fig = Figure(figsize=(10, 15), dpi=100)
    axs = fig.subplots(2, 3)  # 3x2 Raster von Subplots erstellen
    fig.delaxes(axs[1, 2])

    # Lösche das show_frame bevor neuer Inhalt hinzugefügt wird
    for widget in show_frame.winfo_children():
        widget.destroy()

    # Erstelle eine Leinwand, um die Figur im customtkinter Fenster anzuzeigen
    canvas = FigureCanvasTkAgg(fig, master=show_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Animation initialisieren und speichern in einer Attribute des show_graphs_two_stage
    show_graphs_two_stage.ani = FuncAnimation(fig, animate_two_stage, frames=len(times), fargs=(times, masses, velocities, luftwiderstand_werte, accelerations, distances, axs), interval=update_time, repeat=False)

    # Figur für späteren Gebrauch speichern
    show_graphs_two_stage.fig = fig
    log_graphs(time_step, total_time)
    update_parameters(0, times, masses, velocities, accelerations, distances)

def simulate_rocket_two_stages(initial_mass, fuel_mass_stage1, exhaust_velocity_stage1, burn_rate_stage1,
                               fuel_mass_stage2, exhaust_velocity_stage2, burn_rate_stage2, total_time, time_step, g, cw, A, A_stage2, rho0, T0, M, R, v):
    global delta_v
    times = np.arange(0, total_time, time_step)
    masses = []
    velocities = [0]
    accelerations = [9.81]
    distances = [0]
    luftwiderstand_werte = []

    mass = initial_mass
    velocity = 0
    stage = 1
    distance = 0
    acceleration_value = g
    current_mass = initial_mass



    for t in times:
        if stage == 1:
            if fuel_mass_stage1 > 0:
                fuel_mass_stage1 -= burn_rate_stage1 * time_step
                thrust = burn_rate_stage1 * exhaust_velocity_stage1
                old_mass = mass
                mass -= burn_rate_stage1 * time_step
                delta_v = exhaust_velocity_stage1 * np.log(old_mass / mass)
            else:
                stage = 2
                thrust = 0

        if stage == 2:
            if fuel_mass_stage2 > 0:
                fuel_mass_stage2 -= burn_rate_stage2 * time_step
                thrust = burn_rate_stage2 * exhaust_velocity_stage2
                old_mass = mass
                mass -= burn_rate_stage2 * time_step
                delta_v = exhaust_velocity_stage2 * np.log(old_mass / mass)
            else:
                thrust = 0


        velocity += delta_v

        masses.append(mass)
        velocities.append(velocity)

        if t != 0:
            acceleration_values = (velocities[int(t)] - velocities[int(t - 1)]) / (times[int(t)] - times[int(t - 1)])
            # Berechnung der zurückgelegten Strecke über die Zeit (vereinfacht zu s = v * t)
            distance = velocity * t + 0.5 * acceleration_values * t ** 2

        luftwiderstand_werte.append(luftwiderstand(T0, rho0, g, M, R, cw, A, v, t))

        accelerations.append(acceleration_value)
        distances.append(distance)

    return times, masses, velocities, accelerations, distances, luftwiderstand_werte

def export_graphs():
    if hasattr(show_graphs, 'fig'):
        dialog = ctk.CTkInputDialog(text="Geben Sie den Projektnamen ein:", title="Projektname")
        project_name = dialog.get_input()
        if project_name:
            save_subplots_as_images(show_graphs.fig, project_name)
        else:
            messagebox.showerror("Fehler", "Projektname wurde nicht eingegeben")
    elif hasattr(show_graphs_two_stage, 'fig'):
        dialog = ctk.CTkInputDialog(text="Geben Sie den Projektnamen ein:", title="Projektname")
        project_name = dialog.get_input()
        if project_name:
            save_subplots_as_images(show_graphs_two_stage.fig, project_name)
        else:
            messagebox.showerror("Fehler", "Projektname wurde nicht eingegeben")
    else:
        messagebox.showerror("Fehler", f"Keine Graphen zum Exportieren")

def reset_default():
    # Update input fields with values from the JSON file
    input_A.delete(0, tk.END)
    input_A.insert(0, "10.0")
    input_Cw.delete(0, tk.END)
    input_Cw.insert(0, "0.3")
    input_v.delete(0, tk.END)
    input_v.insert(0, "100.0")
    input_duration.delete(0, tk.END)
    input_duration.insert(0, "100.0")
    input_steps.delete(0, tk.END)
    input_steps.insert(0, 1.0)
    input_initial_mass.delete(0, tk.END)
    input_initial_mass.insert(0, "500.0")
    input_v_e.delete(0, tk.END)
    input_v_e.insert(0, "2500.0")
    input_fuel_mass.delete(0, tk.END)
    input_fuel_mass.insert(0, "300.0")
    input_burn_rate.delete(0, tk.END)
    input_burn_rate.insert(0, "2.0")

def show_select():
    fm_2 = input_fuel_mass_stage2.get()
    a_2 = input_A_stage2.get()
    v_e_2 = input_v_e_stage2.get()
    br_2 = input_burn_rate_stage2.get()

    if fm_2 and a_2 and v_e_2 and br_2 != "":
        print("2 stages")
        show_graphs_two_stage()
    else:
        print("One stage")
        show_graphs()

root = ctk.CTk()
root.geometry("2500x1000")
root.title("AstralSim")
settings = load_settings('Json_settings/settings.json')
if settings["dark_mode"]:
    ctk.set_appearance_mode("dark")
    plt.style.use('dark_background')
    color='black'
else:
    ctk.set_appearance_mode("light")
    color='#f2fafc'

#Tastenkombis
root.bind("<Control-s>", lambda event: save())
root.bind("<Control-l>", lambda event: import_json())
root.bind("<Return>", lambda event: show_select())
root.bind("<Control-r>", lambda event: reset_default())

# Menu bar Title buttons
menu = CTkMenuBar(root)
button_1 = menu.add_cascade("Datei")
button_2 = menu.add_cascade("Erweitert")
button_3 = menu.add_cascade("Über")

# Menu Bar - Datei
dropdown1 = CustomDropdownMenu(widget=button_1)
dropdown1.add_option(option="Öffnen", command=import_json)
dropdown1.add_option(option="Speichern", command=save)
dropdown1.add_separator()
dropdown1.add_option("Graphen exportieren", command=export_graphs)
dropdown1.add_option("Als Ordner exportieren", command=export_project)
dropdown1.add_option("Ordner öffnen", command=open_path)

# Menu Bar - Experte
dropdown2 = CustomDropdownMenu(widget=button_2)
dropdown2.add_option(option="Einstellungen", command=open_advanced_settings)
dropdown2.add_option(option="Log", command=show_log)

# Menu Bar - Über
dropdown3 = CustomDropdownMenu(widget=button_3)
dropdown3.add_option(option="Impressum", command=impressum)
dropdown3.add_separator()
dropdown3.add_option(option="Infos", command=leika)
dropdown3.add_separator()
dropdown3.add_option(option="Quiz", command=quiz_main)

# Frames
side_frame = ctk.CTkFrame(root, width=400, corner_radius=0)
side_frame.pack(side='left', fill='y', expand=False)
show_frame = ctk.CTkScrollableFrame(root, corner_radius=0, fg_color=color, width=300)
show_frame.pack(side='left', fill='both', expand=True)

# Side Frame Elements
def option_files(choice):
    if choice == "Auswählen":
        return  # No file selected, do nothing

    # Load the selected JSON file
    file_path = os.path.join("Saves", choice)  # Assuming "Saves" is the directory where JSON files are stored
    try:
        with open(file_path, "r") as json_file:
            input_values = json.load(json_file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{choice}' not found.")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Invalid JSON format in '{choice}'.")
        return

    # Update input fields with values from the JSON file
    input_A.delete(0, tk.END)
    input_A.insert(0, input_values.get("Fläche", "").replace(".", ","))
    input_Cw.delete(0, tk.END)
    input_Cw.insert(0, input_values.get("Strömungswiderstand", "").replace(".", ","))
    input_v.delete(0, tk.END)
    input_v.insert(0, input_values.get("Geschwindigkeit", "").replace(".", ","))
    input_duration.delete(0, tk.END)
    input_duration.insert(0, input_values.get("Dauer", "").replace(".", ","))
    input_steps.delete(0, tk.END)
    input_steps.insert(0, input_values.get("Schrittweite", "").replace(".", ","))
    input_initial_mass.delete(0, tk.END)
    input_initial_mass.insert(0, input_values.get("Initial Mass", "").replace(".", ","))
    input_v_e.delete(0, tk.END)
    input_v_e.insert(0, input_values.get("Ausstoßgeschwindigkeit", "").replace(".", ","))
    input_fuel_mass.delete(0, tk.END)
    input_fuel_mass.insert(0, input_values.get("Fuel Mass", "").replace(".", ","))
    input_burn_rate.delete(0, tk.END)
    input_burn_rate.insert(0, input_values.get("Burn Rate", "").replace(".", ","))
    input_A_stage2.delete(0, tk.END)
    input_A_stage2.insert(0, input_values.get("Fläche 2", "").replace(".", ","))
    input_v_e_stage2.delete(0, tk.END)
    input_v_e_stage2.insert(0, input_values.get("Ausstoßgeschwindigkeit 2", "").replace(".", ","))
    input_fuel_mass_stage2.delete(0, tk.END)
    input_fuel_mass_stage2.insert(0, input_values.get("Fuel Mass 2", "").replace(".", ","))
    input_burn_rate_stage2.delete(0, tk.END)
    input_burn_rate_stage2.insert(0, input_values.get("Burn Rate 2", "").replace(".", ","))

    show_select()

# Define a global counter to keep track of the number of times the function is called
call_count = 0


def update_parameters(index_u, times, masses, velocities, accelerations, distances):
    global call_count

    settings = load_settings('Json_settings/settings.json')
    real_time_update = int(1000 / int(settings["update_parameters_settings"]))

    # Increment the call counter
    call_count += 1

    # Check if the function has been called less than 2 times
    if call_count < 3:
        # Do nothing and return immediately
        root.after(real_time_update+100, update_parameters, index_u, times, masses, velocities, accelerations, distances)
        return

    # Check if the index is within the arrays
    if index_u < len(times):
        # Calculate current values of the parameters
        current_time = times[index_u].round(2)
        current_mass = round(masses[index_u], 2)
        current_velocity = round(velocities[index_u], 2)
        current_acceleration = round(accelerations[index_u], 2)
        current_distance = round(distances[index_u], 2)

        # Update the user interface with the current values
        label_current_time.configure(text=f"{current_time} s")
        label_current_mass.configure(text=f"{current_mass} kg")
        label_current_velocity.configure(text=f"{current_velocity} m/s")
        label_current_acceleration.configure(text=f"{current_acceleration} m/s²")
        label_current_distance.configure(text=f"{current_distance} m")

        # Schedule the next update
        root.after(real_time_update, update_parameters, index_u + 1, times, masses, velocities, accelerations,
                   distances)
    else:
        index_u = 0

# Directory containing the JSON files
json_directory = "Saves"

# Get a list of all JSON files in the directory
vals_rockets = ["Numero Uno", "Numero Dos"]

def update_files_dropdown():
    global json_files
    json_files_new = [file for file in os.listdir(json_directory) if file.endswith(".json")]
    if json_files != json_files_new:
        filemenu.configure(values=json_files_new)
        json_files = json_files_new
        root.after(1000, update_files_dropdown)

    else:
        root.after(1000, update_files_dropdown)

json_files = [file for file in os.listdir(json_directory) if file.endswith(".json")]

# Filemenu
filemenu = ctk.CTkOptionMenu(side_frame, values=json_files, command=option_files, width=200)
filemenu.set("Auswählen")
update_files_dropdown()

# Input variables
input_width = 200

# Inputs
input_A = ctk.CTkEntry(side_frame, placeholder_text="Fläche", width=input_width)
input_Cw = ctk.CTkEntry(side_frame, placeholder_text="Cw", width=input_width)
input_v = ctk.CTkEntry(side_frame, placeholder_text="Geschwindigkeit", width=input_width)
input_duration = ctk.CTkEntry(side_frame, placeholder_text="Dauer", width=input_width)
input_steps = ctk.CTkEntry(side_frame, placeholder_text="Schrittweite", width=input_width)
input_initial_mass = ctk.CTkEntry(side_frame, placeholder_text="Initial Mass", width=input_width)
input_v_e = ctk.CTkEntry(side_frame, placeholder_text="Ausstoßgeschwindigkeit", width=input_width)
input_fuel_mass = ctk.CTkEntry(side_frame, placeholder_text="Fuel Mass", width=input_width)
input_burn_rate = ctk.CTkEntry(side_frame, placeholder_text="Fuel Mass", width=input_width)
input_A_stage2 = ctk.CTkEntry(side_frame, placeholder_text="Fläche Stufe 2", width=input_width)
input_v_e_stage2 = ctk.CTkEntry(side_frame, placeholder_text="Ausstoßgeschwindigkeit Stufe 2", width=input_width)
input_fuel_mass_stage2 = ctk.CTkEntry(side_frame, placeholder_text="Fuel Mass Stufe 2", width=input_width)
input_burn_rate_stage2 = ctk.CTkEntry(side_frame, placeholder_text="Burn Rate Stufe 2", width=input_width)

#Label
label_A = ctk.CTkLabel(side_frame, text="Fläche:", fg_color="transparent")
label_Cw = ctk.CTkLabel(side_frame, text="Strömungswiderstand:", fg_color="transparent")
label_v = ctk.CTkLabel(side_frame, text="Geschwindigkeit:", fg_color="transparent")
label_duration = ctk.CTkLabel(side_frame, text="Dauer:", fg_color="transparent")
label_steps = ctk.CTkLabel(side_frame, text="Schrittweite:", fg_color="transparent")
label_initial_mass = ctk.CTkLabel(side_frame, text="Initial Mass:", fg_color="transparent")
label_v_e = ctk.CTkLabel(side_frame, text="Ausstoßgeschwindigkeit:", fg_color="transparent")
label_fuel_mass = ctk.CTkLabel(side_frame, text="Fuel Mass:", fg_color="transparent")
label_burn_rate = ctk.CTkLabel(side_frame, text="Burn Rate:", fg_color="transparent")
label_A_stage2 = ctk.CTkLabel(side_frame, text="Fläche (2):", fg_color="transparent")
label_v_e_stage2 = ctk.CTkLabel(side_frame, text="Ausstoßgeschwindigkeit 2", fg_color="transparent")
label_fuel_mass_stage2 = ctk.CTkLabel(side_frame, text="Fuel Mass (2):", fg_color="transparent")
label_burn_rate_stage2 = ctk.CTkLabel(side_frame, text="Burn Rate (2):", fg_color="transparent")

# Button
button_do = ctk.CTkButton(side_frame, text="Graphen anzeigen", command=show_select)

#Current values
label_title_current = ctk.CTkLabel(side_frame, text="Daten in Echtzeit", font=("CTkFont",25))

label_time = ctk.CTkLabel(side_frame,         text="Zeit")
label_mass = ctk.CTkLabel(side_frame,         text="Masse")
label_velocity = ctk.CTkLabel(side_frame,     text="Geschwindigkeit")
label_acceleration = ctk.CTkLabel(side_frame, text="Beschleunigung")
label_distance = ctk.CTkLabel(side_frame,     text="Strecke")

label_current_time = ctk.CTkLabel(side_frame,         text="n/a")
label_current_mass = ctk.CTkLabel(side_frame,         text="n/a")
label_current_velocity = ctk.CTkLabel(side_frame,     text="n/a")
label_current_acceleration = ctk.CTkLabel(side_frame, text="n/a")
label_current_distance = ctk.CTkLabel(side_frame,     text="n/a")

# Place widgets
filemenu.place(x=(400-200)/2, y=10)
input_A.place(x=((400 - input_width) / 2) + 67, y=50)
label_A.place(x=15, y=50)
input_Cw.place(x=((400 - input_width) / 2 + 67), y=90)
label_Cw.place(x=15, y= 90)
input_v.place(x=((400 - input_width) / 2 + 67), y=130)
label_v.place(x=15, y= 130)
input_duration.place(x=((400 - input_width) / 2 + 67), y=170)
label_duration.place(x=15, y= 170)
input_steps.place(x=((400 - input_width) / 2 + 67), y=210)
label_steps.place(x=15, y= 210)
input_initial_mass.place(x=((400 - input_width) / 2 + 67), y=250)
label_initial_mass.place(x=15, y= 250)
input_v_e.place(x=((400 - input_width) / 2 + 67), y=290)
label_v_e.place(x=15, y= 290)
input_fuel_mass.place(x=((400 - input_width) / 2 + 67), y=330)
label_fuel_mass.place(x=15, y= 330)
input_burn_rate.place(x=((400 - input_width) / 2 + 67), y=370)
label_burn_rate.place(x=15, y= 370)
input_A_stage2.place(x=((400 - input_width) / 2) + 67, y=410)
label_A_stage2.place(x=15, y=410)
input_v_e_stage2.place(x=((400 - input_width) / 2) + 67, y=450)
label_v_e_stage2.place(x=15, y=450)
input_fuel_mass_stage2.place(x=((400 - input_width) / 2) + 67, y=490)
label_fuel_mass_stage2.place(x=15, y=490)
input_burn_rate_stage2.place(x=((400 - input_width) / 2) + 67, y=530)
label_burn_rate_stage2.place(x=15, y=530)
button_do.place(x=125, y=570)

label_title_current.place(x= 15, y=610)

label_time.place(x= 15, y= 650)
label_mass.place(x= 15, y= 690)
label_velocity.place(x= 15, y=730)
label_acceleration.place(x= 15, y= 770)
label_distance.place(x= 15, y= 810)

label_current_time.place(x= 175, y= 650)
label_current_mass.place(x= 175, y= 690)
label_current_velocity.place(x= 175, y=730)
label_current_acceleration.place(x= 175, y= 770)
label_current_distance.place(x= 175, y= 810)

#Fill entrys with basic value
input_initial_mass.insert(tk.END, "500,0")
input_fuel_mass.insert(tk.END, "300,0")
input_v_e.insert(tk.END, "2500,0")
input_burn_rate.insert(tk.END, "2,0")
input_duration.insert(tk.END, "100,0")
input_steps.insert(tk.END, "1,0")
input_A.insert(tk.END, "10,0")
input_Cw.insert(tk.END, "0,3")
input_v.insert(tk.END, "100,0")

root.mainloop()