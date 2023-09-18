import openai
import os
import tiktoken
import json

def callback_llm_req(attempt):
    return

def parse_response(gpt_response):
    gpt_response_parsed = []
    for option in gpt_response:
        try:
            gpt_response_json = json.loads(option)
            gpt_response_parsed.extend(gpt_response_json["playlist"])
        except:
            print("BAD RESPONSE FORMAT")
            # Will propogate empty result through workflow until eventually being handled later if there is not enough data
            continue
    return gpt_response_parsed

def query_gpt(batches, system_prompt, user_prompt, model="gpt-3.5-turbo"):
    responses = []
    for batch in batches:
        song_options_stringified = " ,".join(batch)
        try:
            gpt_response = openai.ChatCompletion.create(
                model=model,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt+song_options_stringified}
                    ]
            )
        except openai.error.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return []
        except openai.error.APIConnectionError as e:
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            return []
        except openai.error.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            return []
        responses.append(gpt_response["choices"][0]['message']['content'])
    return parse_response(responses)

def batch_songs(song_options, system_prompt, user_prompt, num_songs, model="gpt-3.5-turbo", context_size=4097, batch_size=4097):
    # ASSUMPTION: average under 20 tokens per song+artist output
    encoding = tiktoken.encoding_for_model(model)
    available_context = context_size - len(encoding.encode(system_prompt+user_prompt)) - num_songs*20
    batches, running_batch, running_size = [], [], 0
    for song in song_options:
        running_size += len(encoding.encode(song))
        if running_size >= available_context or running_size >= batch_size:
            batches.append(running_batch.copy())
            running_batch = []
            running_size = 0
        else:
            running_batch.append(song)
    batches.append(running_batch)
    return batches

def reduce_batches(batches, system_prompt, user_prompt, num_songs, model="gpt-3.5-turbo", max_depth=3, batch_size=4097):
    num_runs = 0
    while len(batches) > 1 and num_runs<max_depth:
        gpt_response = query_gpt(batches, system_prompt, user_prompt, model=model)
        song_options = []
        for track in gpt_response:
            song_options.append("'" + track["song"] + "'" + " by " + track["artist"])
        batches = batch_songs(song_options, system_prompt, user_prompt, num_songs, model=model, batch_size=batch_size)
        num_runs+=1
    return batches


def query_openai(prompt, num_songs, song_options, model="gpt-3.5-turbo"):
    system_prompt = """You are a helpful assistant. Your job is to recommend songs for a music playlist given a list of song options. If you don't know a song, you can make a guess based on the title and artist, but be more cautious. You will give your response in a JSON format with the following schema: {"playlist": [{"song": String, "artist": String}]}. Do not include any text in your response other than the JSON output."""
    user_prompt = "I want to create a playlist that is: " + prompt + ". Given the following song options (in no particular order, try to consider each song equally), create an appropriate playlist that is " + str(num_songs*2) + " songs long. Song options: "
    openai.api_key = os.getenv("OPENAI_API_KEY")

    batches = batch_songs(song_options, system_prompt, user_prompt, num_songs*2, model, batch_size=500)
    final_batch = reduce_batches(batches, system_prompt, user_prompt, num_songs*2, model, batch_size=500)
    final_songs = query_gpt(final_batch, system_prompt, user_prompt, model)
    if len(final_songs) > num_songs:
        return final_songs[:num_songs], final_songs[num_songs:]
    return final_songs, []
        
    