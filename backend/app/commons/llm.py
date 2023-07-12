import openai
import os

def query_openai(prompt, num_songs, song_options):
    system_prompt = "You are a helpful assistant. Your job is to recommend songs for a music playlist given a list of song options. You will give your response in a JSON format with the following schema: {\"playlist\": [{\"song\": String, \"artist\": String}]}. Do not include any text in your response other than the JSON output."
    user_prompt = "I want to create a playlist that is: " + prompt + ". Given the following song options, create an appropriate playlist that is " + str(num_songs) + " songs long. Song options: " + song_options
    openai.api_key = os.getenv("OPENAI_API_KEY")
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
    )
    response_message = gpt_response["choices"][0]['message']['content']
    return response_message
