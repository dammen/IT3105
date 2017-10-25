
import sys
sys.path.append('./')
sys.path.append('./tools')
from tkinter import *
from tkinter import ttk
from gann import Gann, Caseman
import tflowTools as TFT


class Application():
    def __init__(self):

        root = Tk()

        root.title("General Artificial Neural Network Interface")
        mainframe = ttk.Frame(root, padding="20 20 20 20")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.valid_input = False

        self.data_sources = [("Parity", 0),
                             ("Auto Encoder", 1),
                             ("Bit Counter", 2),
                             ("Segment Counter", 3),
                             ("MNIST", 4),
                             ("Wine Quality", 5),
                             ("Glass", 6),
                             ("Yeast", 7),
                             ("Hacker's Choice", 8)]

        self.data_source = IntVar()
        self.data_source.set(0)
        self.parameters = StringVar()

        self.labels = ["Network Dimensions",
                       "Hidden Activation Function",
                       "Output Activation Function",
                       "Cost Function",
                       "Learning Rate",
                       "Initial Weight Range",
                       "Epochs",
                       "Validation Fraction",
                       "Test Fraction",
                       "Minibatch Size",
                       "Map Batch Size",
                       "Validation intervall",
                       "Steps",
                       "Map Layers",
                       "Map Dendrograms",
                       "Display Weights",
                       "Display Biases", ]

        self.label_details = ["Eg. '2,25,12,2'",
                              "'relu' or 'sigmoid'",
                              "See tensorflow documentation for list of supported functions",
                              "'cross entropy' or 'mse'",
                              "",
                              "Eg. '0.3-0.7'",
                              "",
                              "",
                              "",
                              "",
                              "'0' = No map test",
                              "",
                              "",
                              "Eg. '2-3'",
                              "Eg. '1,3,4'",
                              "",
                              "", ]

        self.network_settings = []
        self.dims = []
        self.hidden_activation_function = ""
        self.output_activation_function = ""
        self.loss_function = ""
        self.learning_rate = 0
        self.initial_weight_range = []
        self.epochs = 0
        self.validationFraction = 0
        self.testFraction = 0
        self.minibatch_size = 0
        self.map_batch_size = 0
        self.validation_interval = 0
        self.steps = 0
        self.map_layers = 0
        self.map_dendrograms = 0
        self.display_weights = 0
        self.display_biases = 0

        self.status = StringVar()

        for i in range(len(self.labels)):
            self.network_settings.append(StringVar())

        self.create_widgets(mainframe)

        root.mainloop()

    def create_widgets(self, frame):

        ttk.Label(frame, text="Data Source:", font=("Arial", 20)).grid(
            column=0, pady=10, padx=10)

        for (lbl, val) in self.data_sources:
            ttk.Radiobutton(frame, text=lbl,
                            variable=self.data_source, value=val).grid(column=0, padx=15, pady=5)

        ttk.Label(frame, text="Parameters:", font=("Arial", 10, "italic")).grid(
            column=0)

        ttk.Entry(frame, textvariable=self.parameters).grid(
            column=0)

        ttk.Label(frame, text="Settings:", font=("Arial", 20)).grid(
            columnspan=3, row=0, column=1, pady=10)

        for i in range(0, len(self.labels)):
            ttk.Label(frame, text=self.labels[i]).grid(
                column=1, row=i + 1, sticky=E, padx=5, pady=5)
            ttk.Entry(frame, text="", textvariable=self.network_settings[i]).grid(
                column=2, row=i + 1, sticky=E, padx=5, pady=5)
            ttk.Label(frame, text=self.label_details[i], font=("Arial", 10, "italic")).grid(
                column=3, row=i + 1, sticky=W, padx=5, pady=5)

        ttk.Button(frame, text="Validate",
                   command=self.validate).grid(column=0, row=20)
        ttk.Button(frame, text="Initialize",
                   command=self.initialize).grid(column=1, row=20)
        ttk.Button(frame, text="autofill",
                   command=self.autofill).grid(column=2, row=20)
        ttk.Button(frame, text="Run network",
                   command=self.run_network).grid(column=3, row=20)

        ttk.Label(frame, text="Status", font=("Arial", 20)
                  ).grid(row=21, column=1, pady=10)
        ttk.Entry(frame, textvariable=self.status).grid(
            column=2, row=21, columnspan=2)

    def validate(self):
        try:
            self.params = self.parameters.get()
            print(self.network_settings[0].get())
            self.dims = [int(x)
                         for x in self.network_settings[0].get().split(" ")]
            self.hidden_activation_function = self.network_settings[1].get()
            print(self.hidden_activation_function, "validate")
            #self.output_activation_function = self.network_settings[2].get()
            #self.loss_function = self.network_settings[3].get()
            self.learning_rate = float(self.network_settings[4].get())
            #self.initial_weight_range = [float(x) for x in self.network_settings[5].get().split("-")]
            self.epochs = int(self.network_settings[6].get())
            print("epochs", self.epochs)
            self.vfrac = float(self.network_settings[7].get())
            self.tfrac = float(self.network_settings[8].get())
            print("mbs", self.network_settings[9].get())

            self.mbs = int(self.network_settings[9].get())
            #self.map_batch_size = int(self.network_settings[10].get())
            print("vint", self.network_settings[11].get())

            self.vint = int(self.network_settings[11].get())
            # self.steps = int(self.network_settings[12].get())      WHY ?
            #self.map_layers = int(self.network_settings[13].get())
            #self.dendrograms = int(self.network_settings[14].get())
            #self.display_weights = int(self.network_settings[15].get())
            #self.biases = int(self.network_settings[16].get())
            self.valid_input = True

        except Exception as e:
            print(str(e))
            self.valid_input = False

    def initialize(self):

        self.status.set("initializing dataset")
        self.cman = Caseman(cfunc=self.case, params=self.params,
                            vfrac=self.vfrac, tfrac=self.tfrac)
        self.status.set("Initializing GANN")
        self.ann = Gann(dims=self.dims, cman=self.cman, lrate=self.lrate,
                        showint=self.showint, mbs=self.mbs, vint=self.vint, softmax=self.sm, hidden_activation_function=self.hidden_activation_function)
        # Plot a histogram and avg of the incoming weights to module 0.
        self.ann.gen_probe(0, 'wgt', ('hist', 'avg'))
        # Plot average and max value of module 1's output vector
        # ann.gen_probe(1, 'out', ('avg', 'max'))
        # Add a grabvar (to be displayed in its own matplotlib window).
        # ann.add_grabvar(0, 'wgt')
        self.status.set("initialization was succesful")

    def autofill(self):
        case = int(self.data_source.get())
        mapping = self.getMapping(case)
        params = self.getParams(case)
        dims = self.getDims(case)
        self.case = case
        self.params = params
        self.dims = dims.split(" ")
        self.epochs = mapping[0]
        self.lrate = mapping[1]
        self.showint = mapping[2]
        self.mbs = mapping[3]
        self.vfrac = mapping[4]
        self.tfrac = mapping[5]
        self.vint = mapping[6]
        self.sm = mapping[7]
        self.bestk = mapping[8]
        self.size = mapping[9]
        self.mbs = mapping[3] if mapping[3] else mapping[9]

        self.parameters.set(params)
        self.network_settings[0].set(dims)
        # self.network_settings[1].set("sigmoid")
        # self.network_settings[2].set("sigmoid")
        # self.network_settings[3].set("mse")
        self.network_settings[4].set(mapping[1])
        # self.network_settings[5].set("0.4-0.6")
        self.network_settings[6].set(mapping[0])
        self.network_settings[7].set(mapping[4])
        self.network_settings[8].set(mapping[5])
        self.network_settings[9].set(mapping[3] if mapping[3] else mapping[9])
        self.network_settings[11].set(mapping[6])
        # self.network_settings[10].set("50")
        # self.network_settings[11].set("50")
        # self.network_settings[12].set("50")
        # self.network_settings[13].set("50")
        # self.network_settings[14].set("50")
        # self.network_settings[15].set("50")
        print("VALUES NOT SHOWN IN THE GUI: ")
        print("showint: ", self.showint)  # 2
        print("softmax", self.sm)  # 7
        print("bestk", self.bestk)  # 8

    def run_network(self):
        self.status.set("Running GANN")
        self.ann.run(self.epochs, bestk=self.bestk)
        self.status.set("Finished running Gann")

    def getMapping(self, i):
        mappings = [
            [50, 0.1, 25, None, 0.1, 0.1, 25, True, 1, 10],
            [100, 0.1, 25, None, 0.1, 0.1, 25, True, 1, 1],
            [100, 0.1, 0, None, 0.1, 0.1, 25, True, 1, 10],
            [100, 0.1, 10, None, 0.1, 0.1, 25, True, 1, 20],
            [50, 0.03, 10, None, 0.1, 0.1, 10, True, False, 20],
            [50, 0.03, 10, None, 0.1, 0.1, 10, True, False, 20],
            [50, 0.03, 10, None, 0.1, 0.1, 10, True, False, 20],
            [50, 0.03, 10, None, 0.1, 0.1, 10, True, False, 20],
        ]
        return mappings[i]

    def getParams(self, i):
        params = ["10", "4", "500 15", "25 1000 0 8"]
        if(i < 4):
            return params[i]
        else:
            return ""

    def getDims(self, i):
        dims = [
            "10 8 2",
            "16 16",
            "15 15 16",
            "25 18 9",
            "784 100 10",
            "11 6",
            "9 7",
            "8 10",
        ]
        return dims[i]


app = Application()
app.mainloop()
