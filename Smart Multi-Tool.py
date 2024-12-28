import tkinter as tk
from tkinter import font
import requests
from tkinter import messagebox
from tkinter import ttk
import key
from tkinter import *
from tkinter import filedialog
import cv2
import pytesseract
from tkinter import filedialog, messagebox
import os
import speech_recognition as sr


#******************************************************************************************************
def show_weather_interface():
    def get_weather():
        city = entry.get()
        url = f'\\'
        response = requests.get(url)
        data = response.json()

        if data:
            table.delete(*table.get_children())  
            for item in data:
                latitude = item['lat']
                longitude = item['lon']
                country = item['country']
                city_name = item['name']

                weather_url = f'\\'
                weather_response = requests.get(weather_url)
                weather_data = weather_response.json()

                if 'weather' in weather_data and len(weather_data['weather']) > 0:
                    weather_type = weather_data['weather'][0]['main']
                else:
                    weather_type = "N/A"

                if 'main' in weather_data:
                    temperature = weather_data['main']['temp']
                    humidity = weather_data['main']['humidity']
                else:
                    temperature = "N/A"
                    humidity = "N/A"

                table.insert("", tk.END, values=(country, city_name, latitude, longitude, temperature, humidity, weather_type))
        else:
            table.delete(*table.get_children())  
            table.insert("", tk.END, values=("لا توجد بيانات", "", "", "", "", "", ""))

    def delete_data():
        table.delete(*table.get_children())  

    root = tk.Tk()
    root.geometry("800x400")
    root.title("Weather Interface")
    root.config(bg="lightblue")

    label = tk.Label(root, text="أهلاً بك في واجهة الطقس", bg="lightblue")
    label.pack(pady=30)

    label = tk.Label(root, text="اكتب اسم المدينة")
    label.pack()

    entry = tk.Entry(root,width=30)
    entry.pack()

    button_get_weather = tk.Button(root, text="الحصول على الطقس", bg="#0000FF",foreground="white", command=get_weather)
    button_get_weather.pack(pady=5)

    delete_button_frame = tk.Frame(root, bg="lightblue")
    delete_button_frame.pack()

    button_delete_data = tk.Button(delete_button_frame, text="حذف البيانات", foreground="white", bg="red", command=delete_data)
    button_delete_data.pack(side="right", pady=10)

    style = ttk.Style()
    

    style.configure("Treeview.Heading", background="#0000FF") 

    columns = ("الدولة", "المدينة", "خط العرض", "خط الطول", "درجة الحرارة", "الرطوبة", "نوع الطقس")
    table = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")

    for column in columns:
        table.heading(column, text=column, anchor="center")
        table.column(column, width=100, anchor="center")

    table.pack(expand=True, fill=tk.BOTH)

    root.mainloop()


