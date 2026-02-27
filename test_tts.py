import asyncio
import os
from elevenlabs.client import AsyncElevenLabs

ELEVENLABS_API_KEY = "sk_467f4eb142b2bc8893dc90d22ecd90ceac2a9fb37a61a67e"

async def test_tts():
    client = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)
    try:
        print("Testing ElevenLabs convert...")
        audio_stream = client.text_to_speech.convert(
            text="Hello, this is a test.",
            voice_id="21m00Tcm4TlvDq8ikWAM",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        print("Got stream! Reading chunks...")
        count = 0
        async for chunk in audio_stream:
            count += 1
            if count == 1:
                print("Successfully received first audio chunk!")
        print("Done.")
    except Exception as e:
        print(f"Exception exactly: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_tts())
