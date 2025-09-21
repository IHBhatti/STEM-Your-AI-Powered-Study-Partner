import streamlit as st
def pdf_uploader():
  """create a file uploader for pdf documents"""
  return st.file_uploader(
      "Upload pdf files",
      type="pdf",
      accept_multiple_files=True,
      help="upload one or more sindh textbook pdf books",
      )