import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def process_txt(file_path, text):
    '''
    对txt文本进行处理
    '''
    with open(file_path, mode='w') as IMtxt:
        IMtxt.writelines(text)
        IMtxt.close()
        

def address_sort(df, inOrOut):
    '''
    按地址进行排序并恢复数据
    '''
    # 只保留数字
    df['Logical Address'] = df['Logical Address'].str.extract('(\\d+\\.?\\d*)').astype('float')
    df_tags = []

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
            df_tags.append(df.loc[i, 'Name'])
            df.loc[i, "Logical Address"] = address_bool + df.loc[i, "Logical Address"]
        elif df['Data Type'][i] in ("Int","Word"):
            df.loc[i, "Logical Address"] = df.loc[i, "Logical Address"] .replace('.0', '')
            df.loc[i, "Logical Address"] = address_int + df.loc[i, "Logical Address"]
        else:  
            df.loc[i, "Logical Address"] = df.loc[i, "Logical Address"] .replace('.0', '')
            df.loc[i, "Logical Address"] = address_dword + df.loc[i, "Logical Address"]
    return df,df_tags

def extractor(df, io):
    if io == 'i':
        extractio = 'I'
    else:
        extractio = 'Q'
    df_io = df[df['Logical Address'].str.contains(extractio)]
    return df_io

def generate_map(df, ioMap):
    df_ioMap =df.copy()   # 创建原始数据的副本，对副本进行操作，不改变原始数据
    # add_m = lambda x: x + '_m'
    df_ioMap['Name'] = df_ioMap['Name'] + '_m'
    if ioMap == 'iMap':
        path = 'I_Map'
    else:
        path = 'Q_Map'
    df_ioMap.loc[df_ioMap.index,'Path'] = df_ioMap['Path'].str.replace('IO_Table', path)
    return df_ioMap

def extractorTags(tags, flag):
    df_tags = tags
    if flag == 0:
        add_newline = lambda x:'="'+ x + '"\n'
        df_tags = add_newline(df_tags)
    else:
        addA_newline = lambda x:'A"'+ x + '"\n'
        df_tags = addA_newline(df_tags)
    
    return df_tags

def process_excel(df):
    
    df_io = df
    # 对=进行处理 
    df_io['Name'] = df_io['Name'].str.replace('=', '')
    
    (df_i, df_itags) = address_sort(extractor(df_io, 'i'), 'in')
    print(df_itags)  # 提取出的标签存储在列表里
    # print(df_i['Name'])
    # df_itags = df_i['Name']
    # df_itags = extractorTags(df_itags, 1)
    
    df_i.to_excel(r'C:\Users\Administrator\Desktop\testI.xlsx', index = False, sheet_name='PLC Tags')
    (df_o, df_otags) = address_sort(extractor(df_io, 'o'), 'out')
    df_o.to_excel(r'C:\Users\Administrator\Desktop\testO.xlsx', index = False, sheet_name='PLC Tags')

    df_iMap = generate_map(df_i, 'iMap')   #直接传入之后会改变参数的值
    
    # 输出到excel中
    df_iMap.to_excel(r'C:\Users\Administrator\Desktop\testIM1.xlsx', index = False, sheet_name='PLC Tags')   # 前缀r防止转义

    df_oMap = generate_map(df_o, 'oMap')
    # 输出到excel中
    df_oMap.to_excel(r'C:\Users\Administrator\Desktop\testQM1.xlsx', index = False, sheet_name='PLC Tags')

    
    # 获取标签
    df_itags = df_i['Name']
    print(df_itags)
    print(df_itags.type)
    df_itags = extractorTags(df_itags, 1)

    df_iMaptags = extractorTags(df_iMap['Name'], 0)

    df_oMaptags = extractorTags(df_oMap['Name'], 1)

    df_otags = extractorTags(df_o['Name'], 0)

    return df_itags,df_otags,df_iMaptags,df_oMaptags
   

class App(tk.Frame):

    tag_tup = ()
    def __init__(self, master = None ):
        super().__init__(master)
        self.pack


    def save_file(self):
        for i in self.tag_tup:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.txt',
                filetypes=[('Text files', '*.txt')],
                initialdir='/',
                title='Save file'
            )

            if file_path:
                print(f'File saved to:{file_path}')
                process_txt(file_path, i)
            
            
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=file_types,
            title='Open file'
        )

        if file_path:
            print(f"选择的文件：{file_path}")
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            df_io = pd.read_excel(file_path, 
                                  engine= 'openpyxl', 
                                  usecols= [0,1,2,3,4]
                    )
            if file_extension == '.txt':
                process_txt(file_path)
            elif file_extension == '.xlsx':
                self.tag_tup = self.tag_tup + process_excel(df_io)
                print(self.tag_tup[1])
        else:
            print("未选择文件")


file_types = (
    ("All supported files","*.txt;*.csv;*.xlsx"),
    ("Excel files","*.xlsx"),
    ("Text files", "*.txt"),
    ("CSV files", "*.csv")
)

myapp = App()

myapp.master.title("保存文件")
myapp.master.maxsize(1000,200)
print(os.getcwd())
# os.mkdir('files')  # 创建空文件夹用来保存处理后的文件
save_button = tk.Button(myapp.master,text='save',command=myapp.save_file)
open_button = tk.Button(myapp.master,text='Open',command=myapp.open_file)
open_button.pack()
save_button.pack()


myapp.mainloop()