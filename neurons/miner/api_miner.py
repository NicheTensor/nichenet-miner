import requests

class APIMiner:
    def __init__(self, url, model_name, prompting = None):
        self.url = url
        self.model_name = model_name

        if prompting == None:
            self.prompting = {
                "prefix":"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.",
                "assistant_start":'\nASSISTANT:',
                "assistant_end":'</s>',

                "user_start":'\nUSER: ',
                "user_end":'',
                }
        else:
            self.prompting=prompting

    
    def quick_generate(self, prompt, max_tokens = 1000, timeout=30):
      prompt = "<prefix><user_start>"+prompt+"<assistant_start>"
      prompt = self.replace_keywords(prompt)
      return self.generate_text(prompt, max_tokens=max_tokens, temperature=0.7, timeout=timeout)
    

    def replace_keywords(self,prompt):

        prompt = prompt.replace("<prefix>",self.prompting["prefix"])

        prompt = prompt.replace("<assistant_start>",self.prompting["assistant_start"])
        prompt = prompt.replace("<assistant_end>",self.prompting["assistant_end"])

        prompt = prompt.replace("<user_start>",self.prompting["user_start"])
        prompt = prompt.replace("<user_end>",self.prompting["user_end"])

        return prompt
    
    def generate_text(self, input_text, max_tokens=100, temperature = 0.0, timeout=30):

        return self.call_endpoint(input_text, max_tokens,temperature=temperature, timeout=timeout)[0]
    

    def call_endpoint(self, prompt, max_tokens, temperature, n=1, timeout=30):

        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n":n,
            "stop":self.prompting["user_start"],
        }
        
        response = requests.post(self.url, headers={'Content-Type': 'application/json'}, json=data, timeout=timeout)
        generations = []
        if response.json().get("choices"):
            for d in response.json()["choices"]:
                generations.append(d["text"])

        return generations