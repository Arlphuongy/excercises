from transformers import AutoModel, AutoTokenizer

huggingface_model_name = "arlzphuong/mix-zh-en-500k"
hf_model = AutoModel.from_pretrained(huggingface_model_name)
hf_tokenizer = AutoTokenizer.from_pretrained(huggingface_model_name)

local_model_path = r"C:\Users\ASUS\Desktop\Practice\util\weights\zh-en-1m"
local_model = AutoModel.from_pretrained(local_model_path)
local_tokenizer = AutoTokenizer.from_pretrained(local_model_path)

def average_models(model1, model2):
    model1_state_dict = model1.state_dict()
    model2_state_dict = model2.state_dict()

    for key in model1_state_dict.keys():
        model1_state_dict[key] = (model1_state_dict[key] + model2_state_dict[key]) / 2

    return model1_state_dict

combined_model_state_dict = average_models(hf_model, local_model)

combined_model = AutoModel.from_config(hf_model.config)
combined_model.load_state_dict(combined_model_state_dict)

save_path = "finetune/mix-zh-en-1.5m"
combined_model.save_pretrained(save_path)
hf_tokenizer.save_pretrained(save_path)  
