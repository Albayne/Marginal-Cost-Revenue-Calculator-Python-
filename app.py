"""
Using the small incremental nature of marginal costs and revenue to derive them using derivatives
"""

#importing essential libraries
import sympy as sp                          #Performs higher level mathematics
import matplotlib.pyplot as plt             #Plots Graphs
from tkinter import *                      #Creates GUI interface
from tkinter import messagebox, Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


q=sp.Symbol('q')      #Turning q from String to a sympy symbol

#Creating the class Economic function
class EconomicFunction:
    def __init__(self,expr_string):
        try: #Exception handling
            self.expr=sp.sympify(expr_string) #Converts expr to a string
            self.derivative=sp.diff(self.expr,q) #Differentiates expr w.r.t q
        except Exception as e:
            raise ValueError(f"Invalid function{e}")

    def evaluate(self,q_val):
        """function that substitutes the q symbol with an actual numeric value"""
        return float(self.expr.subs(q,q_val))

    def marginal(self,q_val):
        """function that substitutes the q symbol in the derivative with an actual numeric value"""
        return float(self.derivative.subs(q,q_val))

class EconomicsModel:
    def __init__(self,revenue_str,cost_str):
        self.revenue=EconomicFunction(revenue_str)
        self.cost=EconomicFunction(cost_str)
        self.profit=EconomicFunction(str(self.revenue.expr-self.cost.expr))

    def optimal_quantity(self):
        """function that calculates the optimal quantity of to make revenue"""
        eq=sp.Eq(self.revenue.derivative,self.cost.derivative) #equation/function
        sols=sp.solve(eq,q) #solution to the equation eq
        real_solution=[float(s) for s in sols if s.is_real]
        return real_solution

    def plot(self, q_min=0,q_max=50):
        """function that plots the optimal quantity of to make revenue"""
        q_vals=list(range(q_min,q_max+1))
        #Table values
        R_vals=[self.revenue.evaluate(i) for i in q_vals]
        C_vals=[self.cost.evaluate(i) for i in q_vals]
        P_vals=[self.profit.evaluate(i) for i in q_vals]
        MR_vals=[self.revenue.marginal(i) for i in q_vals]
        MC_vals=[self.cost.marginal(i) for i in q_vals]

        #Actual graph plotting
        plt.figure(figsize=(10,6)) #Allocating scale to the graph
        plt.plot(q_vals,R_vals, label="Revenue R(q)",linewidth=2)
        plt.plot(q_vals,C_vals, label="Cost R(q)",linewidth=2)
        plt.plot(q_vals,P_vals, label="Profit pi(q)",linewidth=2)
        plt.plot(q_vals,MR_vals,'--', label="Marginal Revenue MR(q)")
        plt.plot(q_vals,MC_vals,'--', label="Marginal Cost MC(q)")
        #Determining the x-axes, and y-axes
        plt.xlabel("Quantity q")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

        #------------------GUI Interface-----------------------#

def build_gui():
    """function that builds the GUI"""
    root = Tk()
    root.title("Economics Marginal Analysis Tool") #Title of app interface
    root.geometry("500x450") #Size of app interface

    Label(root,text="Revenue Function R(q):").pack()
    rev_entry=Entry(root,width=40)
    rev_entry.pack()

    Label(root,text="Cost Function C(q):").pack()
    cost_entry=Entry(root,width=40)
    cost_entry.pack()

    Label(root,text="Quantity (q):").pack()
    q_entry=Entry(root,width=20)
    q_entry.pack()

    output=Text(root,width=60,height=10)
    output.pack()

    global graph_frame
    graph_frame = Frame(root)
    graph_frame.pack(pady=10)

    model={"obj":None}

    def load_model():
        """ function that loads the model"""
        try:
            model["obj"]=EconomicsModel(rev_entry.get(),cost_entry.get())
            output.insert(END,"functions loaded successfully.\n")
        except Exception as e:
            messagebox.showerror("Error",f"{e}")

    def evaluate():
        """ function that evaluates the model"""
        if not model["obj"]:
           messagebox.showwarning("Warning","Load Function First")
           return
        try:
           q_val=float(q_entry.get())
           m=model["obj"]
           output.insert(END,f"\nAt q={q_val}\n")
           output.insert(END,f"R(q)={m.revenue.evaluate(q_val)}\n")
           output.insert(END,f"C(q)={m.cost.evaluate(q_val)}\n")
           output.insert(END,f"Profit(q)={m.profit.evaluate(q_val)}\n")
           output.insert(END,f"MR(q)={m.revenue.marginal(q_val)}\n")
           output.insert(END,f"MC(q)={m.cost.marginal(q_val)}\n")
        except Exception as e:
            messagebox.showerror("Error",f"{e}")

    def find_optimal_quantity():
        """ function that finds the optimal quantity"""
        if not model["obj"]:
            messagebox.showwarning("Warning","Load Function First")
            return
        sols=model["obj"].optimal_quantity()
        if sols:
           output.insert(END,f"\n Optimal quantity (MR=MC): {sols}.\n")
        else:
           output.insert(END,"\n No real solution for MR = MC \n")

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    def plotgraph():
        if not model["obj"]:
            messagebox.showwarning("Warning", "Load Function First")
            return

        # Clear previous graph
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Generate the figure
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        q_vals = list(range(0, 51))
        R_vals = [model["obj"].revenue.evaluate(i) for i in q_vals]
        C_vals = [model["obj"].cost.evaluate(i) for i in q_vals]
        P_vals = [model["obj"].profit.evaluate(i) for i in q_vals]
        MR_vals = [model["obj"].revenue.marginal(i) for i in q_vals]
        MC_vals = [model["obj"].cost.marginal(i) for i in q_vals]

        ax.plot(q_vals, R_vals, label="Revenue R(q)")
        ax.plot(q_vals, C_vals, label="Cost C(q)")
        ax.plot(q_vals, P_vals, label="Profit π(q)")
        ax.plot(q_vals, MR_vals, '--', label="MR(q)")
        ax.plot(q_vals, MC_vals, '--', label="MC(q)")

        ax.set_xlabel("Quantity q")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    Button(root, text="Load Functions", command=load_model).pack(pady=5)
    Button(root, text="Evaluate at q", command=evaluate).pack(pady=5)
    Button(root, text="Find Optimal Quantity", command=find_optimal_quantity).pack(pady=5)
    Button(root, text="Plot Graph", command=plotgraph).pack(pady=5)

    root.mainloop()









if __name__ == "__main__":
    build_gui()





























