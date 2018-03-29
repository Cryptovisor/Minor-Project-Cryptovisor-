from coinmarketcap import Market
import tkinter as tk                
from tkinter import font  as tkfont
import pandas as pd
#####################################BACKEND##############################################################################################
curr =  {'Bitcoin Cash' : 'bch', 'Bitcoin' : 'btc', 'Dash' : 'dash', 'Decred' : 'dcr', 'Dogecoin' : 'doge',
         'Ethereum Classic' : 'etc', 'Ethereum' : 'eth', 'Litecoin' : 'ltc', 'PIVX' : 'pivx', 'Vertcoin' : 'vtc',
         'NEM' : 'xem', 'Monero' : 'xmr', 'Zcash' : 'zec'}

cp = Market()
def PriceFinder(*args,**kwargs):   #args are currencies choosen by user
	currencies = []       #Will hold currencies choosen by user
	for i in args:
		currencies.append(i)
	#print(currencies)
	
	prices = []
	for j in currencies:
		real_time_price = cp.ticker(currency=str(j),limit=1,convert='USD') 
		prices.append(real_time_price[0]['price_usd'])

	#print(prices)
	currency_dict = dict(zip(currencies,prices))
	extract(currency_dict)

def extract(price_dictionary):

	mean_of_30_Days = {}
	curr_list = list(price_dictionary.keys())
	for i in curr_list:
		data = pd.read_csv('DataSets\\'+curr[i].strip('')+'.csv',skiprows = range(1,337))
		prices = data.price_USD.tolist()
		summation = sum(prices)/30
		mean_of_30_Days[i] = summation
	performance(mean_of_30_Days,price_dictionary)


def performance(mean_of_30_Days,price_dictionary):  #gives 30 days performance of a currency
	currencyList = [str(i[0]) for i in mean_of_30_Days.items()]
	meanList = [float(i[1]) for i in mean_of_30_Days.items()]
	priceList = [float(i[1]) for i in price_dictionary.items()]
	performanceList = [priceList[i] - meanList[i] for i in range(min(len(priceList),len(meanList)))]
	performance_Dictionary = dict(zip(currencyList,performanceList))
	#print(performance_Dictionary)
	WeightDistributor(performance_Dictionary,price_dictionary)
	
	
def WeightDistributor(performance_Dictionary,price_dictionary):   #This algorithm will define weights
	weights = []
	Pf = [float(i[1]) for i in price_dictionary.items()] #real time price
	#print(Pf)
	Gh = [float(i[1]) for i in performance_Dictionary.items()]    #gain-drop in previous 30 days
	#print(Gh)
	C = [str(i[0]) for i in performance_Dictionary.items()]
	#print(C)
	for i in tuple(zip(Pf,Gh)):
		temp_var = ((i[1]*i[0])/(i[0]-i[1]))%30
		weights.append(round(temp_var,3))
	#print(weights)
	FractionalKnapsack(capacity,weights,Pf)

def FractionalKnapsack(capacity,weights,Pf):
	#print(capacity,weights,Pf)
#PriceFinder('Bitcoin','Ethereum','Litecoin','Dash')
#############################################FRONTEND################################################################################
class Engine(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
class StartPage(tk.Frame):        #Welcome
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Investements using Greedy Algorithm", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button1.place(relx=.8, rely=.9)
class PageOne(tk.Frame):      #ChooseAmount
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Your Amount", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(relx=.5, rely=.9)
        button1 = tk.Button(self, text="Next",
                           command=lambda: controller.show_frame("PageTwo"))
        button1.place(relx=.8, rely=.9)
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("PageOne"))
        button.place(relx=.9, rely=.10)
        button2 = tk.Button(self, text="Next",
                           command=lambda: controller.show_frame("PageOne"))
        button2.place(relx=.8, rely=.9)


if __name__ == "__main__":
    app = Engine()
    app.mainloop()
