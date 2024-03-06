MODEL="gpt-3.5-turbo"
SYSTEM_PROMPT="""You are a helpful assistant. Your job is to recommend songs \
for a music playlist given a list of song options. If you don't know a \
song, you can make a guess based on the title and artist, but be more \
cautious. You will give your response in a JSON format with the following \
schema: {"playlist": [{"song": String, "artist": String}]}. Do not include \
any text in your response other than the JSON output."""
USER_PROMPT_TEMPLATE="""I want to create a playlist that is: {}. Given the \
following song options (in no particular order, try to consider each song \
equally), create an appropriate playlist that is {} songs with your very \
best picks towards the beginning. Song options: """
BATCH_SIZE=1000
MAX_BATCHING_DEPTH=3