#******************************************************************************************************
def show_translation_interface():
 url = "\\"
 querystring = {"api-version": "3.0", "to": "ar", "textType": "plain", "profanityAction": "NoAction"}

 def translate(subtitle):
    payload = "[\r\n    {\r\n        \"Text\": \""
    payload2 = "\"\r\n    }\r\n]"
    payload = payload + subtitle + payload2
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': key.key,
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    text = response.text
    start = text.find('"text":"')
    end = text.find('","to"')
    text = text[start + len('"text":"'):end]
    return text

 def translate_text(input_file_path, output_file_path):
    translated = []
    finished = False
    with open(input_file_path) as f:
        for line in f:
            if line[0:1].lower() in "abcdefghijklmnopqrstuvwxyz":
                line = translate(line.replace("\n", " "))
                translated.append(line)
                print(line)
            else:
                translated.append(line.replace("\n", " "))
        finished = True
    if finished:
        with open(output_file_path, "w", encoding="utf-8") as f:
            for line in translated:
                line.encode("utf-8")
                f.write(line)
                f.write("\n")

 def translate_image(input_file_path, output_file_path):
    image = Image.open(input_file_path)
    text = pytesseract.image_to_string(image, lang="eng")
    translated_text = translate(text)
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(translated_text)

 def translate_file(input_file_path, output_file_path, file_type):
    if file_type == "Text":
        translate_text(input_file_path, output_file_path)
    elif file_type == "Image":
        translate_image(input_file_path, output_file_path)

 def create_gui():
    window = tk.Tk()
    window.title("Subtitle Translator")
    window.geometry("400x300")
    window.configure(bg="lightblue")

    button_bg_color = "blue"
    button_fg_color = "white"
    button_width = 15
    button_height = 2

    def translate_button_click():
        file_type = file_type_var.get()

        filetypes = {
            "Text": [("Text Files", "*.txt")],
            "Image": [("Image Files", "*.png;*.jpg")]
        }

        input_file_path = filedialog.askopenfilename(
            title="اختر الملف المراد ترجمته",
            filetypes=filetypes[file_type])

        output_file_path = filedialog.asksaveasfilename(
            title="حدد مسار حفظ الملف المترجم",
            defaultextension=".txt",
            filetypes=filetypes[file_type])

        translate_file(input_file_path, output_file_path, file_type)

        messagebox.showinfo("تمت الترجمة", "تمت عملية الترجمة بنجاح!")

    file_type_var = tk.StringVar(window)
    file_type_var.set("نــوع الملف")

    file_type_label = tk.Label(window, text=" قم بأختيــار نــوع الملف المراد ترجمته", bg="lightblue", fg="black")
    file_type_label.pack(pady=25)

    file_type_option_menu = tk.OptionMenu(window, file_type_var, "Text", "Image")
    file_type_option_menu.configure(bg="white", width=button_width, height=button_height)
    file_type_option_menu.pack()

    translate_button = tk.Button( window,
     text="تــرجمة",
     bg='lightblue',
     fg='white',
     width=button_width,
     height=button_height,
     font=("Arial", 12),
     command=translate_button_click)
    
    translate_button.pack(pady=30)
    translate_button.configure(width=20, height=1)
    translate_button.configure(bg="#8B1A1A")

    window.mainloop()


 create_gui()


#******************************************************************************************************
def video_to_srt(input_file_path):
    # Load the video file
    video = cv2.VideoCapture(input_file_path)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # Initialize subtitle text
    subtitle_text = ""

    # Loop through frames and extract text
    for frame_number in range(frame_count):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video.read()

        # Convert frame to grayscale and apply OCR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang='eng')

        # Append text to subtitle
        subtitle_text += f"{frame_number+1}\n00:00:{frame_number//fps:02},000 --> 00:00:{(frame_number+1)//fps:02},000\n{text}\n\n"

    # Create the output SRT file path
    directory_path = os.path.dirname(input_file_path)
    base_filename = os.path.basename(input_file_path)
    base_filename = os.path.splitext(base_filename)[0]  # Remove the extension from the filename
    output_srt_path = os.path.join(directory_path, base_filename + ".srt")

    # Save the subtitles to the SRT file
    with open(output_srt_path, 'w') as f:
        f.write(subtitle_text)

    # Show success message
    messagebox.showinfo("تمت العملية", "تم استخراج الترجمات بنجاح.")

def video_convert_button_click():
    input_file_path = filedialog.askopenfilename(
        title="اختر ملف الفيديو",
        filetypes=[("ملفات الفيديو", "*.mp4")])

    video_to_srt(input_file_path)


