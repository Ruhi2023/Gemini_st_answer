import streamlit as st 
import os
import io
from PIL import Image
import google.generativeai as genai

def upload_to_genai(path, mime_type):
   file = genai.upload_file(path, mime_type=mime_type)
   print(f"file has been uploaded to genai: {file.name}")
   return file

def take_images(uplo):
  """
  Take images from file upload then makes a folder (if not aleredy present), uploads to gemini using upload to genai
  """
  par = os.getcwd()
  with open(os.path.join(par, "file upload", uplo.name), "wb") as file:
    file.write(uplo.getvalue())
  f_nam =upload_to_genai(os.path.join(par, "file upload",uplo.name), mime_type="image/png")
  return f_nam.name
def make_img_inp(names):
  """
  Makes a list of images from the uploaded files
  """
  lis =list(map(genai.get_file, names))
  return lis




st.write("""Please provide your google API key
          """)
gak = st.text_input(label="Enter your google API key",type="password")
genai.configure(api_key=gak)
pr = st.text_input("Enter your prompt")
use_img = st.checkbox("Work with images")


if use_img:
    uplad_files = st.file_uploader("Upload files", type=["png"], accept_multiple_files=True) 
    names = list(map(take_images, uplad_files))
    #TODO: make a function map that will use upload files and return a file object appended to list
if st.checkbox("Generate Text"):
    #st.write(genai.get_file(a[0]))
    generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": int(1024*8),
  "response_mime_type": "text/plain",
}
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
    model_input = [pr]
    if use_img:
       
       model_input.extend(make_img_inp(names))
       
       #TODO: make a model input function that will make append a model input
    res = model.generate_content(model_input)
    st.write(f":orange-background[{res.text}]")

if st.checkbox("Delete files", value=False):  
  st.write("Files in cache being deleted: ")
  if genai.list_files() is not None:
      for f in genai.list_files():
        st.write(f"Deleting {f}")
        genai.delete_file(f)
  par = os.getcwd()
  path_files = os.listdir(os.path.join(par, "file upload"))
  if len(path_files) != 0:
      for f in path_files:
        try:
          os.remove(os.path.join(par, "file upload",f))
        except:
            st.write(f"Could not delete {f}") 
