from shiny import App, ui, reactive, render
import os
import openai
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

os.environ["NVIDIA_API_KEY"] = "Your NVIDIA_API_KEY"
os.environ["NVIDIA_MODEL_NAME"] = "writer/palmyra-med-70b"
os.environ["NVIDIA_BASE_URL"] = "https://integrate.api.nvidia.com/v1"

# Another option is using an OpenAI model. In this case the key and the model should be adjusted accordingly. 

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

def create_query_engine(db_path, collection_name):
    db_client = chromadb.PersistentClient(path=db_path)
    chroma_collection = db_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    return index.as_query_engine()


# Define UI components
app_ui = ui.page_fluid(
    # Black strip at the top
    ui.tags.div(
        ui.tags.div(
            ui.HTML('<i class="fa fa-search" style="color: white; margin-right: 10px;"></i>'),
            "Sepsis Management Assistant ISAAC-Sepsis-3-RAG",
            style="color: white; font-size: 1.2em; display: inline-block; vertical-align: middle;"
        ),
        style="""
            background-color: #000055;
            height: 1.5cm;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 10px;
        """
    ),
    # Navigation bar
    ui.page_navbar(
        ui.nav_panel(
            "Assistant",
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_text("input1", "Diagnosis:"),
                    ui.input_text("input2", "Demographic:"),
                    ui.input_text("input3", "Vital_signs:"),
                    ui.input_text("input4", "Laboratory_findings:"),
                    ui.input_text("input5", "Medical_history:"),
                    ui.input_text("input6", "Special_comments:"),
                   
                    ui.input_action_button("submit", "Submit"),
                    ui.input_action_button("reset", "Reset")
                    
               ),
                ui.panel_main(
                    ui.input_action_button("get_result0", "Read and verify input"),
                    ui.output_text("joined_text_output"),
                    ui.hr(),
                    ui.input_radio_buttons("response_length", "Select Response Length:", 
                                           choices=["Regular response", "Short response"], selected="Regular response"),
                    ui.hr(),               
                    ui.input_action_button("result1_btn", "Get literature-based sepsis management recommendations"),
                    ui.output_text("result1"),
                    ui.hr(),               
                    ui.input_action_button("result2_btn", "Get antibiotic recommendations"),
                    ui.output_text("result2"),
                    ui.hr(),               
                    ui.input_action_button("result3_btn", "Get compliance-with-guidelines conclusion"),
                    ui.output_text("result3"),
                    ui.hr()

                )
            )
        ),
       ui.nav_panel(
           "How to Use the Application",
           
               ui.panel_main(
                   ui.markdown("""
                   ### How to Use the Application
                   1. Enter text in the input fields. The "Special comments" field requires information about potential site of infection:
                   Pulmonary Infections (e.g., Community-Acquired Pneumonia (CAP) or Hospital-Acquired Pneumonia/Ventilator-Associated Pneumonia (HAP/VAP));
                   Central Nervous System Infections; Skin and Soft Tissue Infections (e.g., Necrotizing Fasciitis, Nonpurulent Cellulitis/Erysipelas, Purulent Infection);
                   Intra-Abdominal Infection; Genitourinary Infections. etc.
                   2. Click on 'Submit' to join and display the input text.
                   3. Short response radio-button can be used in case of time constrains in a clinical setting.
                   4. Use the additional buttons to see different transformations of the joined text.
                   4. Click 'Reset' to clear all input fields.
                   """)
                )
           )
      )
)

# Define processing functions
def join_inputs(inputs):
    return '; '.join(inputs)
    
def format_inputs_for_display(inputs, names):
    return '; '.join(f"{name}: {text}" for name, text in zip(names, inputs))

def get_response_length1(selected_option):
    return 300 if selected_option == "Regular response" else 50

def get_response_length2(selected_option):
    return 100 if selected_option == "Regular response" else 30

