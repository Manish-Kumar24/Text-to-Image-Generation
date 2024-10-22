import streamlit as st 
import requests
import base64
from PIL import Image
import io

st.title("Text to Image Generator")
st.write("Enter a text description to generate an Image")

# Add sidebar for configuration
st.sidebar.header("Configuration")

# Add a dropdown for selecting the model
model_options = ["stability.ai", "runway"]
selected_model = st.sidebar.selectbox("Select Model", model_options)

# Use the same API URL for both models
api_url = st.sidebar.text_input(
    "Backend API URL",
    "https://4068-35-247-57-12.ngrok-free.app"  # Using the same URL for both models
)

# Main interface for the text prompt
text_prompt = st.text_input("Enter your prompt:", "")

# Generate Image button
if st.button("Generate Image"):
    if not api_url:
        st.error("Please enter the backend API URL in the sidebar")
    else:
        with st.spinner("Generating image..."):
            try:
                # Send request to the backend API with the selected model
                response = requests.post(
                    f"{api_url}/generate",
                    json={
                        "text": text_prompt,
                        "model": selected_model  # Pass the selected model to the API
                    }
                )
                
                if response.status_code == 200:
                    # Decode and display the image
                    image_data = base64.b64decode(response.json()["image"])
                    image = Image.open(io.BytesIO(image_data))
                    st.image(image, caption=f"Generated Image using {selected_model}")
                else:
                    st.error(f"Failed to generate image. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Add prompt tips
st.markdown("""
### Tips for better prompts:
- Be specific in your descriptions
- Include details about style, lighting, and composition
- Try different variations of your prompt
""")
