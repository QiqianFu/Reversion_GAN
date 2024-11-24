import torch
import clip
from PIL import Image

# 加载CLIP模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)
sum = 0
for i in range(4):
    image_path = "/u/fu1/ece449/Reversion_GAN/on_with_GAN_and_L_try_4/inference/cat <R> table/samples/000"+str(i)+'.png'
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    text = "cat and table"  # 替换为你的输入字符串
    text_tokens = clip.tokenize([text]).to(device)

    # 计算特征
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_tokens)

    # 归一化特征
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # 计算相似性分数
    similarity = (image_features @ text_features.T).item()

    print(f"Similarity score: {similarity:.4f}")
    sum+=similarity
    
print("avg:", sum/4)