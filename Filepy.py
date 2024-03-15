import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def process_txt(file_path):
    '''
    对txt文本进行处理
    '''
    with open(file_path, 'x') as file:
            content = file.read()
            print(content)
            file.close()

def address_sort(df, inOrOut):
    '''
    按地址进行排序并恢复数据
    '''
    # 只保留数字
    df['Logical Address'] = df['Logical Address'].str.extract('(\\d+\\.?\\d*)').astype('float')

    df = df.sort_values(by='Logical Address')
    df['Logical Address'] = df['Logical Address'].astype(str)
    if inOrOut in ('iMap', 'oMap'):
        address_bool = '%M'
        address_int = '%MW'
        address_dword = '%MD'
    elif inOrOut == 'in':
        address_bool = '%I'
        address_int = '%IW'
        address_dword = '%ID'
    else:
        address_bool = '%Q'
        address_int = '%QW'
        address_dword = '%QD'
    for i in df['Data Type'].index:
        if df['Data Type'][i] == "Bool":
            df.loc[i, "Logical Address"] = address_bool + df.loc[i, "Logical Address"]
        elif df['Data Type'][i] in ("Int","Word"):
            df.loc[i, "Logical Address"] = df.loc[i, "Logical Address"] .replace('.0', '')
            df.loc[i, "Logical Address"] = address_int + df.loc[i, "Logical Address"]
        else:  # df['Data Type'][i] == "Dword":
            df.loc[i, "Logical Address"] = df.loc[i, "Logical Address"] .replace('.0', '')
            df.loc[i, "Logical Address"] = address_dword + df.loc[i, "Logical Address"]
    return df

def preprocess(df, ioMap):
    # 分别提取输入输出变量并修改路径
    if ioMap == 'iMap':
        extractio = 'I'
        path = 'I_Map'
    else:
        extractio = 'Q'
        path = 'Q_Map'
    df_ioMap = df[df['Logical Address'].str.contains(extractio)]
    df_ioMap.loc[df_ioMap.index,'Path'] = df_ioMap['Path'].str.replace('IO_Table', path)
    return df_ioMap

def process_excel(file_path):
    # 设置最大行、最大列为无限
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_column', None)

    # 读取excel文件,5,6
    # df = pd.read_excel('PLCTags (2).xlsx',engine= 'openpyxl', usecols= "A:E", converters={'A':lambda x: "\'"+ x})
    df_io = pd.read_excel(file_path, engine= 'openpyxl', usecols= [0,1,2,3,4], converters={0:lambda x:  x + "_m"})

    # 对=进行处理 
    df_io['Name'] = df_io['Name'].str.replace('=', '')
    df_io.to_excel(r'C:\Users\Administrator\Desktop\test.xlsx', index = False, sheet_name='PLC Tags')

    # 提取输入变量并进行映射处理
    # df_iMap = df_io[df_io['Logical Address'].str.contains('I')]
    # # df1.loc[df1.index,'Logical Address'] = df1['Logical Address'].str.replace('I', 'M')
    # df_iMap.loc[df_iMap.index,'Path'] = df_iMap['Path'].str.replace('IO_Table', 'I_Map')
    df_iMap = preprocess(df_io, 'iMap')
    df_iMap = address_sort(df_iMap, 'iMap')

    df_iMap_tags = df_iMap['Name']
    add_newline = lambda x:'="'+ x + '"\n'
    # print(df_iMap_tags)
    with open(r'C:\Users\Administrator\Desktop\testIM.txt', mode='w') as IMtxt:
        IMtxt.writelines(add_newline(df_iMap_tags))
        IMtxt.close()
        
    # 输出到excel中
    df_iMap.to_excel(r'C:\Users\Administrator\Desktop\testIM.xlsx', index = False, sheet_name='PLC Tags')   # 前缀r防止转义


    df_oMap = preprocess(df_io, 'oMap')
    df_oMap = address_sort(df_oMap, 'oMap')
    # 输出到excel中
    df_oMap.to_excel(r'C:\Users\Administrator\Desktop\testQM.xlsx', index = False, sheet_name='PLC Tags')

   


def process_sdf(file_path):
    '''
    SDF文件处理 rdkit库
    # from rdkit import Chem
    # from rdkit.Chem import AllChem
    # from rdkit.Chem import Draw       
    '''

class App(tk.Frame):
    def __init__(self, master = None ):
        super().__init__(master)
        self.pack
        # save_button = tk.Button(self, text='Save File', command=self.save_file)
        # save_button.pack()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt')],
            initialdir='/',
            title='Save file'
        )

        if file_path:
            print(f'File saved to:{file_path}')
            
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=file_types,
            title='Open file'
        )

        if file_path:
            print(f"选择的文件：{file_path}")
            file_name = os.path.basename(file_path)
            print(file_name)
            file_extension = os.path.splitext(file_name)[1]
            print(file_extension)
            if file_extension == '.txt':
                process_txt(file_path)
            elif file_extension == '.xlsx':
                process_excel(file_path)
        else:
            print("未选择文件")

myapp = App()

myapp.master.title("保存文件")
myapp.master.maxsize(1000,200)

save_button = tk.Button(myapp.master,text='save',command=myapp.save_file)
open_button = tk.Button(myapp.master,text='Open',command=myapp.open_file)
open_button.pack()
save_button.pack()
# # 初始化Tkinter.grid(column=0,row=0)
# root = tk.Tk()
# # root.withdraw()  # 隐藏主窗口
# button = tk.Button(root)
# root.title("保存文件")
# print(root.size())


file_types = (
    ("All supported files","*.txt;*.csv;*.xlsx"),
    ("Excel files","*.xlsx"),
    ("Text files", "*.txt"),
    ("CSV files", "*.csv")
)

'''
file_path = filedialog.askopenfilename(filetypes=file_types, title='Open File')

if file_path:
    print(f"选择的文件：{file_path}")
    file_name = os.path.basename(file_path)
    print(file_name)
    file_extension = os.path.splitext(file_name)[1]
    print(file_extension)
    if file_extension == '.txt':
        process_txt(file_path)
    elif file_extension == '.xlsx':
        process_excel(file_path)
else:
    print("未选择文件")
'''

# root.mainloop()  # 进入消息循环
myapp.mainloop()