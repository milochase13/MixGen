CONTEXT_TEMPLATE="""I want you to create a music playlist that is {num_songs} \
songs long and most accurately reflects the following prompt: {{user_input}}. \
Only use the following song options and their corresponding lyrics and composers \
to create this playlist: {{context}}


"""

RESPONSE_SCHEMA=""" You will give your response in a JSON format with the \
following schema: \
{{
"playlist": [{{"song": String, "artist": String}}]
}}

Do not include any text in your response other than the JSON output. \
"""