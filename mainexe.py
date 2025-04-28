import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

interest = ctrl.Antecedent(np.arange(0, 11, 1), 'interest')
popularity = ctrl.Antecedent(np.arange(0, 11, 1), 'popularity')
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

interest.automf(3)
popularity.automf(3)

recommendation['low'] = fuzz.trimf(recommendation.universe, [0, 0, 5])
recommendation['medium'] = fuzz.trimf(recommendation.universe, [0, 5, 10])
recommendation['high'] = fuzz.trimf(recommendation.universe, [5, 10, 10])

rule1 = ctrl.Rule(interest['poor'] | popularity['poor'], recommendation['low'])
rule2 = ctrl.Rule(interest['average'] & popularity['average'], recommendation['medium'])
rule3 = ctrl.Rule(interest['good'] | popularity['good'], recommendation['high'])

recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
recommendation_simulator = ctrl.ControlSystemSimulation(recommendation_ctrl)

window = tk.Tk()
window.title("Fuzzy E-Commerce Product Recommender")
window.geometry("600x400")
window.configure(bg="#f0f8ff")
window.minsize(500, 350)
window.resizable(True, True)

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 14), background="#f0f8ff")
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TEntry", font=("Segoe UI", 12))

def calculate_recommendation():
    try:
        user_interest = float(interest_entry.get())
        product_pop = float(popularity_entry.get())

        if not (0 <= user_interest <= 10 and 0 <= product_pop <= 10):
            raise ValueError("Inputs must be between 0 and 10.")

        recommendation_simulator.input['interest'] = user_interest
        recommendation_simulator.input['popularity'] = product_pop
        recommendation_simulator.compute()

        result = recommendation_simulator.output['recommendation']
        recommendation_label.config(text=f"Recommendation Score: {result:.2f}/10")

        threshold = 5.70
        if result >= threshold:
            messagebox.showinfo("Recommendation Status", "Product is recommended!")
        else:
            messagebox.showwarning("Recommendation Status", 
                f"Product is not recommended.\nMinimum required score: {threshold:.1f}")
        
        plot_fuzzy_graph(result)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter numbers between 0 and 10.")

def reset_fields():
    interest_entry.delete(0, tk.END)
    popularity_entry.delete(0, tk.END)
    recommendation_label.config(text="Recommendation Score: —")

def plot_fuzzy_graph(score):
    x = np.arange(0, 11, 0.1)
    
    low = fuzz.trimf(x, [0, 0, 5])
    medium = fuzz.trimf(x, [0, 5, 10])
    high = fuzz.trimf(x, [5, 10, 10])
    
    plt.figure(figsize=(8, 6))
    plt.plot(x, low, label='Low', color='red')
    plt.plot(x, medium, label='Medium', color='orange')
    plt.plot(x, high, label='High', color='green')

    plt.axvline(x=score, color='blue', linestyle='--', label=f'Recommendation Score: {score:.2f}')

    plt.title("Fuzzy Recommendation Score")
    plt.xlabel("Recommendation Score")
    plt.ylabel("Membership Degree")
    plt.legend()
    plt.grid(True)
    
    plt.show()

frame = tk.Frame(window, bg="#f0f8ff")
frame.pack(expand=True, fill="both", padx=20, pady=20)

ttk.Label(frame, text="User Interest (0–10)").pack(pady=(10, 5))
interest_entry = ttk.Entry(frame, width=10)
interest_entry.pack()

ttk.Label(frame, text="Product Popularity (0–10)").pack(pady=(20, 5))
popularity_entry = ttk.Entry(frame, width=10)
popularity_entry.pack()

ttk.Button(frame, text="Get Recommendation", command=calculate_recommendation).pack(pady=20)
ttk.Button(frame, text="Reset", command=reset_fields).pack()

recommendation_label = ttk.Label(frame, text="Recommendation Score: —", font=("Segoe UI", 16, "bold"))
recommendation_label.pack(pady=30)


window.mainloop()
