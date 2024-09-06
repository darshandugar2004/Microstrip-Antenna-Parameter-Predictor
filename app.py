from tkinter import messagebox
from tkinter import *
import math as m
from PIL import Image, ImageTk
from model import *
from tensorflow import keras
import numpy

def get_float_value():
    try:
        height_var = float(height_entry.get())
        permitivity_var = float(permitivity_entry.get())
        freq_var = float(freq_entry.get())
        calculate(height_var, permitivity_var, freq_var)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid float value.")
        
def calclate_params(f,h,e) :
    loss = 25
    load_model_y = keras.models.load_model('best_model_y.h5')
    load_model_x = keras.models.load_model('best_model_x.h5')
    data = []
    input_data = numpy.array([h,f,e,loss])
    data[0] = load_model_x.predict(input_data)
    data[1] = load_model_y.predict(input_data)
    return data
    
def calculate(h, e, f):
    # calculate Heigth and width
    f0 = f*pow(10,9)
    W = c/(2*f0 * m.sqrt( (e+1)/2) )
    Eeff = (e+1)/2 + ( (e-1)/2 )*pow( (1+12*h/W) , -0.5)
    Leff = c/( 2*f0*m.sqrt(Eeff) )
    DL = 0.412*h*(Eeff + 0.3)*(W/h + 0.264)/( (Eeff - 0.258)*(W/h + 0.8) )
    L = Leff - 2*DL
    W = round(W,3)
    L = round(L,3)
    
    # width of feed line
    exponent = z0 * m.sqrt(e+1.41) / 87
    imp_width = (7.48*h)/pow(e,exponent) - 1.25*t
    
    # predicted data
    data = calculate_param(e,f,L)
    
    # print values
    L_value = Label(text=round(L,3) , font=('Arial',TEXT))
    L_value.place(x=X_ENTRY , y=350)
    
    W_value = Label(text=round(W,3) , font=('Arial',TEXT))
    W_value.place(x=X_ENTRY , y=400)
    
    feed_value = Label(text=round(data[0],3) , font=('Arial',TEXT))
    feed_value.place(x=X_ENTRY + 30 , y=450)
    
    gap_value = Label(text=round(data[1],3) , font=('Arial',TEXT))
    gap_value.place(x=X_ENTRY -15, y=500)
    
    imp_value = Label(text=round(imp_width,3) , font=('Arial',TEXT))
    imp_value.place(x=X_ENTRY+75 , y=550)
    
    # on diagram
    L_value = Label(text=round(L,3) , font=('Arial',DIAGRAM))
    L_value.place(x=191+400, y=166+100)
    
    W_value = Label(text=round(W,3) , font=('Arial',DIAGRAM))
    W_value.place(x=367+400 , y=106+100)
    
    feed_value = Label(text=round(data[0],3) , font=('Arial',DIAGRAM))
    feed_value.place(x=125+400 , y=274+100)
    
    gap_value = Label(text=round(data[1],3) , font=('Arial',DIAGRAM))
    gap_value.place(x=289+400 , y=279+100)
    
    imp_value = Label(text=round(imp_width,3) , font=('Arial',DIAGRAM))
    imp_value.place(x=182+400 , y=371+100)
    
    height_value = Label(text=round(h,3) , font=('Arial',DIAGRAM))
    height_value.place(x=410+400 , y=319+100)
    
def save_antenna() :
    to_save = ''''''
    # write these values in txt file
    
def model_details():
    model_details_window = Toplevel(window)
    model_details_window.title("Model Details")
    model_details_window.geometry("900x600")
    
    model_label = Label(model_details_window, text="Model Info.", font=("Arial", 22))
    model_label.pack(pady=10)

    model_label = Label(model_details_window, text=MODEL_DATA ,wraplength=800, font=("Arial", 12),justify="left" )
    model_label.pack(pady=10)
    
    model_label = Label(model_details_window, text=CITATION ,wraplength=800, font=("Arial", 12),justify="left" )
    model_label.pack(pady=10)

    close_button = Button(model_details_window, text="Close", command=model_details_window.destroy , font=("Arial", 12))
    close_button.place(x=440,y=550)
    
