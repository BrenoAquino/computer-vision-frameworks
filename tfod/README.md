# Overview

Esse projeto implementa alguns _scripts_ para facilitar a configuração de um projeto usando TensorFlow Object Detection API (TFOD). A explicação detalhada das etas está em [tfod.md](tfod.md).

Existem 4 _scripts_ responsaveis pela configuração do projeto

> :warning: É recomendado utilizar um ambiente virtual, como o _virtualenv_.

> :warning: É necessario estar na pastar dos `scripts` para executa-los

1. [`tfod/setup_project.py`](setup_project.py)
    - Esse _script_ executa todos os outros na ordem necessária, ou seja, basta rodar ele que configurará o projeto como um todo com o TFOD. Existe a possibilidade de pular algumas etapas, caso queira
1. [`tfod/setup_folders.py`](setup_folders.py)
    - Esse _script_ cria as pastas padrões do projeto
```
└─ workspace/
    └─ dataset/
    └─ pre_trained_models/
    └─ custom_model/
```
1. [`tfod/setup_protoc.py`](setup_protoc.py)
    - Esse _script_ baixa e configura o [_protoc_](https://github.com/protocolbuffers/protobuf) que será utilizado para compilar o TFOD
1. [`tfod/setup_tfod.py`](setup_tfod.py)
    - Esse _script_ baixa e instala o TFOD do [repositório](https://github.com/tensorflow/models) de modelos do TensorFlow
1. [`tfod/setup_label_img.py`](setup_label_img.py)
    - Esse _script_ baixa e instala o [LabelImg](https://github.com/tzutalin/labelImg), ferramenta utilizada para classificar imagens para utilizar como treinamento ou validação do modelo

Existe também um _script_ auxiliar que ajuda a converter as imagens com os aquivos _xml_ das posições dos objetos em um arquivo _trecord_ utilizado pelo TensorFlow para treinar ou validar o modelo.

1. [`tfod/xml_to_tf_record.py`](xml_to_tf_record.py)
    - Esse _script_ transforma imagens com as _tags_ de _xml_ para _tfrecord_ (extensão utilizada pelo TensorFlow)
        - Autor [Nicholas Renotte](https://github.com/nicknochnack) e [Repositório](https://github.com/nicknochnack/GenerateTFRecord)
