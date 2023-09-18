import gradio as gr
import random
import requests

def ScrapeData(message):
    
    try:
        """
        Returns the response from rasa chatbot
        """
        url = "http://127.0.0.1:8000/data"
        headers = {"Content-Type": "application/json"}
        data = {"content": message}
        

        response = requests.post(url, json=data, headers=headers)

        # You can then access the response content
        
        if response.json():
            ella_response = response.json()[0]
        else:
            return "Error scraping Data"

        result = ""
        
        return result
    except Exception as e:
        print(e)
        return "Error. Please try again."

with gr.Blocks(theme=gr.themes.Soft(), title="ClickClick Scrapper", css="footer {visibility: hidden}") as demo:
    
    style_msg_textbox = {
    "border": "2px solid blue",  # Replace "blue" with the color you want
    "padding": "10px",
    "margin": "10px",
    }
    
    gr.Markdown("""<h1> <center> Scrape Business Data </center>""")
    chatbot = gr.Chatbot().style(height=450, width=100)
    msg = gr.Textbox(placeholder="Type your query here...", autofocus = True, show_copy_button = True)
    print("Message: ", msg)
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        print("Input Message: ", message)
        bot_message = ScrapeData(message)
        print("Bot Message: ", bot_message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    # Launch
    demo.launch(share = True, debug=True, server_name="0.0.0.0", server_port=7860)