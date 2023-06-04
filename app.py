from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, VideoUnavailable, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
from transformers import T5ForConditionalGeneration, T5Tokenizer, BartForConditionalGeneration, BartTokenizer, BartConfig
from flask_cors import CORS
import nltk
import json
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)
app.app_context().push()

def get_summary(str1):
    model = BartForConditionalGeneration.from_pretrained(
        "facebook/bart-large-cnn",  output_past=True)
    tokenizer = BartTokenizer.from_pretrained(
        "facebook/bart-large",  output_past=True)
    device = 'cuda'
    nested = nest_sentences(str1)
    input_tokenized = tokenizer.encode(
        ' '.join(nested[0]), truncation=True, return_tensors='pt')
    input_tokenized = input_tokenized.to(device)
    summary_ids = model.to("cuda").generate(
        input_tokenized, length_penalty=3.0, min_length=30, max_length=100)
    output = [tokenizer.decode(g, skip_special_tokens=True,
                               clean_up_tokenization_spaces=False) for g in summary_ids]
    return output

def format_text(document):
    formatter = TextFormatter()
    transcript = formatter.format_transcript(document).replace("\n", ". ")
    return transcript
    


def nest_sentences(document):
    nested = []
    sent = []
    l = 0
    for i in nltk.sent_tokenize(document):
        l += len(i)
        if (l < 1024):
            sent.append(i)
        else:
            nested.append(sent)
            sent = []
            l = 0
    if (sent):
        nested.append(sent)
    return nested


def get_youtube_data(youtube_uri):
    str1 = ""
    try:
        data = (YouTubeTranscriptApi.get_transcript(youtube_uri, languages=["en"]))
        str1 = format_text(data)
    except NoTranscriptAvailable:
        return  json.dumps({"response" : "No Transcript available for following video"})
    except VideoUnavailable:
        return json.dumps({"response" : "Video unavailable"})
    except TranscriptsDisabled:
        return  json.dumps({"response" : "No Transcript available for following video"})
    
    print(get_summary(str1))
    return json.dumps({"response" : get_summary(str1)[0]})


@app.route("/api/summarize", methods=["GET"])
def summarize():
    param = request.args.get("youtube_url")
    youtube_uri_arr = param.split("=")
    youtube_id = youtube_uri_arr[1]
    return (get_youtube_data(youtube_id))


if __name__ == "__main__":
    app.run(debug=True, port=2000)
