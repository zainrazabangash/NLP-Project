import nbformat
import os
import time
import gradio as gr
from jupyter_client import KernelManager
import json
import webbrowser
import re

def run_notebook(notebook_path):

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Start a kernel
    km = KernelManager(kernel_name='python')
    km.start_kernel()
    kc = km.client()
    kc.start_channels()
    kc.wait_for_ready()
    
    try:
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != 'code':
                continue
                
            try:
                print(f"Executing cell {i+1}...")
                
                msg_id = kc.execute(cell.source)
                
                while True:
                    msg = kc.get_shell_msg()
                    if msg['parent_header']['msg_id'] == msg_id:
                        break
                
                while True:
                    msg = kc.get_iopub_msg()
                    if msg['parent_header']['msg_id'] == msg_id:
                        if msg['header']['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                            break
                        if msg['header']['msg_type'] == 'stream':
                            output_text = msg['content']['text']
                            print(output_text)
                            localhost_match = re.search(r'http://127.0.0.1:\d+', output_text)
                            if localhost_match:
                                url = localhost_match.group(0)
                                print(f"\nOpening {url} in your default browser...")
                                webbrowser.open(url)
                        elif msg['header']['msg_type'] == 'error':
                            print('Error:', msg['content']['traceback'])
                
                print(f"Cell {i+1} executed successfully!")
                
                time.sleep(2)
                
                if i == len(nb.cells) - 1:
                    print("Interface is ready!")
                    print("Press Ctrl+C to stop the script when you're done with the interface.")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\nStopping the script...")
                        gr.close_all()
                        print("Interface closed successfully!")
                        
            except Exception as e:
                print(f"Error executing cell {i+1}: {str(e)}")
                raise e
                
    finally:
        kc.stop_channels()
        km.shutdown_kernel()

if __name__ == "__main__":
    notebook_path = "22I-0513_22I-0520.ipynb"
    run_notebook(notebook_path) 