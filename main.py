import gradio as gr
from Query import Query
from YouTubeHelper import YouTubeHelper

query = Query()


def process_video(video_url):
    yt_helper = YouTubeHelper(video_url)
    query.set_content(yt_helper.get_formatted_transcript())

    return 'Video processed.'


def add_text(history, text):
    history = history + [[text, None]]
    return history, ''


def get_response(history):
    response = query.get_response(history[-1][0])
    history[-1][1] = response

    return history


with gr.Blocks(theme=gr.themes.Soft(), title='Chatbot for Youtube') as demo:
    with gr.Row(elem_id='row'):
        with gr.Column(scale=20):
            video_url = gr.Textbox(label='YouTube url')
            process_button = gr.Button('Process url')
            process_status = gr.Markdown()

        with gr.Column(scale=80):
            chatbot = gr.Chatbot(label='Chatbot', value=[], elem_id='chatbot')

            question = gr.Textbox(
                elem_id='text',
                label='Message',
                placeholder='Enter text and press [Enter]',
            )


    process_button.click(
        process_video, [video_url], [process_status]
    )

    question.submit(add_text, [chatbot, question], [chatbot, question]).then(
        get_response, [chatbot], [chatbot]
    )

demo.launch(share=True)
