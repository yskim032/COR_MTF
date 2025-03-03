import os


from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import fileinput
import chardet

#C:\Users\kod03\OneDrive\바탕 화면\파이썬강의\gui_basic> pyinstaller -F -w .\MSC_D(tab 누르기)

root = Tk()
root.title("DTX Converter")
root.geometry("640x480")
root.resizable(False,False)


def select_file():

    list_file=[]
    files = filedialog.askopenfilenames(initialdir="/",\
                 title = "Select DTX files.",\
                    filetypes = (("*.GVA","*GVA"),("*.txt","*txt"),("*.xls","*xls"),("*.csv","*csv")))
    

    if files == '':
        messagebox.showwarning("Warning", "Select file.") 
    else:
        for i in files:
            listbox.insert(0,i)
    
    lbl = Label(root, padx=10, pady=10, background = 'spring green',text=listbox.size(), fg='black', font=('Arial Bold',20,'bold'))
    lbl.place(x=550, y=0)
    

def print_items():
    a = listbox.get(0, listbox.size())
    total_files = len(a)  # 총 파일 개수

    for i in a:
        with fileinput.input(i, inplace=True) as f:
            for line in f:
                if f.isfirstline():
                    print('HDR              55MFT                               096N', end='\n')
                else:
                    print(line, end='')
    
    # 결과 메시지 업데이트
    result_label.config(text=f"Successfully converted {total_files} files!")

btn1=Button(root, padx=20, pady = 20, bg="yellow", text="Select Files",command=select_file)
btn1.pack()

listbox=Listbox(root, selectmode="extended", width=80, height=20)
listbox.pack()

# 분홍색 변환 버튼 추가
btn_convert = Button(root, padx=20, pady=10, bg="pink", text="Convert Files", command=print_items)
btn_convert.pack()

# 결과 표시 라벨 추가
result_label = Label(root, text="", pady=10, font=('Arial', 10))
result_label.pack()

root.mainloop()
