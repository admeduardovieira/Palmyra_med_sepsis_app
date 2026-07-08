![PyPI - Version](https://img.shields.io/badge/Pyhton-v3.11.10-blue)
![PyPI - Version](https://img.shields.io/badge/shiny%20for%20python-v0.10.2-blue)
![PyPI - Version](https://img.shields.io/badge/chromadb-v0.5.23-brown)
![PyPI - Version](https://img.shields.io/badge/llama%20index-v0.12.5-blue)
![PyPI - Version](https://img.shields.io/badge/Writer_Palmyra_med_llm-70b-blue)
![PyPI - Version](https://img.shields.io/badge/NVIDIA_platform-green)
![PyPI - Version](https://img.shields.io/badge/ISAAC_sepsis-3.0-%23000055)


# Palmyra_med_sepsis_app
 This is the repository for a research project concerning building LLM-RAG-based applications.
## Overview
The repository contains files with persisting ChromaDB vector stores used for the functioning of a RAG-based software application that uses elements of a [multi-agentic approach](https://arxiv.org/pdf/2311.10537).
## The software applications for decision-making at an early stage of sepsis
The application requires input of information about a particular sepsis case as a clinical vignette. By pressing respective buttons on the application GUI, the user will get 
* *literature-based recommendations* concerning the management of a particular sepsis case at an early stage (e.g., before culture results are available)
* *antibiotic recommendations*
* a *statement concerning the compliance of the generated recommendations with current sepsis guidelines*

The appearance of the user interface of the application 👇:

![GUI](https://github.com/user-attachments/assets/985f9ec4-6ef4-4909-aa2b-c45e51bfc8fd)

The application is built using [Shiny for Python package](https://shiny.posit.co/py/), and the inference engine is [Palmyra-med 70B LLM](https://writer.com/blog/palmyra-med-fin-models/) hosted on [NVIDIA platform](https://build.nvidia.com/explore/discover).

### Availability
To experiment with the application, you can build it on your machine (the code is available in *app.py*) or access the cloud version (which uses GPT-3.5-turbo as an inference engine) on [huggingface](https://huggingface.co/spaces/LlmRAGbasedAPPs/LLM_MA_RAG_Sepsis) after sending a request to victor.iapascurta@usmf.md. 
By activating the **How to Use the Application** button on the upper horizontal menu, the user gets instructions on how to use the application.

### Acknowledgments
This application is part of the following projects:
- Project PN-IV-PCB-RO-MD-2024-036 "DACISLAB: Virtual laboratory on open data and open science in the new generation of computing continuum systems";
- Postdoctoral project no. 25.00208.5007.07/PD "Intelligent Software Methods and Algorithms for Intensive Care: A Complexity Science Approach," funded by the National Agency for Research and Development (NARD) of Moldova.
