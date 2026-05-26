import os
import time

from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

MAX_RETRIES = 5


def generate_text(prompt):

    for attempt in range(MAX_RETRIES):

        try:

            response = client.chat.complete(

                model="mistral-small-latest",

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                temperature=0,

                max_tokens=8192,
            )

            return response.choices[0].message.content

        except SDKError as e:

            error_text = str(e)

            if "429" in error_text:

                wait_time = 2 ** attempt

                print(
                    f"Rate limit hit. "
                    f"Retrying in {wait_time}s..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise Exception(
        "Maximum retry attempts exceeded."
    )