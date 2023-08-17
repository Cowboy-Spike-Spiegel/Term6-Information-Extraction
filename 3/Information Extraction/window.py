import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox


class UIApp:
    def __init__(self, folder_path, module):
        # 已经初始化完成的module
        self.extraction_module = module

        self.window = tk.Tk()
        self.window.title("信息提取")

        # 设定文件参数
        self.language = ''
        self.name = ''
        self.English_list = os.listdir(folder_path+'\\English')
        self.Chinese_list = os.listdir(folder_path+'\\Chinese')

        # 计算全屏的宽度和高度
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.width = int(screen_width * 0.8)
        self.height = int(screen_height * 0.8)

        # 设置窗口大小和位置
        self.window.geometry(f"{self.width}x{self.height}+{int((screen_width - self.width) / 2)}+{int((screen_height - self.height) / 2)}")

        # 运行主循环
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # 设置窗口关闭事件的处理函数

    def create_widgets(self):
        # 书籍-----------------------------------------------------------------------------------------
        # 创建英文书目下拉选项框
        English_label = ttk.Label(self.window, text="英文书目:")
        English_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        options = []
        for file_name in self.English_list:
            options.append(file_name[:-4])
        self.English_combobox = ttk.Combobox(self.window, values=options)
        self.English_combobox.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.English_combobox.bind("<<ComboboxSelected>>", self.english_combobox_selected)

        # 创建中文书目下拉选项框
        Chinese_label = ttk.Label(self.window, text="中文书目:")
        Chinese_label.grid(row=0, column=4, padx=10, pady=10, sticky=tk.NSEW)
        options = []
        for file_name in self.Chinese_list:
            options.append(file_name[:-4])
        self.Chinese_combobox = ttk.Combobox(self.window, values=options)
        self.Chinese_combobox.grid(row=0, column=5, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
        self.Chinese_combobox.bind("<<ComboboxSelected>>", self.chinese_combobox_selected)

        analyze_button = ttk.Button(self.window, text="解析", command=self.analyze_button_click)
        analyze_button.grid(row=0, column=8, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

        # 选项---------------------------------------------------------------------------------------
        # 创建英文tag下拉选项框
        English_tag_label = ttk.Label(self.window, text="英文tag:")
        English_tag_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.en_tags = self.extraction_module.get_tag("English")
        options = ['']
        for key, value in self.en_tags.items():
            options.append(str(key) + '-' + str(value))
        self.English_tag_combobox = ttk.Combobox(self.window, values=options)
        self.English_tag_combobox.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
        self.English_tag_combobox.bind("<<ComboboxSelected>>", self.english_tag_combobox_selected)

        # 创建中文tag下拉选项框
        Chinese_tag_label = ttk.Label(self.window, text="中文tag:")
        Chinese_tag_label.grid(row=1, column=4, padx=10, pady=10, sticky=tk.NSEW)
        self.ch_tags = self.extraction_module.get_tag("Chinese")
        options = ['']
        for key, value in self.ch_tags.items():
            options.append(str(key) + '-' + str(value))
        self.Chinese_tag_combobox = ttk.Combobox(self.window, values=options)
        self.Chinese_tag_combobox.grid(row=1, column=5, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
        self.Chinese_tag_combobox.bind("<<ComboboxSelected>>", self.chinese_tag_combobox_selected)

        # 正则表达式及是否是筛选命名实体空间------------------------------------------------------------------------
        # 正则表达式下拉框
        re_label = ttk.Label(self.window, text="常用正则表达式:")
        re_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.re_formats = self.extraction_module.get_re()
        options = ['']
        for key, value in self.re_formats.items():
            options.append(str(key) + '-' + str(value))
        self.re_combobox = ttk.Combobox(self.window, values=options)
        self.re_combobox.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
        #self.re_combobox.bind("<<ComboboxSelected>>", self.re_selected)

        # 选择框
        self.in_named_entities = False
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.window, text="是否在命名实体空间中提取", variable=self.checkbox_var, command=self.checkbox_click)
        self.checkbox.grid(row=2, column=5, padx=10, pady=10, sticky=tk.NSEW)

        # 输入和按钮------------------------------------------------------------------------------------
        # 创建输入框
        input_label = ttk.Label(self.window, text="输入信息:")
        input_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.input_text = tk.StringVar()
        self.input_entry = ttk.Entry(self.window, textvariable=self.input_text)
        self.input_entry.grid(row=3, column=1, columnspan=5, padx=10, pady=10, sticky=tk.NSEW)

        # 检索和提取按钮
        retrieval_button = ttk.Button(self.window, text="检索", command=self.retrieval_button_click)
        retrieval_button.grid(row=3, column=6, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        extract_button = ttk.Button(self.window, text="提取", command=self.extract_button_click)
        extract_button.grid(row=3, column=8, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

        # 输出---------------------------------------------------------------------------------------
        # 创建提取结果输出框
        output_label = ttk.Label(self.window, text="输出结果:")
        output_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.output_text = tk.StringVar()
        # 创建滚动文本框
        self.output_scroll = scrolledtext.ScrolledText(self.window, width=40, height=10)
        self.output_scroll.grid(row=4, column=2, rowspan=10, columnspan=8, padx=10, pady=10, sticky=tk.NSEW)
        self.output_scroll.configure(state="disabled") # 设置滚动文本框为只读状态
        self.description_label = ttk.Label(self.window, text="三个功能：1.解析选中文本；2.针对选中文本检索；3.针对选中文本提取词性&正则式匹配")
        self.description_label.grid(row=14, column=0, rowspan=1, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

    def on_closing(self):
        self.window.destroy()  # 销毁窗口
        exit(0)

    def english_combobox_selected(self, event):
        self.language = "English"
        self.name = self.English_combobox.get()
        self.Chinese_combobox.set('')
        self.Chinese_tag_combobox.set('')

    def chinese_combobox_selected(self, event):
        self.language = "Chinese"
        self.name = self.Chinese_combobox.get()
        self.English_combobox.set('')
        self.English_tag_combobox.set('')

    def english_tag_combobox_selected(self, event):
        if self.language == "Chinese":
            messagebox.showerror(title="Select error", message="No English book selected")
            self.English_tag_combobox.set('')

    def chinese_tag_combobox_selected(self, event):
        if self.language == "English":
            messagebox.showerror(title="Select error", message="No Chinese book selected")
            self.Chinese_tag_combobox.set('')

    def checkbox_click(self):
        checked = self.checkbox_var.get()
        if checked:
            self.in_named_entities = True
        else:
            self.in_named_entities = False
        self.English_tag_combobox.set('')
        self.Chinese_tag_combobox.set('')


    # 解析按钮
    def analyze_button_click(self):
        t = time.time()
        if self.name == '':
            messagebox.showerror(title="Analyze error", message="No book selected")
            return
        # 解析该路径文件，并存储分析数据到对象
        information = self.extraction_module.generate(self.name, self.language)
        # 提示解析完成
        messagebox.showinfo(title="Analyze complete", message=information+"\nCost " + str(time.time()-t) + " seconds.")


    # 检索按钮
    def retrieval_button_click(self):
        # 获得检索结果
        if self.language == '' or self.name == '':
            messagebox.showerror(title="Retrieval error", message="No book selected")
            return
        input_text = self.input_entry.get()
        sorted_texts, sorted_scores = self.extraction_module.search_bm25(self.name, input_text)
        if sorted_texts == False:
            messagebox.showerror(title="Retrieval error", message="Book should analyze firstly.")
            return

        # 生成展示字符串
        output_text = ""
        cnt = 0
        for text, score in zip(sorted_texts, sorted_scores):
            if score <= 0: break
            output_text = output_text + "Text:\t" + str(text) + "\nScore:\t" + str(score) + "\n\n"
            cnt = cnt+1
        output_text = "Find " + str(cnt) + " items.\n" + output_text

        # 提示检索完成
        messagebox.showinfo(title="Retrieval complete", message="Find " + str(cnt) + " items.")

        # 展示到滑动窗口
        self.output_scroll.configure(state="normal")  # 先将滚动文本框设置为可编辑状态
        self.output_scroll.delete("1.0", tk.END)  # 清空文本框内容
        self.output_scroll.insert(tk.END, output_text)  # 在文本框中插入结果
        self.output_scroll.configure(state="disabled")  # 将滚动文本框设置为只读状态


    # 提取
    def extract_button_click(self):
        if self.language == '' or self.name == '':
            messagebox.showerror(title="Retrieval error", message="No book selected")
            return

        # 获取检索信息：
        tag = ''
        pattern = ''
        if self.language == "English":
            tag = self.English_tag_combobox.get().split('-')[0]
        elif self.language == "Chinese":
            tag = self.Chinese_tag_combobox.get().split('-')[0]
        if self.input_text.get() != '':
            pattern = self.input_text.get()
        else:
            pattern = self.re_combobox.get()
            if pattern != '':
                pattern = pattern.split('-')[0]

        # 查询的tag为空则匹配全部tag，查询的输入为空则匹配全部token
        ans = []
        print(tag, pattern)
        if tag == '':
            if pattern == '':
                messagebox.showerror(title="Extraction error", message="No tag or re_query.")
                return
            else:
                ans = self.extraction_module.search_reByName(self.name, self.re_formats[pattern])
        else:
            ans = self.extraction_module.search_byTag(self.name, tag)
            if pattern != '':
                ans = self.extraction_module.search_reByData(ans, self.re_formats[pattern])

        # 根据命名实体识别过滤
        if self.in_named_entities == True:
            ans = self.extraction_module.filter_named_entities(self.name, ans)

        # 生成展示字符串
        output_text = "Find " + str(len(ans)) + " tokens.\n"
        for token in ans:
            output_text = output_text + token + ", "

        # 提示提取完成
        messagebox.showinfo(title="Extract complete", message="Find " + str(len(ans)) + " items.")

        # 展示到滑动窗口
        self.output_scroll.configure(state="normal")  # 先将滚动文本框设置为可编辑状态
        self.output_scroll.delete("1.0", tk.END)  # 清空文本框内容
        self.output_scroll.insert(tk.END, output_text)  # 在文本框中插入结果
        self.output_scroll.configure(state="disabled")  # 将滚动文本框设置为只读状态


    def run(self):
        self.window.mainloop()