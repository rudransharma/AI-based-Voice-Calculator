import whisper  # Speech-to-text
import pyttsx3  # Text-to-Speech (TTS)
import openai   # GPT-4 for conversational AI
import sympy as sp  # For structured math calculations
import re
import speech_recognition as sr
from langchain.llms import OpenAI  # LangChain for AI pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load Whisper model for voice recognition
model = whisper.load_model("base")

# Initialize Text-to-Speech
tts = pyttsx3.init()

# OpenAI GPT-4 API Key (replace with your API key)
OPENAI_API_KEY = "Generate API KEy"
llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4")

# LangChain prompt template for solving math problems
math_prompt = PromptTemplate(
    input_variables=["question"],
    template="Solve this math problem step by step: {question}"
)
math_chain = LLMChain(llm=llm, prompt=math_prompt)

def recognize_speech_from_mic():
    """Capture and transcribe speech from the microphone using Whisper"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please say your calculation.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized Speech: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the speech.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

def extract_math_expression(text):
    """Extract mathematical expressions ensuring full calculations are captured"""
    text = re.sub(r"\bdivided by\b", "/", text)
    text = re.sub(r"\bplus\b", "+", text)
    text = re.sub(r"\bminus\b", "-", text)
    text = re.sub(r"\btimes\b", "*", text)
    text = re.sub(r"\bmultiplied by\b", "*", text)
    text = re.sub(r"\bsquare root of\b", "sqrt", text)

    expression = re.findall(r'\d+(?:\.\d+)?|[\+\-\*/()]|sqrt', text)
    
    if not expression:
        return None
    if expression[-1] in '+-*/':
        return None

    return ' '.join(expression)

def evaluate_expression(expression):
    """Evaluate the mathematical expression safely using sympy"""
    try:
        if not expression:
            return "Invalid expression"
        
        if "/ 0" in expression or "/0" in expression:
            return "Undefined (Division by Zero)"
        
        result = sp.sympify(expression)
        return float(result) if isinstance(result, sp.Rational) else result
    except Exception:
        return "Invalid expression"

def solve_using_gpt(query):
    """Solve math queries using GPT-4 or LLaMA"""
    response = math_chain.run({"question": query})
    return response

def speak_result(result):
    """Convert result to speech"""
    response = f"The result is {result}"
    tts.say(response)
    tts.runAndWait()

def main():
    """Main function to process user input via speech"""
    text = recognize_speech_from_mic()
    
    if not text:
        print("No valid input detected.")
        return
    
    expression = extract_math_expression(text)
    
    if expression:
        result = evaluate_expression(expression)
        print(f"Calculated Result: {result}")
        speak_result(result)
    else:
        print("Using AI for complex math...")
        ai_response = solve_using_gpt(text)
        print(f"AI Response: {ai_response}")
        speak_result(ai_response)

if __name__ == "__main__":
    main()
