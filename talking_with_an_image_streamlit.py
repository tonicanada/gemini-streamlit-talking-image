import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv, find_dotenv


def ask_and_get_answer(prompt, img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img])
    return response.text


def st_image_to_pil(st_image):
    import io
    from PIL import Image
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image


if __name__ == '__main__':
    load_dotenv(find_dotenv(), override=True)
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    st.image('gemini-logo.png')
    st.subheader('Talking with an Image 💫')
    # st.image('https//... .jpg')
    img = st.file_uploader('Select an Image: ', type=[
                           'jpg', 'jpeg', 'png', 'gif'])
    if img:
        st.image(img, caption='Talk with this image.')

        prompt = st.text_area('Ask a question about this image: ')
        if prompt:
            pil_image = st_image_to_pil(img)
            with st.spinner('Running ...'):
                answer = ask_and_get_answer(prompt, pil_image)
                st.text_area('Gemini Answer: ', value=answer)

            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history = ''

            value = f'Q: {prompt} \n\n A: {answer}'
            st.session_state.history = f'{value} \n\n {"*" * 100} \n\n {st.session_state.history}'

            h = st.session_state.history
            st.text_area(label='Chat History', value=h, height=400, key='history')
