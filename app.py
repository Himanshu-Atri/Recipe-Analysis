# Recipe Analysis: Fine-tune an LLM to parse cooking recipes, extract ingredients, 
# and provide a detailed breakdown of macro/micro-nutrients and calorie counts. 
# If using Gen AI create multiple parallel  requests to ChatGPT, Gemin or Co-Pilot

from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

# importing the Libraries
import streamlit as st
import os
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage
from groq import Groq

# configuring the gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# loading Gemini flash model
model=genai.GenerativeModel(model_name="gemini-1.5-flash",
                            system_instruction="you are a cook and you only respond to cooking recipes or cooking related questions. you will receive a cooking recipes as input. you task is to extract ingredients, and provide a detailed breakdown of macro/micro-nutrients and calorie counts. give ingredients, macro/micro-nutrients and calorie counts in tabular format."
                            ) 

# loading openai model
openai_bot = ChatOpenAI(temperature=0.6, openai_api_key=os.environ["OPENAI_API_KEY"])

# loading llama model
client = Groq(
    api_key=os.getenv("LLAMA_API_KEY"),
)

   
#  getting openai's response  
def get_openai_response(question):
    response = openai_bot([
        SystemMessage(content="you will receive a cooking recipes as input. you task is to extract ingredients, and provide a detailed breakdown of macro/micro-nutrients and calorie counts."),
        HumanMessage(content=question)
    ])
    
    return response
    
    
#  getting gemini's response 
def get_gemini_response(question):
    response=model.generate_content(question, stream=True)
    return response


def get_llama_response(question):
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a cook and you only respond to cooking recipes or cooking related questions. you will receive a cooking recipes as input. you task is to extract ingredients, and provide a detailed breakdown of macro/micro-nutrients and calorie counts."
        },
        
        {
            "role": "user",
            "content": question,
        }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return response.choices[0].message
    


# starting of th e app
if __name__ == '__main__':

    st.set_page_config(page_title="Receipe Analysis")

    st.title("FlavorFusion: Your Virtual Kitchen Guide 🧑🏻‍🍳")


    input = st.text_area("Recipe: ", key="input")
    submit = st.button("Submit Recipe")
    
    if submit and input:
        #  showing gemini's response
        try:
            gemini_response = get_gemini_response(input)

            st.subheader("Gemini Response is")
            gemini_response_placeholder = st.empty()
            
            accumulated_text = ""
            for chunk in gemini_response:
                accumulated_text += chunk.text 
                gemini_response_placeholder.write(accumulated_text)

            gemini_response_placeholder.write(gemini_response.text)
        except Exception as e:
            st.error(e.text)


        # showing the openai response
        st.subheader("OpenAI Response is")
        openai_response_placeholder = st.empty()
        
        try:
            openai_response = get_openai_response(input)
            openai_response_placeholder.write(openai_response.content)
        except Exception as e:
            st.error(e)
            
        # showing the llama response
        st.subheader("Llama Response is")
        llama_response_placeholder = st.empty()
        
        try:
            llama_response = get_llama_response(input)
            llama_response_placeholder.write(llama_response.content)
        except Exception as e:
            st.error(e)
        
