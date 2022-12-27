# PDVC

❏ PDVC의 구조는 다음과 같습니다.
```
📂pdvc
├─ 📂cfgs
│   ├─ 📄anet_tsp_pdvc.yml
│   ├─ 📄anet_tsp_pdvc_gt.yml
│   ├─ 📄anet_tsp_pdvcl.yml
│   ├─ 📄yc2_tsn_pdvc.yml
├─ 📂data
│   ├─ 📂anet
│   │   ├─ 📂captiondata
│   │   └─ 📄vocabulary_activitynet.json
│   └─ 📄video_dataset.py
├─ 📂densevid_eval3
│   └─ 📄eval_dvc.py
├─ 📂misc
├─ 📂pdvc
│   └─ 📂ops
│       └─ 📄make.sh
├─ 📂video_backbone
│   └─ 📂TSP
├─ 📂visualization
│   └─ 📂videos
├─ 📄.gitignore
├─ 📄LICENSE
├─ 📄README.md
├─ 📄eval.py
├─ 📄eval_utils.py
├─ 📄opts.py
├─ 📄requirement.txt
├─ 📄test_and_visualize.sh
└─ 📄train.py
```

❏ 테스트 시스템 사양은 다음과 같습니다.
```
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
--cfg_path <CFG_PATH> \
--gpu_id <int>
```

❏ 평가 방법입니다.
```
python eval.py \
--eval_folder <EVAL_FOLDER> \
--eval_transformer_input_type queries \
--gpu_id <GPU_ID>
```
