# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text2text-generation", model="arlzphuong/mix-zh-en-1.5m")
# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("arlzphuong/mix-zh-en-1.5m")
model = AutoModelForSeq2SeqLM.from_pretrained("arlzphuong/mix-zh-en-1.5m")
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

# src_text = [
#     "The quick brown fox jumps over the lazy dog",
#     "As the sun sets, the gentle breeze carries the scent of freshly bloomed flowers across the serene garden ",
#     "Although she was hesitant at first, the young artist eventually found the courage to showcase her masterpiece at the prestigious art gallery",
#     "If you had told me yesterday that I would be standing here today, I would have thought you were joking. ",
#     "The ancient ruins, hidden deep within the dense jungle, held secrets that had been untouched for centuries. ",
#     "As the waves crashed against the rocky shore, the lighthouse stood tall, guiding lost sailors back to safety. ",
#     "The passionate chef, known for his innovative dishes, surprised his guests with a unique fusion of flavors that left them craving for more.",
# ]

# src_text = [
# "In the heart of the bustling city, a small cafe exuded warmth and charm, drawing in passersby with the aroma of freshly brewed coffee.",
# "Under the starlit sky, a lone figure stood at the edge of the cliff, contemplating the vastness of the universe spread out before them.",
# "Amidst the chaos of the busy marketplace, a street performer captivated the crowd with a mesmerizing display of acrobatics and music.",
# "As the first snowflakes began to fall, children eagerly rushed outside, their laughter filling the crisp winter air with joy and excitement.",
# "Deep in the forest, a hidden waterfall cascaded down moss-covered rocks, creating a tranquil oasis untouched by the outside world."
# ]


translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
print([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