def developers_details():
    model_details_window = Toplevel(window)
    model_details_window.title("Developers Details")
    model_details_window.geometry("900x600")

    model_label = Label(model_details_window, text="Developers Info.", font=("Arial", 22))
    model_label.pack(pady=10)

    darshan_photo = Image.open(model_details_window,"darshan.jpg")
    darshan_photo = darshan_photo.resize((200,300))
    photo = ImageTk.PhotoImage(model_details_window,darshan_photo)
    label = Label(model_details_window,image=photo)
    label.place(x=50,y=200)
    
    close_button = Button(model_details_window, text="Close", command=model_details_window.destroy)
    close_button.pack(pady=10)
    
#Creating a new window and configurations
window = Tk()
window.title("Software")    
window.minsize(width=1000, height=700)
window.resizable(False,False)
window.configure(bg="#EEEDEB")

# heading
Title = Label(text="Microstrip Antenna Params Predictor" , font=("Arial", 22))
Title.pack()

# Lable -> inputs
Title = Label(text="Input Parametrs" , font=("Arial", SUBHEADING))
Title.place(x=120, y=50)

# inputs
height_lable = Label(text="Height (mm) : " , font=('Arial',TEXT))
height_lable.place(x=X_LABLE , y=100)
height_entry = Entry(width=WIDTH_ENTRY)
height_entry.place(x=X_ENTRY , y=100)

permitivity_lable = Label(text="Substrate Permitivity : " , font=('Arial',TEXT))
permitivity_lable.place(x=X_LABLE , y=150)
permitivity_entry = Entry( width=WIDTH_ENTRY)
permitivity_entry.place(x=X_ENTRY , y=150)

freq_lable = Label(text="Frequency (Ghz) : " , font=('Arial',TEXT))
freq_lable.place(x=X_LABLE , y=200)
freq_entry = Entry(width=WIDTH_ENTRY)
freq_entry.place(x=X_ENTRY , y=200)

# Calculate Buttons
button = Button(text="Calculate", command=get_float_value, bg='#939185' , font=('Arial',BUTTON), width=10 , height=1)
button.place(x=150 , y=250)

# Lable -> Outputs
Title = Label(text="Predicted Parametrs" , font=("Arial", SUBHEADING))
Title.place(x=100, y=300)

# outputs
L_lable = Label(text="Patch Length L (mm) : " , font=('Arial',TEXT))
L_lable.place(x=X_LABLE , y=350)

W_lable = Label(text="Patch Width W (mm) : " , font=('Arial',TEXT))
W_lable.place(x=X_LABLE , y=400)

feed_lable = Label(text="Inset Feed Length l (mm) :" , font=('Arial',TEXT))
feed_lable.place(x=X_LABLE , y=450)

gap_lable = Label(text="Notch Gap (mm) s : " , font=('Arial',TEXT))
gap_lable.place(x=X_LABLE , y=500)

imp_lable = Label(text=u"Impedence Line Width W\u2080 (mm) : " , font=('Arial',TEXT))
imp_lable.place(x=X_LABLE , y=550)

# SAVE button
save_button = Button(text="Save\n Design", command=save_antenna, width=20 , height=3 ,bg='#939185' , font=('Arial',BUTTON))
save_button.place(x=100 , y=600)

# Model button
model_button = Button(text="Model", command=model_details, width=20 , height=3 ,bg='#939185', font=('Arial',BUTTON))
model_button.place(x=450 , y=600)

# Developers button
developers_button = Button(text="Developers", command=developers_details, width=20 , height=3 ,bg='#939185', font=('Arial',BUTTON))
developers_button.place(x=710 , y=600)

# diagram & Lable
Title = Label(text="Diagram" , font=("Arial", SUBHEADING))
Title.place(x=620, y=50)

image = Image.open("diagram.png")
image = image.resize((550,465))
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.place(x=400,y=100)

# def display_coordinates(event):
#     # Display the coordinates
#     print(f"Mouse clicked at coordinates: ({event.x}, {event.y})")
    
# # Bind the left mouse button click to the display_coordinates function
# window.bind("<Button-1>", display_coordinates)

def close_window():
    window.destroy()  # Close the window
# window.after(5000, close_window)


window.mainloop()