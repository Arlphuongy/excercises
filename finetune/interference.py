from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


tokenizer = AutoTokenizer.from_pretrained("arlzphuong/zh_to_en")
model = AutoModelForSeq2SeqLM.from_pretrained("arlzphuong/zh_to_en")
# you can try with your own finetuned model


# Translate a sample text to test the model3
src_text = [
    "昨天我和朋友们去了长城，那里的景色非常壮观，我们拍了很多照片。",
    "随着人工智能技术的发展，未来的汽车将能够完全自动驾驶。",
    "教育不仅仅是学习知识，更是关于培养解决问题的能力和发展个人品德。",
    "环保组织呼吁政府采取更有力的措施，以减少工业排放和保护自然环境。",
    "健康饮食和定期运动对维持长期健康至关重要。",
    "北京烤鸭是一道著名的中式菜肴，以其皮脆肉嫩和独特的风味而闻名。",
    "随着时尚界对可持续性的关注增加，越来越多的品牌开始使用环保材料制作衣服。",
]


translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
print([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