# Define server logic
def server(input, output, session):
    joined_text_value = reactive.Value("")
    formatted_text_value = reactive.Value("")
    result1_text = reactive.Value("")
    result2_text = reactive.Value("")
    result3_text = reactive.Value("")

    response_length1_value = reactive.Value(300)  # Default to 300 tokens
    response_length2_value = reactive.Value(50)
    
    input_names = ["Diagnosis", "Demographic", "Vital_signs", "Laboratory_findings", "Medical_history", "Special_comments"]

    @reactive.Effect
    @reactive.event(input.submit)
    def submit_action():
        joined_text_value.set(join_inputs([input.input1(), input.input2(), input.input3(), input.input4(), input.input5(), input.input6()]))
    
    @reactive.Effect
    @reactive.event(input.reset)
    def reset_action():
        session.send_input_message("input1", {"value": ""})
        session.send_input_message("input2", {"value": ""})
        session.send_input_message("input3", {"value": ""})
        session.send_input_message("input4", {"value": ""})
        session.send_input_message("input5", {"value": ""})
        session.send_input_message("input6", {"value": ""})
        joined_text_value.set("")
        formatted_text_value.set("")
        result1_text.set("")
        result2_text.set("")
        result3_text.set("")
        response_length1_value.set(300)  # Reset to default
        response_length2_value.set(50)  # Reset to default

    @reactive.Effect
    @reactive.event(input.response_length)
    def update_response_length1():
        response_length1_value.set(get_response_length1(input.response_length()))

    @reactive.Effect
    @reactive.event(input.response_length)
    def update_response_length2():
        response_length2_value.set(get_response_length2(input.response_length()))

    
    
    @reactive.Effect
    @reactive.event(input.get_result0)
    def get_result0():
        formatted_text_value.set(format_inputs_for_display([input.input1(), input.input2(), input.input3(), input.input4(), input.input5(), input.input6()], input_names))
   
    @output
    @render.text
    def joined_text_output():
        return formatted_text_value.get()

    @reactive.Effect
    @reactive.event(input.result1_btn)
    def get_result1():
        query_engine_sepsis = create_query_engine("sepsis_management_chroma_db", "sepsis_management")
        query_sepsis_management = f"The sepsis management recommendations you provide should be maximally based on the queried database and {joined_text_value.get()}. The length of your response should not exceed {response_length1_value.get()} tokens."
        sepsis_recommendations = query_engine_sepsis.query(query_sepsis_management)
#        result1_text.set(query_engine_sepsis.query(joined_text_value.get()))
        result1_text.set(sepsis_recommendations)
            
    @reactive.Effect
    @reactive.event(input.result2_btn)
    def get_result2(): 
        query_engine_antibiotics = create_query_engine("sepsis_antibiotics_chroma_db",
                                                       "sepsis_antibiotic_recommendations")
        query_antibiotics = f"The antibiotics recommendations you provide should be maximally based on the queried database and {input.input6()}. When possible, recommend particular antibiotics and their doses."
        antibiotic_recommendations = query_engine_antibiotics.query(query_antibiotics)
        result2_text.set(antibiotic_recommendations)
            
    @reactive.Effect
    @reactive.event(input.result3_btn)
    def get_result3():
        combined_result = f"{result1_text.get()} | {result2_text.get()}"
        compliance_response = create_query_engine("sepsis_guidelines_chroma_db",
                                                  "sepsis_management_guidelines")
        compliance_query = f"Check if the following sepsis management recommendations comply with current sepsis management guidelines. Return 'compliant' or 'non-compliant': {combined_result}"
        compliance_content = str(compliance_response.query(compliance_query))

#        print("Compliance response:", compliance_content)  # Debug print

        if "compliant" in compliance_content:
            compliance_statement = "Recommendations comply with current sepsis management guidelines."
            compliance_explanation = ""
        else:
            compliance_statement = "Compliance with current sepsis management guidelines is questionable."
            compliance_explanation_query = f"Explain why the following recommendations do not comply: {combined_result}. The length of your response should not exceed {response_length2_value.get()} tokens."
            compliance_explanation_response = compliance_response.query(compliance_explanation_query)
            compliance_explanation = str(compliance_explanation_response)
            compliance_suggestion_query = f"Provide suggestions to make the following recommendations compliant: {combined_result}. The length of your response should not exceed {response_length2_value.get()} tokens."
            compliance_suggestion_response = compliance_response.query(compliance_suggestion_query)
            compliance_suggestions = str(compliance_suggestion_response)
            compliance_explanation += f"\n\nTo achieve compliance, consider the following suggestions:\n{compliance_suggestions}"
#        print("Compliance statement:", compliance_statement)  # Debug print
        result3_text.set(compliance_explanation)

       
    @output
    @render.text
    def result1():
        return result1_text.get()
    
    @output
    @render.text
    def result2():
        return result2_text.get()
    
    @output
    @render.text
    def result3():
        return result3_text.get()

# Create the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
