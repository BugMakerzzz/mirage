from transformers import AutoTokenizer, AutoModelForCausalLM
from .config import llama3_8b_base_path, llama3_8b_chat_path, llama2_13b_base_path, llama2_13b_chat_path, mistral_7b_base_path, mistral_7b_chat_path, vicuna_13b_base_path, llama3_70b_chat_path, qwq_32b_path, marco_o1_path
from .openai_chat import chat_generate
import torch
import torch.nn.functional as F



class ModelWrapper():

    def __init__(self, model_name, lora_path=None):   
        self.model_name = model_name     
        self.is_llama = model_name.startswith('Llama') 
        self.is_mistral = model_name.startswith('Mistral')
        self.is_gpt = model_name.startswith('gpt')
        self.is_qwq = model_name.startswith('qwq')
        self.is_marco = model_name.startswith('marco')
        self.is_chat = False
        self.is_remote = False
        
        if self.is_llama:
            if '8b' in model_name:
                if 'chat' in model_name:
                    self.is_chat = True
                    path = llama3_8b_chat_path 
                else: 
                    path = llama3_8b_base_path
           
            elif '70b' in model_name:
                self.is_chat = True 
                path = llama3_70b_chat_path
            else:
                if 'chat' in model_name:
                    self.is_chat = True
                    path = llama2_13b_chat_path
                else:
                    path = llama2_13b_base_path
        elif self.is_mistral:
            if 'chat' in model_name:
                self.is_chat = True
                path = mistral_7b_chat_path
            else:
                path = mistral_7b_base_path
        elif self.is_qwq:
            self.is_chat = True
            path = qwq_32b_path
        elif self.is_marco:
            self.is_chat = True
            path = marco_o1_path
        else:
            path = None
        
        if path:
            self.tokenizer = AutoTokenizer.from_pretrained(path, torch_dtype=torch.float16, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16, device_map='auto', trust_remote_code=True)
            if lora_path:
                self.model = self.load_ft_model(lora_path=lora_path)
            self.device = self.model.device
        else:
            self.model = model_name
            self.is_remote = True
            self.is_chat = True
       
    def __call__(self, input_ids, labels=None, return_dict=True, output_attentions=False, output_hidden_states=False):
        if labels:
            outputs = self.model(
                input_ids=input_ids.to(self.device),
                labels=labels.to(self.device),
                return_dict=return_dict,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
        else:
            outputs = self.model(
                input_ids=input_ids.to(self.device),
                return_dict=return_dict,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
        return outputs
    
    
    def generate(self, input, sample_cnt=1):
        if self.is_remote:
            if self.is_gpt or sample_cnt == 1:
                result = chat_generate([input], model=self.model, max_tokens=25000, sample_cnt=sample_cnt)
                print(result)
                response = [result[0][-1]['choices'][i]['message']['content'] for i in range(sample_cnt)]
            else:
                response = []
                for _ in range(sample_cnt):
                    result = chat_generate([input], model=self.model, max_tokens=500, sample_cnt=sample_cnt)
                    res = result[0][-1]['choices'][0]['message']['content']
                    response.append(res)
        else:
            with torch.no_grad():
                self.model.eval()
                if self.is_chat:
                    inputs = self.tokenizer.apply_chat_template(input, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(self.device)
                else:
                    inputs = self.tokenizer(input, return_tensors="pt")["input_ids"].to(self.device)
                response = []
                if sample_cnt == 1:
                    do_sample = False
                else:
                    do_sample = True 
                for _ in range(sample_cnt):
                    outputs = self.model.generate(inputs, max_new_tokens=25000, do_sample=do_sample)
                    res = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
                    if self.is_llama and '8b' in self.model_name:
                        res = res.split('assistant\n')[0]
                    response.append(res)
                
                    
        return response


        
    def get_pred_logits(self, input, output):
        context = self.tokenizer(input + ' '  + output,return_tensors='pt')['input_ids']
        pred_ids = self.tokenizer(output)['input_ids']
        logits = self.model(context.to(self.device))[0].to('cpu')
        # pred_range = range(len(context)-len(pred_ids)-1, len(context)-1)
        logits = F.softmax(logits, dim=-1)
        probs = logits[:,len(context)-len(pred_ids)-1, pred_ids[0]].item()
        return probs


    def get_hidden_states(self, input):
        context = self.tokenizer(input + ' ',return_tensors='pt')['input_ids']
        with torch.no_grad():
            outputs = self.model(
                context.to(self.device),
                output_hidden_states=True
            )
        return outputs['hidden_states']


    # def load_ft_model(self, lora_path):
        # base_model = self.model
        # model = PeftModel.from_pretrained(base_model, lora_path) 
        # return model