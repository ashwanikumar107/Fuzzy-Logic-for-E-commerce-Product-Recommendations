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
