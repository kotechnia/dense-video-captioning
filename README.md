# PDVC

❏ PDVC의 구조는 다음과 같습니다.
```
📂pdvc
├─ 📂cfgs
├─ 📂data
├─ 📂densevid_eval3
├─ 📂misc
├─ 📂pdvc
├─ 📂video_backbone
├─ 📂visualization
├─ 📄.gitignore
├─ 📄LICENSE
├─ 📄README.md
├─ 📄eval.py
├─ 📄eval_utils.py
├─ 📄prepare_dataset.py
├─ 📄opts.py
├─ 📄requirement.txt
├─ 📄test_and_visualize.sh
└─ 📄train.py
```

❏ 테스트 시스템 사양은 다음과 같습니다.
```
Ubuntu 22.04   
Python 3.8.10 
Torch 1.9.0+cu111 
CUDA 11.1
cuDnn 8.5.0    
```

❏ 사용 라이브러리 및 프로그램입니다.
```
$ pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
$ pip install ffmpeg

$ cd pdvc
$ pip install -r requirement.txt

$ cd pdvc/ops
$ sh make.sh
$ cd -
```

# 실행 방법 (예시)

❏ 훈련 방법입니다.
```
python train.py \
--cfg_path cfgs/dense_video_caption_ko.yml \
--gpu_id 0 1 2 3
```

❏ 평가 방법입니다.
```
python eval.py \ 
--eval_folder dense_video_captioning_korean \
--gpu_id 0 1 2 3  
```
