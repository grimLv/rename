#coding=GBK
import os
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tm
import re

def getDirector():
    system_separate=os.sep
    file_dir=path_input_frame.get()
    if file_dir=='':
        tm.showerror("Error","文件选择路径不能为空！")
        return
    try:
        for out_root,dirs,files in os.walk(file_dir):
            if len(files) == 0:
                for dir in dirs:
                    for set in os.walk(out_root+system_separate+dir):
                        # 子文件夹没有文件直接跳过
                        if len(set[2]) == 0:
                            print(out_root+system_separate+dir+"-----文件夹为空！")
                            continue
                        root=set[0]
                        print(root)
                        # 获取子文件夹的文件数组
                        sub_files=set[2]
                        # 循环遍历子文件夹的文件数组
                        for file_index in range(len(sub_files)):
                            if sub_files[file_index].count('-')>1 or sub_files[file_index].count('_') > 1:
                                tm.showerror('Error','该文件命名格式有误：'+root+system_separate+sub_files[file_index])
                                return
                            # 完整的旧文件路径
                            old_name_complete=root+system_separate+sub_files[file_index]
                            # 旧文件名
                            old_name=sub_files[file_index].split(".")[0]
                            # 旧文件名后缀格式
                            old_name_suffix=sub_files[file_index].split(".")[1]
                            # 用-或_分割文件名
                            after_split=re.split('-|_',old_name)
                            pattern = re.compile(r'[A-Za-z]\d{1,4}')
                            # 如果符合姓名-工号的格式则进方法体
                            if pattern.match(after_split[0]) == None:
                                # 如果文件名包含-符号，则跳过
                                if old_name.count('-')==1:
                                    continue
                                elif old_name.count('_') ==1:
                                # 如果文件名包含_符号，则替换成-
                                    modify_file_name=root+system_separate+after_split[0]+'-'+after_split[1]+'.'+old_name_suffix
                                    os.rename(old_name_complete,modify_file_name)
                                    continue
                            search_result = pattern.search(after_split[0]).group()
                            if len(search_result) != 0:
                                temp = after_split[1]
                                after_split[1] = after_split[0]
                                after_split[0] = temp
                                concat_file_name=after_split[0]+"-"+after_split[1]
                                print(concat_file_name)
                                new_name=concat_file_name+"."+old_name_suffix
                                new_name_complete=root+system_separate +new_name
                                print(old_name_complete)
                                print(new_name_complete)
                                os.rename(old_name_complete,new_name_complete)
            else:
                print("外层文件夹没有文件"+out_root)
    except:
        tm.showerror("Error","执行出错！")
    else:
        tm.showinfo("Info","执行完成")

def selectFile():
    global file_dir
    file_dir=tkfd.askdirectory()
    path_input_frame.insert(0,file_dir)

def execute():
    getDirector()
    pass

def showWindow():
    root_window = tk.Tk();
    root_window.title("        文件批量重命名         ")
    root_window.geometry("400x200")

    path_label = tk.Label(root_window,text="文件路径：")
    path_label.grid(row=0,padx=20,pady=30)
    global path_input_frame
    path_input_frame = tk.Entry(root_window)
    path_input_frame.grid(row=0,column=1,pady=30)
    path_select_button = tk.Button(root_window,text="浏览",width=5,height=1,command=selectFile)
    path_select_button.grid(row=0,column=2,padx=30)
    path_select_button = tk.Button(root_window,text="开始",width=10,height=2,command=execute)
    path_select_button.grid(row=1,column=1,padx=40,pady=20)

    root_window.mainloop()

if __name__=="__main__":
    showWindow()
    getDirector()