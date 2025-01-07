import os
import openai
from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
openai.api_key = "[redacted]"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import json
import random 
random.seed(42)

from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_demo_image(image_size,device):
    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')   

    w,h = raw_image.size
    display(raw_image.resize((w//5,h//5)))
    
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image

    from models.blip import blip_decoder
def load_demo_image(image_size,device):
    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')   

    w,h = raw_image.size
    display(raw_image.resize((w//5,h//5)))
    
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image

image_size = 480
image = load_demo_image(image_size=image_size, device=device)

model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'
    
BLIPCAP = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
BLIPCAP.eval()
BLIPCAP = BLIPCAP.to(device)

# with torch.no_grad():
#     # beam search
#     caption = model.generate(image, sample=False, num_beams=3, max_length=20, min_length=5) 
#     # nucleus sampling
#     # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
#     print(caption[0])

from models.blip_vqa import blip_vqa

image_size = 480
image = load_demo_image(image_size=image_size, device=device)     

model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth'
    
BLIPVQA = blip_vqa(pretrained=model_url, image_size=image_size, vit='base')
BLIPVQA.eval()
BLIPVQA = BLIPVQA.to(device)

# question = 'where is the woman sitting?'

# with torch.no_grad():
#     answer = model(image, question, train=False, inference='generate') 
#     print('answer: '+answer[0])

def VAVI (image, question):
  #call BLIP
  #call gpt3
  #parse gpt3 output to get answer 
  with torch.no_grad():
    # beam search
    #caption = BLIPCAP.generate(image, sample=False, num_beams=3, max_length=20, min_length=5) 
    # nucleus sampling
    image = Image.open(image).convert('RGB')
    w,h = image.size    
    transform = transforms.Compose([
       transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(image).unsqueeze(0).to(device)   
    caption = BLIPCAP.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
    question_nochoices = question.split("\na.")[0]
    prompt_GPT3 = ("I see " + caption[0] + " ."
                   "Generate questions about visual features that we would need to know the answers to to answer " 
                   + question_nochoices + "\nDo not ask non-sight questions.\n\n-")
    generate_questions = openai.Completion.create(model="text-davinci-003", prompt=prompt_GPT3, temperature=0.7, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)
    #print(generate_questions)
    questions = generate_questions["choices"][0]["text"].strip().split("\n")
    answers = []
    for q in questions:
        q = q.strip("-").replace("-", "")
        answer = BLIPVQA(image, q, train=False, inference='generate')[0]
        print(answer, "BLIPVQA ANSWER")
        answers.append(answer)
    qa_pairs = [f"Q: {question.strip('-')}\nA: {answer}" for question, answer in zip(questions,answers)]
    qa_pairs_str = "\n".join(qa_pairs)
    caption = BLIPCAP.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
    example = "I see a photo of a person on a beach playing volleyball. I ask the following questions about it and received the following answers:\n\nQ: What color is the ball?\nA: Blue and yellow\nQ: How many people are there?\nA: Five people.\n\nWhy is one of the people raising their hands?\na. They are giving someone a high-five.\nb. They are spiking the ball.\nc. They are drinking wine.\nd. They are cheering on their teammates.\nAnswer: High-fiving only requires one hand, so the answer is not a. Similarly, spiking the ball requires only one hand, so the answer is not b. Drinking wine is not typically done in the middle of a volleyball game, so the answer is not c. Cheering on teammates could require both hands, so the most plausible answer is d. Final answer: d"
    example2 = "I see a photo of a glass of waater with ice cubes in it. I ask the following questions about it and received the following answers:\n\nQ: How full is the glass?\nA: The glass is half full.\nQ: Does the glass of water have a straw?\nA: No, the glass of water does not have a straw.\n\nWhy is the outside of the glass wet?\na. The light causes it to get wet \nb. The ice water cools the glass, causing moisture in the air to condense onto the outer surface. \nc. The glass is in the middle of the ccean.\nd. The water is spilling over the glass.\nAnswer: Shining light on an object does not make it wet, so the answer is not a. A glass in the middle of the ocean is unlikely to be photographed, so the answer is not c. The glass is not stated to be spilling over, so the answer is not d. Water vapor does indeed condense onto cold surfaces, so the best answer is b. Final answer: b"
    result = f"{example}\n\n{example2}\n\nI see a photo of {caption[0]}. I asked the following questions about it and received the following answers:\n\n{qa_pairs_str}\n\n{question}\nAnswer: "
    print("result: " + result)
    output = openai.Completion.create(model="text-davinci-003", prompt=result, temperature=0.7, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0)
    ans = output["choices"][0]["text"]
    print (ans, "model_ans")
    return output["choices"][0]["text"]

  

def tokens2sent(tokens, objects):
  out_tokens = []
  for token in tokens:
        if type(token) == str:
          out_tokens.append(token)
        elif type(token) == list:
          if len(tokens) == 1:
              out_tokens.append(objects[tokens[0]])
              continue 
          x = int(token[0])
          commaList = ",".join([objects[x]])
          #for token in tokens[:-1]
          out_tokens.append(f"{commaList}")
          #, and {objects[token[-1]]}
  #print(out_tokens)
  return out_tokens

def checkAnswers(answer, question, image):
  print("abcd"[int(answer)], "printans") 
  x = VAVI(image, question).strip().split("answer: ")[-1][0]
  print (x, "VAVI OUTPUT")
  return x == "abcd"[int(answer)]

with open("val.jsonl") as testfile:
  counter = 0
  size = 1000
  data = testfile.readlines() 
  data = random.sample(data, size)
  #print (data)
  questions = []
  for datum in data:
    datum = json.loads(datum)
    #print(datum)
    #print(datum.keys())
    tokens = datum["question"]
    objects = datum["objects"]
    img_fn = datum["img_fn"]
    answer = datum["answer_label"]
    choices = datum["answer_choices"]
    question_tokens = tokens2sent(tokens, objects)
    choice_ids = "abcd"
    choices = [choice_ids[i] + ". " + " ".join(tokens2sent(answer_choice, objects)) for i, answer_choice in enumerate(choices)]
    choices = [choice.replace(" ,", ",").replace(" .", ".").replace(" ' ", "'").replace(" ?", "?").replace(" !", "!") for choice in choices]
    print(choices, "choices")
    question = " ".join(question_tokens)
    image = f"/content/vcr1/vcr1images/{img_fn}"
    question = " ".join(question_tokens) + "\n" + "\n".join(choices)
    question = question.replace(" ,", ",").replace(" .", ".").replace(" ' ", "'").replace(" ?", "?").replace(" !", "!")
    questions.append(question)
    counter += checkAnswers(answer, question, image)
    print(question, "question")
    #for image, question, answer in zip(images, questions, answer):
    
accuracy = counter/size
print(accuracy)
