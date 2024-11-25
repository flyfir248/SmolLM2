import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# Load model and tokenizer
@st.cache_resource  # Cache the model to avoid reloading on every app run
def load_model():
    # Specify the 360M model checkpoint
    checkpoint = "HuggingFaceTB/SmolLM2-360M-Instruct"
    st.write("Downloading and loading the 360M model. This may take a moment...")

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForCausalLM.from_pretrained(
        checkpoint,
        torch_dtype=torch.float16,  # Use FP16 for performance optimization
        device_map="auto"  # Automatically map to GPU if available
    )
    return model, tokenizer


# Initialize model and tokenizer
model, tokenizer = load_model()

# Streamlit app title and description
st.title("SmolLM2 Interactive App (360M)")
st.write("This app uses the **360M version of SmolLM2-Instruct** to generate responses. Enter your prompt below!")

# Input section
st.header("Enter Your Prompt")
user_prompt = st.text_area("Write your query here:", value="", height=150)

# Sidebar for model parameters
st.sidebar.header("Model Parameters")
max_tokens = st.sidebar.slider("Max Tokens", min_value=10, max_value=200, value=50, step=10)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
top_p = st.sidebar.slider("Top-p (Nucleus Sampling)", min_value=0.0, max_value=1.0, value=0.9, step=0.1)

# Button to generate output
if st.button("Generate"):
    if user_prompt.strip():
        # Tokenize and generate response
        inputs = tokenizer.encode(user_prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )
        # Decode and display output
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.subheader("Generated Response")
        st.write(response)
    else:
        st.warning("Please enter a valid prompt.")

# About section
st.sidebar.header("About")
st.sidebar.write("""
This app is powered by the 360M version of SmolLM2-Instruct.
For more details, visit the [Hugging Face Model Card](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct).
""")
