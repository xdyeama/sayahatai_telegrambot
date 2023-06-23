import openai
import logging
import config

openai.api_key = config.OPENAI_API_KEY


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return (
            response["choices"][0]["message"]["content"],
            response["usage"]["total_tokens"],
        )
    except Exception as e:
        logging.error(e)
