# CThru — Sign Language Recognition

## About

Sign Language detector a part of Cthru made by Me(Araadh{ Araadh Singh on slack }) is a machine learning pipeling which uses some custom dataset(custom collected samples) 
and mostly the letters are from a dataset from Kaggle (https://www.kaggle.com/datasets/grassknoted/asl-alphabet?resource=download) which has positions of hand In american sign
language letters in varying angles and positions and lightings for the machine to learn better and I have made the front end too so u guys can u se it too(https://cthru.vercel.app/)


---

## How It Works

The file Recognize_words.py collects webcam data normalizes the data relative to the wrist position and then the model predicts what the letter could be and presents it as text


Webcam → MediaPipe → Hand Landmarks → ML Model → Sign → Text

---



### Dataset Samples

### A
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/64d6594d-5633-4348-8517-93f29796b04f" />


### B
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/eb717e46-7b7d-44bd-bfa2-54b28ffe5183" />


### C
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/244d98db-ce8f-4eac-a232-d0e25bb44ee2" />


### D
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/bc97ab94-4cfb-4a67-a375-5d95a8f297f0" />

### E
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e18c9fd6-da3d-4b61-86df-dac5825aff2f" />

### F
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/be725940-8e18-48f0-8938-96d6370b1ad5" />

### G
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/cd6c353e-dbd9-4eb8-ac80-43b8f10bdec2" />

### H
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/428a8cbb-9a59-4209-ab97-f8e2e926f3c3" />

### I
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/6d6b3c93-a4c9-4921-8b8b-e6c4cfe84851" />

### J
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/139975a4-7c9b-4995-b93b-8c1c5242ca4d" />

### K
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e6fd2b2f-3a82-4d93-8b46-c0deecac5aba" />
### L
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/1efea42d-8768-4fb7-8b7d-b4dbd7b3a1f6" />

### M
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/269f89ff-5f8e-4c79-80e5-37a68caa5e4a" />

### N
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/7ed7fd9f-c36a-44a2-a2d0-a9facce5be1a" />

### O
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/0f8384f3-6ad7-4d1c-bae1-c3771dda34fd" />

### P
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/34d5a3d5-6042-49f2-9d3c-ef7d6a6d7194" />

### Q
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/64505ef8-bd34-44e9-b650-63a18334926f" />

### R
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/ca3ff729-fa0c-426c-9d4b-167c7716b052" />

### S
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/86605be2-9c56-4c24-8ed3-a9a9d79e15f9" />

### T
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/0ad35d2d-5a9f-4175-b2bf-35d6f66dd954" />

### U
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/31c40b09-4a42-4b93-ae02-5909d75f33b7" />

### V
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/d436baf4-c5e9-4300-9222-cfb4ce6f17c5" />

### W
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/fa15b7dc-7e0b-410b-8402-beda91514272" />

### X
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/9412bcfe-2b5e-45c5-b47c-bd09aa11de21" />

### Y
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/4373f064-85d3-4be9-90b8-0b11f650602f" />

### Z
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/cf6f8bd4-32c8-41fa-a6a2-29cb333aa290" />

---

## Model

**Model:** model_webcam.pkl

**Accuracy:** 98.56

---

## Website

The frontend was made using HTML, CSS and JavaScript.

**Live:** https://cthru.vercel.app/

<img width="1886" height="957" alt="image" src="https://github.com/user-attachments/assets/a04db455-9471-4df1-8065-1e15ac8f736e" />

---

## Technologies

- Python
- OpenCV
- MediaPipe
- scikit-learn
- FastAPI
- HTML
- CSS
- JavaScript

---

## Project Structure

```text
frontend/
models/
dataset/
backend.py
train_webcam_model.py
