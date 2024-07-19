# File Compressor with Huffman Algorithm
This project implements a file compression and decompression utility using the Huffman coding algorithm. It includes a graphical user interface (GUI) built with Tkinter.

## Features
- **File Compression:** Compresses text files using Huffman coding.
- **File Decompression:** Decompresses files encoded with the tool.
- **GUI:** User-friendly graphical interface for easy fiole selection and compression/decompression operations.

## Installation
### Prerequisities
- Python 3.x
- Tkinter (usually included with Python)
### Steps
1. Clone the repository:
```
git clone https://github.com/MayurVadhadiya360/file-compressor-with-huffman-algo.git
cd file-compressor-with-huffman-algo
```
2. Install the required packages (if any). You can use `pip install pkg-name` to install any missing packages

## Usage
### Running the Application
1. Navigate to the project directory.
2. Run the application:
```
python main.py
```
3. The GUI will open, allowing you to select files for compression or decompression.

### Creating `.exe` File
You can create `.exe` file using following command:
```
pyinstaller -F -w --onefile main.py
```
After running command, you can find `.exe` file at `dist/main.exe`. You can remove other files created i.e., `build/*` and `main.spec`.

### Instructions
#### Compressing a File
1. Click on the "**Encode**" menu.
2. Click the "**Upload**" button to select the text file you want to compress.
3. The file path will appear in the "**File**" text box.
4. The location where the encoded files will be saved will appear in the "**Location**" text box. You can change this location if desired.
5. Click the "**Encode**" button.
6. The compressed file and the codebook file will be created in the specified location with `_encoded` appended to their names.
#### Decompressing a File
1. Click on the "**Decode**" menu.
2. Click the "**Upload**" button to select the encoded file.
3. The file path will appear in the "**File**" text box.
4. Enter the path and name for the decompressed file in the "**Save as**" text box.
5. Click the "**Decode**" button.
6. The decompressed file will be saved in the specified location.

### Example
Here is an example of using the tool to compress and decompress a file:
1. Select a text file (`example.txt`) to compress.
2. The tool will create `example_encoded.txt` and `example_encoded.json` in the same directory.
3. To decompress, select `example_encoded.txt`.
4. Specify the output path and name, such as `example_decoded.txt`.
5. Click "Decode" to get the original content back in `example_decoded.txt`.

## Acknowledgements
- The Huffman coding algorithm.
- Tkinter for the GUI.
