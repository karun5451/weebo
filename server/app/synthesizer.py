import os
import subprocess
import boto3

from gtts import gTTS
from contextlib import closing
from time import sleep

from .settings import global_lang, speech_service, aws_voice_id, aws_speech_sample_rate, tmp_speech_file

def aws_ssml_processing(text, whisper):
    if(whisper):
        text = '<speak><amazon:effect name="whispered">' + text + '</amazon:effect></speak>'
    else:
        text = '<speak><prosody pitch="high">' + text + '</prosody></speak>'
    return text

def amazon_aws_request(text):
    client = boto3.client(
        'polly',
        region_name='eu-west-1'
    )

    response = client.synthesize_speech(
        Text=text,
        VoiceId=aws_voice_id,
        OutputFormat="mp3",
        SampleRate=str(aws_speech_sample_rate),
        TextType="ssml"
    )

    if os.path.isfile(tmp_speech_file):
        os.remove(tmp_speech_file)

    # url = generate_presigned_url(client, )
    if("AudioStream" in response):
        with closing(response["AudioStream"]) as stream:
            try:
                with open(tmp_speech_file, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # print(error)
                pass
    return tmp_speech_file

def synthesize(text, whisper):
    if text:
        try:
            if(speech_service == "google"):
                tts = gTTS(text=text, lang=global_lang, slow=False)
                tts.save(tmp_speech_file)
                return tmp_speech_file
            elif(speech_service == "amazon"):
                processed_text = aws_ssml_processing(text, whisper)
                return amazon_aws_request(processed_text)
        except Exception as e:
            print("*** EXCEPTION *** (" + str(e) + ")")

def i_am_weebo():
    subprocess.Popen(["aplay", "app/audio/weebo/i_am_weebo.wav"])
    sleep(1.25)
