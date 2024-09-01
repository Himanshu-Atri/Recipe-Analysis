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
from concurrent.futures import ThreadPoolExecutor

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
    try:
        response = openai_bot([
            SystemMessage(content="you will receive a cooking recipes as input. you task is to extract ingredients, and provide a detailed breakdown of macro/micro-nutrients and calorie counts."),
            HumanMessage(content=question)
        ])
        
        return response.content
    except Exception as e:
        return str(e)
    
    
#  getting gemini's response 
def get_gemini_response(question):
    try:
        response=model.generate_content(question)
        return response.text
    except Exception as e:
        return str(e)

#  getting llama's response
def get_llama_response(question):
    try:
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
        
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
    
    
def get_all_responses(question):
    
    with ThreadPoolExecutor() as executor:
        response_1 = executor.submit(get_gemini_response, question)
        response_2 = executor.submit(get_openai_response, question)
        response_3 = executor.submit(get_llama_response, question)
        
    return [response_1.result(), response_2.result(), response_3.result()]


# starting of th e app
if __name__ == '__main__':

    st.set_page_config(page_title="Receipe Analysis")

    st.title("FlavorFusion: Your Virtual Kitchen Guide 🧑🏻‍🍳")


    input = st.text_area("Recipe: ", key="input")
    submit = st.button("Submit Recipe")
    
    if submit and input:
    
        response_list = get_all_responses(input)
        
        # showing the gemini response
        st.subheader("Gemini Response is")
        st.write(response_list[0])
        
        # showing the openai response
        st.subheader("OpenAI Response is")
        st.write(response_list[1])
     
        # showing the llama response
        st.subheader("Llama Response is") 
        st.write(response_list[2])

            
            
    