#******************************************************************************************************
def sh_vid_extra_interface():
    def translate_subtitle():
        url = "\\"

        querystring = {
           "api-version": "3.0",
           "to": "ar",
           "textType": "plain",
           "profanityAction": "NoAction"
        }

        def translate(subtitle):
            payload = "[\r\n    {\r\n        \"Text\": \""
            payload2 = "\"\r\n    }\r\n]"
            payload = payload + subtitle + payload2
            headers = {
               'content-type': "application/json",
               'x-rapidapi-key': key.key,
               'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
            }
            response = requests.request(
                "POST", url, data=payload.encode('utf-8-sig'), headers=headers, params=querystring)

            text = response.text
            start = text.find('"text":"')
            end = text.find('","to"')
            text = text[start + len('"text":"'):end]
            return text

        subtitle_file_path = filedialog.askopenfilename(title="حدد ملف الترجمة", filetypes=[("ملفات الترجمة", "*.srt")])
        if subtitle_file_path:
            translated_file_path = filedialog.asksaveasfilename(title="حفظ الترجمة المترجمة", defaultextension=".srt",
                                                                filetypes=[("Subtitle Files", "*.srt")])
            if translated_file_path:
                translated = []
                finished = False
                try:
                    with open(subtitle_file_path, "r") as f:
                        for line in f:
                            if line[0].isalpha():
                                line = translate(line.replace("\n", " "))
                                translated.append(line)
                                print(line)
                            else:
                                translated.append(line.replace("\n", " "))
                        finished = True
                except FileNotFoundError:
                    messagebox.showerror("Error", "File not found. Please check the file path.")
                except Exception as e:
                    messagebox.showerror("Error", "An error occurred: " + str(e))

                if finished:
                    try:
                        with open(translated_file_path, "w", encoding="utf-8") as f:
                            for line in translated:
                                f.write(line)
                                f.write("\n")
                        messagebox.showinfo("نجاح", "تمت ترجمة الترجمة بنجاح.")
                    except Exception as e:
                        messagebox.showerror("خطــأ", "حدث خطأ أثناء حفظ الترجمة المترجمة: " + str(e))
            else:
               messagebox.showwarning("تحذير", "لم يتم تحديد ملف لحفظ الترجمة المترجمة.")
        else:
             messagebox.showwarning("تحذير", "لم يتم تحديد ملف للترجمة.")

    # Create the GUI window
    window = tk.Tk()
    window.title("مترجم الترجمة")

    # Set the window dimensions
    window.geometry("400x250")

    # Set the background color
    window.configure(bg="lightblue")

    # Create a label for subtitle file selection
    subtitle_label = Label(window, text="قم بأختيار الملف المراد ترجمته", bg="lightblue", fg="#8B1A1A", font=("Arial", 16))
    subtitle_label.pack(pady=50)

    # Create a button to select the subtitle file
    subtitle_button = Button(window, text="تحـــديد", command=translate_subtitle, bg="#8B1A1A",foreground="white", relief="raised", font=("Arial", 14), width=12)
    subtitle_button.pack(pady=5)

    # Run the GUI
    window.mainloop()


#******************************************************************************************************

def show_main_interface():
    global main_window
    main_window = tk.Tk()
    main_window.title("****أداة_ذكية_متعددة_الاستخداما****")
    main_window.geometry("700x500")
    main_window.configure(bg="#f0f8ff") 

   
    title_font = font.Font(family="Arial", size=18, weight="bold")
    button_font = font.Font(family="Arial", size=14)

    label = tk.Label(main_window, text="أختــر نــوع التطبيق", bg="#f0f8ff", fg="#2e3b4e", font=title_font)
    label.pack(pady=30)


    button_frame = tk.Frame(main_window, bg="#f0f8ff")
    button_frame.pack(pady=20)

    weather_button = tk.Button(button_frame, text="الاستعلام عن الطقس", fg="white", bg="#8B1A1A", font=button_font, 
                               command=show_weather_interface, width=30, relief="flat", height=2)
    weather_button.grid(row=0, column=0, padx=10, pady=10)

    translation_button = tk.Button(button_frame, text="الترجمة", fg="white", bg="#8B1A1A", font=button_font, 
                                   command=show_translation_interface, width=30, relief="flat", height=2)
    translation_button.grid(row=1, column=0, padx=10, pady=10)

    video_conversion_button = tk.Button(button_frame, text="تحويل فيديو إلى نص ترجمة", fg="white", bg="#8B1A1A", font=button_font, 
                                        command=video_convert_button_click, width=30, relief="flat", height=2)
    video_conversion_button.grid(row=2, column=0, padx=10, pady=10)

    video_extraction_button = tk.Button(button_frame, text="ترجمة النص المستخرج من الفيديو", fg="white", bg="#8B1A1A", font=button_font, 
                                        command=sh_vid_extra_interface, width=30, relief="flat", height=2)
    video_extraction_button.grid(row=3, column=0, padx=10, pady=10)

    def on_enter(event, button):
        button.config(bg="#9e2a2b")

    def on_leave(event, button):
        button.config(bg="#8B1A1A")

    for button in [weather_button, translation_button, video_conversion_button, video_extraction_button]:
        button.bind("<Enter>", lambda event, button=button: on_enter(event, button))
        button.bind("<Leave>", lambda event, button=button: on_leave(event, button))

    main_window.mainloop()
# Show the main interface
show_main_interface()

#******************************************************************************************************