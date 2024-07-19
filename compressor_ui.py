from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from os.path import basename, dirname, isdir, isfile, getsize
from Huffman import *


class GUI:
    def __init__(self, rt):
        self.root = rt
        self.root.title("File Compressor")
        self.root.geometry("800x600+350+75")
        self.root.configure(background='')
        self.root.minsize(800, 600)
        self.root.maxsize(800, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_window)

        self.file_path = None
        self.file_dir = None
        self.file_size = 0
        self.encoded_file_size = 0
        self.decoded_file = None

        self.comp_f = None

        self.inner_frm1 = None
        self.l1 = None
        self.inputFile = None

        self.inner_frm2 = None
        self.l2 = None
        self.inputLocation = None

        self.l3 = None

        self.MenuBar = None
        self.FileMenu = None

        self.instr_f = None

        self.MenuBar = Menu(self.root)
        self.MenuBar.add_cascade(label="Encode", command=self.compressor_gui)
        self.MenuBar.add_cascade(label="Decode", command=self.decompressor_gui)
        self.MenuBar.add_cascade(label='Exit', command=self.on_closing_window)
        self.root.config(menu=self.MenuBar)
        self.compressor_gui()

    def compressor_gui(self):
        self.file_path = None

        self.comp_f = Frame(
            self.root,
            bg='#ffcccc',
            borderwidth=2,
            width=500,
            height=275
        )
        self.comp_f.place(x=25, y=275, width=750, height=250)

        self.inner_frm1 = Frame(
            self.comp_f,
            bg='#ffcccc',
            borderwidth=0,
            width=690,
            height=75
        )
        self.inner_frm1.pack()

        self.l1 = Label(
            self.inner_frm1,
            text="File : ",
            font=("Times New Roman", 12),
            width=10
        )
        self.l1.grid(row=0, column=0, padx=2, pady=2, ipady=2, ipadx=2)

        self.inputFile = Text(
            self.inner_frm1,
            height=1,
            width=65
        )
        self.inputFile.grid(row=0, column=1, padx=2, pady=2, ipady=2, ipadx=2)

        Button(self.inner_frm1,
               text="Upload",
               command=self.upload_file,
               font=("", 12, "bold"),
               bg='#87CEEB',
               fg='#ffffff',
               pady=2,
               padx=3
               ).grid(row=0, column=2, padx=2, pady=2, ipady=2, ipadx=2)

        self.inner_frm2 = Frame(
            self.comp_f,
            bg='#ffcccc',
            borderwidth=0,
            width=690,
            height=75
        )
        self.inner_frm2.pack()

        self.l2 = Label(
            self.inner_frm2,
            text="Location : ",
            font=("Times New Roman", 12),
            width=10
        )
        self.l2.grid(row=0, column=0, padx=2, pady=2, ipady=2, ipadx=2)

        self.inputLocation = Text(
            self.inner_frm2,
            height=1,
            width=65
        )
        self.inputLocation.grid(row=0, column=1, padx=2, pady=2, ipady=2, ipadx=2)

        Button(self.inner_frm2,
               text="Encode",
               command=self.encode_doc,
               font=("", 12, "bold"),
               bg='#87CEEB',
               fg='#ffffff',
               pady=2,
               padx=3
               ).grid(row=0, column=2, padx=2, pady=2, ipady=2, ipadx=2)

        self.l3 = Label(
            self.comp_f,
            # text=f"Location of Encoded file and code file :\n{dirname(self.file_path)}",
            font=("Times New Roman", 15),
            width=650
        )
        self.l3.pack(pady=5, ipady=3, ipadx=3)

        self.instr_f = Frame(
            self.root,
            bg='#ffffff',
            borderwidth=2,
            width=500,
            height=275
        )
        self.instr_f.place(x=25, y=25, width=750, height=250)
        Label(self.instr_f,
              text="Instructions :",
              background="#ffffff",
              font=("Consolas", 15),
              justify="center"
              ).pack(ipady=3)

        Label(self.instr_f,
              text="""
1. Click on 'Upload' to upload a file.
2. Click on 'Encode' to compress the file.
3. Compression will create two files, a encoded file and a code file.
4. Compressed file will be created in same folder the original file was by default.
5. Name of compressed and code file will be 'filename_encoded.txt' and 'filename_encoded.json'.""",
              width=700,
              font=("Times", 12),
              justify="left",
              background="#000000",
              foreground="#FACA2F"
              ).pack(ipady=3)

    def upload_file(self):
        self.inputFile.delete("1.0", "end")
        self.inputLocation.delete("1.0", "end")
        self.file_path = askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt")]
        )
        # self.l1.configure(text=f"file : {self.file_path}")
        self.inputFile.insert(END, self.file_path)
        self.file_dir = dirname(self.file_path) + '/'
        self.inputLocation.insert(END, self.file_dir)

    def encode_doc(self):
        self.file_path = self.inputFile.get(1.0, "end-1c")

        if self.file_path in (None, ''):
            messagebox.showwarning('Warning', "You haven't selected any file",
                                   parent=self.root)
            return
        if not isfile(self.file_path):
            messagebox.showwarning('Warning', "File doesn't exits!",
                                   parent=self.root)
            return

        file_name = basename(self.file_path).replace('.txt', '')
        self.file_dir = self.inputLocation.get(1.0, "end-1c")

        if not isdir(self.file_dir):
            messagebox.showwarning('Warning', "Folder doesn't exits!",
                                   parent=self.root)
            return

        if self.file_dir[-1] == '/':
            coded_file_name = self.file_dir + file_name + '_encoded'
        else:
            coded_file_name = self.file_dir + '/' + file_name + '_encoded'

        with open(self.file_path, 'r') as f:
            s_file = f.read()
            freq_list = cal_freq(s_file)
        self.file_size = getsize(self.file_path)

        encoding, code_book = create_encoding(freq_list, s_file)

        write_binary_encoding(encoding, coded_file_name + '.txt')
        write_code_file(code_book, coded_file_name + '.json')

        self.encoded_file_size = getsize(coded_file_name + '.txt')

        self.l3.configure(
            text=f"file size is reduced by {round(100 - (self.encoded_file_size / self.file_size) * 100, 2)} %")
        self.inputFile.delete("1.0", "end")
        self.inputLocation.delete("1.0", "end")

    def decompressor_gui(self):
        self.file_path = None

        self.comp_f = Frame(
            self.root,
            bg='#ffcccc',
            borderwidth=2,
            width=500,
            height=275
        )
        self.comp_f.place(x=25, y=275, width=750, height=250)

        self.inner_frm1 = Frame(
            self.comp_f,
            bg='#ffcccc',
            borderwidth=0,
            width=690,
            height=75
        )
        self.inner_frm1.pack()

        self.l1 = Label(
            self.inner_frm1,
            text="File : ",
            font=("Times New Roman", 12),
            width=10
        )
        self.l1.grid(row=0, column=0, padx=2, pady=2, ipady=2, ipadx=2)

        self.inputFile = Text(
            self.inner_frm1,
            height=1,
            width=65
        )
        self.inputFile.grid(row=0, column=1, padx=2, pady=2, ipady=2, ipadx=2)

        Button(self.inner_frm1,
               text="Upload",
               command=self.upload_file,
               font=("", 12, "bold"),
               bg='#87CEEB',
               fg='#ffffff',
               pady=2,
               padx=3
               ).grid(row=0, column=2, padx=2, pady=2, ipady=2, ipadx=2)

        self.inner_frm2 = Frame(
            self.comp_f,
            bg='#ffcccc',
            borderwidth=0,
            width=690,
            height=75
        )
        self.inner_frm2.pack()

        self.l2 = Label(
            self.inner_frm2,
            text="Save as : ",
            font=("Times New Roman", 12),
            width=10
        )
        self.l2.grid(row=0, column=0, padx=2, pady=2, ipady=2, ipadx=2)

        self.inputLocation = Text(
            self.inner_frm2,
            height=1,
            width=65
        )
        self.inputLocation.grid(row=0, column=1, padx=2, pady=2, ipady=2, ipadx=2)

        Button(self.inner_frm2,
               text="Decode",
               command=self.decode_doc,
               font=("", 12, "bold"),
               bg='#87CEEB',
               fg='#ffffff',
               pady=2,
               padx=3
               ).grid(row=0, column=2, padx=2, pady=2, ipady=2, ipadx=2)

        self.l3 = Label(
            self.comp_f,
            # text=f"Location of Encoded file and code file :\n{dirname(self.file_path)}",
            font=("Times New Roman", 15),
            width=650
        )
        self.l3.pack(pady=5, ipady=3, ipadx=3)

        self.instr_f = Frame(
            self.root,
            bg='#ffffff',
            borderwidth=2,
            width=500,
            height=200
        )
        self.instr_f.place(x=25, y=25, width=750, height=200)
        Label(self.instr_f,
              text="Instructions :",
              background="#ffffff",
              font=("Consolas", 15),
              justify="center"
              ).pack(ipady=3)

        Label(self.instr_f,
              text="""
1. Click on 'Upload' to upload a file.
2. Click on 'Decode' to decompress the file.
3. Enter the path and name as you want save decompressed file.
4. For decompression, both encoded and .json (code file) should be in same folder.
5. Encoded and .json file must have same name.
6. In upload, you need to select only encoded file.""",
              width=700,
              font=("Times", 12),
              justify="left",
              background="#000000",
              foreground="#FACA2F"
              ).pack(ipady=3)

    def decode_doc(self):
        self.file_path = self.inputFile.get(1.0, "end-1c")

        if self.file_path in (None, ''):
            messagebox.showwarning('Warning', "You haven't selected any file",
                                   parent=self.root)
            return
        if not isfile(self.file_path):
            messagebox.showwarning('Warning', "File doesn't exits!",
                                   parent=self.root)
            return

        file_name = basename(self.file_path).replace('.txt', '')
        self.file_dir = self.inputLocation.get(1.0, "end-1c")

        '''if not isdir(dirname(self.encoded_file_dir)):
            messagebox.showwarning('Warning', "Folder doesn't exits!",
                                   parent=self.root)
            return'''

        if dirname(self.file_path)[-1] == '/':
            coded_file_name = dirname(self.file_path) + file_name
        else:
            coded_file_name = dirname(self.file_path) + '/' + file_name

        decoded = decode_file(coded_file_name + '.json', coded_file_name + '.txt')
        with open(self.file_dir, 'w') as df:
            df.write(decoded)

        self.inputFile.delete("1.0", "end")
        self.inputLocation.delete("1.0", "end")

    def on_closing_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
