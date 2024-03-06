import openai
import tiktoken
import time
from app.providers.commons import combine_response_options
from app.providers.getSongOptionsBase import GetSongOptionsProvider
from typing import List
from app.providers.types import SongOption

'''
GetSongOptionsProviderGPTImpl

implements the GetSongOptionsProvider base class using GPT as the llm api. 

The general approach: give GPT a list of the user's saved spotify songs and ask
it to choose the top n songs which match the user prompts,
where n is twice the user-specified playlist size. Small note: we ask for
double the number of desired songs to create a list of backups that can be used
if any of the returned songs is not parsable/corrupted.

This implementation makes a few assumptions: 
1. GPT (whichever model is specified, GPT-3.5-Turbo by default) possesses an
    understanding of most popular music and can effectively zero-shot an 
    acceptable playlist from a list of songs given a prompt
2.  GPT is capable of remembering the specified json output format throughout its
    response generation. (I thought this was a long-shot but it actual seems 
    pretty good at this)
3. The average song + artist option scraped from a user's spotify account is
    under 20 tokens. This assumption is used to estimate how large batches should
    be. (more on the batching approach later)

A brief implementation description:
1. We cannot always just include the entire user song library in our prompt
    to GPT because it can easily exceed the context size. Therefore, we must
    batch the library as a series of shorter queries, the responses of which 
    can be recombined and used to query the model again. This process can be 
    repeated until there is only one batch left.
2. The first step, then, is to batch the user library, which is done via
    batch_songs
3. The next step is to query GPT with each batch, recombine get results, 
    and repeat until there is only one batch left (or we exceed batch depth
    limit which can be set as a class instantiation param via 
    `max_batching_depth`). This process is executed in reduce_batches
4. Once there is only one batch of options and GPT chooses its favorites from it,
    a little post-processing is done and the options are returned through the
    get_songs implemented api.

Params:
- model: string - the name of the GPT model to be used
- system_prompt: string - the prompt supplied to GPT dictating system behavior
- user_prompt_template: string - the template string for the user prompt 
    supplied to GPT. ASSUMPTION: it includes 2 string format parameters to 
    interpolate the user prompt and desired number of songs
- openai_api_key: str - the openai api key
- context_size: int - the context size of the model (in tokens)
- batch_size: int - the desired batch size (in tokens)
- max_batching_depth: int - the max number of times batches can be reduced before
    choosing the best songs randomly from all the current candidates.

TODO:
1. improve error handling
2. improve batching peformance through parallelization
3. add input validation, like batch size wrt context size and num songs wrt total songs
'''

class GetSongOptionsProviderGPTImpl(GetSongOptionsProvider):

    def __init__(self, song_choices, model, system_prompt, user_prompt_template, 
                 openai_api_key, context_size=4097, batch_size=4097, 
                 max_batching_depth=3):
        self.song_choices = song_choices
        self.model = model 
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template
        self.openai_api_key = openai_api_key
        self.context_size = context_size
        self.batch_size = batch_size
        self.max_batching_depth = max_batching_depth

    def query_gpt(self, batches: List[List[str]], user_prompt: str) -> List[SongOption]:
        time.sleep(5)
        responses = []
        for batch in batches:
            song_options_stringified = " ,".join(batch)
            try:
                gpt_response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                            {"role": "system", "content": self.system_prompt},
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
        return combine_response_options(responses)
    
    def reduce_batches(self, batches: List[List[str]], user_prompt: str, num_songs: int) -> List[List[str]]:
        num_runs = 0
        while len(batches) > 1 and num_runs<self.max_batching_depth:
            gpt_response = self.query_gpt(batches, user_prompt)
            song_options = []
            for track in gpt_response:
                song_options.append("'" + track["song"] + "'" + " by " + track["artist"])
            batches = self.batch_songs(song_options, user_prompt, num_songs)
            num_runs+=1
        return batches

    def batch_songs(self, song_options: List[str], user_prompt: str, num_songs: int) -> List[List[str]]:
        # ASSUMPTION: average under 20 tokens per song+artist output
        available_context = self.context_size - len(self.encoding.encode(self.system_prompt+user_prompt)) - num_songs*20
        batches, running_batch, running_size = [], [], 0
        for song in song_options:
            running_size += len(self.encoding.encode(song))
            if running_size >= available_context or running_size >= self.batch_size:
                batches.append(running_batch.copy())
                running_batch = []
                running_size = 0
            else:
                running_batch.append(song)
        batches.append(running_batch)
        return batches
    
    def get_songs(self, prompt: str, num_songs: int) -> List[SongOption]:
        user_prompt = self.user_prompt_template.format(prompt, str(num_songs*2))
        openai.api_key = self.openai_api_key
        batches = self.batch_songs(self.song_choices, user_prompt, num_songs*2)
        final_batch = self.reduce_batches(batches, user_prompt, num_songs*2)
        final_songs = self.query_gpt(final_batch, user_prompt)
        if len(final_songs) > num_songs:
            return final_songs[:num_songs], final_songs[num_songs:]
        return final_songs, []

        