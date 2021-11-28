# TensorFlow Object Detection API

Esse guia tem como objetivo explicar como funiona a configuração do TensorFlow Object Detection (que será referenciado como TFOD nesse guia para criar redes customizadas utilizando transferencia de aprendizagem, ou seja, utilizado redes já consolidadas e amplamente testadas na comunidade.

Para todo esse guia será utilizado um ambiente virtual gerado pelo [venv](https://docs.python.org/3/library/venv.html) e nomeado de __tfod_env__.

## Instalação

Nessa seção será aborado a instalação do proprio TFOD como também uma ferramenta utilizada para categorizar as imagens (_labelImg_).

### Configuração do Tensorflow Object Dectection

O TFOD é fornecido em um repositório do próprio tensorflow: [TensorFlow Model Garden](https://github.com/tensorflow/models). As APIs aqui fornecidas ainda precisam ser compiladas. Para isso, vamos usar uma ferramenta chamada [Protoc](https://github.com/protocolbuffers/protobuf).

#### Protoc

Para configurar utilizar o _protoc_ basta ir na página de [releases](https://github.com/protocolbuffers/protobuf/releases) e baixar o correspondente ao do seu sistema operacional. Após o download basta descompactar e deixar a pastar na raiz do projeto. Futuramente usaremos o o arquivo `protoc/bin/protoc` para compilar o pacote.

A estrutura deve está parecida com:
```
project_name/
└─ protoc/
   ├─ bin/
   ├─ include/
   └─ readme.txt
└─ tfod_env/
   ├─ bin/
   ├─ include/
   └── …
```

> OBS: Pode ser necessário dar permissão para executar o `protoc/bin/protoc`

#### TensorFlow Model Garden

Com _protoc_ configurado podemos seguir para baixar o repositório contendo o TFOD. Você pode cloar o [repositório](https://github.com/tensorflow/models) ou baixar o código mesmo, ambos os caminhos chegam no mesmo resultado.

Com o projeto em mãos, nossa estrutura de pastas deve se assemelhar algo assim:

```
project_name/
└─ protoc/
   ├─ bin/
   ├─ include/
   └─ readme.txt
└─ tfod_env/
   ├─ bin/
   ├─ include/
   └── …
└─ models/
   ├─ community/
   ├─ official/
   ├─ orbit/
   └── …
```

Podemos encontrar o TFOD no seguinte path: `models/research/object_detection`. Agora podemos compilar o pacote, mas é preciso estar na pastar `research` para isso. Agora basta executar:
```shell
cd models/research && ../../protoc/bin/protoc object_detection/protos/*.proto --python_out=.
```

> Esse comando não gera nenhum _output_ no terminal

Para evitar algum erro na instalação do TFOD, vamos já instalar o Tensorflow antes.
```shell
pip install tensorflow==2.6.0
```

Após compilar nós precisamos instalar o pacote. Para isso é necessário que estejamos na pastar `research`, logo:
```shell
cd models/research
cp object_detection/packages/tf2/setup.py .
pip install .
```

Para validar a instalação execute;
```shell
python models/research/object_detection/builders/model_builder_tf2_test.py
```

Se aparecer `OK (skipped=1)` no final tudo foi instalado corretamente.

### Configuração do labelImg

Existe um projeto construindo com python e qt que auxilia na criação do dataset. Ele recebe de entrada as imagens e permite você criar as caixas para definir onde estão os elementos a serem reconhecidos e o que são em cada imagem. Ele retorna um xml que converteremos depois para um _input_ reconhecido pelo Tensorflow (_.record_).

Para executar esse projeto é necessário alguns pacotes.
```shell
pip install pyqt5 lxml
```

Para obter o projeto você pode acessar o [repositório](https://github.com/tzutalin/labelImg) para clonar ou baixar o código.

Com o projeto em mãos, vamos configura-lo. Para isso entre na pasta de onde baixou e execute:
```shell
make qt5py3
```

Após isso bastar rodar:
```shell
python labelImg.py
```

> Esse programa não é fundamental para rodar alguma aplicação do TFOD, por conta disso eu não vou representar ele na estrutura de pastas.

## Criando Dataset

Para a contrução do nosso modelo será criado uma nova pastas chamada `workspace` que irá conter todas as informações pertinentes ao nosso modelo.

Já com essa mentalidade, vamos criar uma pasta dentro de `workspace` com o nome de `dataset` para guardar os arquivos que serão utilizados para treinamento e avaliação do nosso modelo. Dentro de _dataset_ ainda haverá uma outra pasta chamda `raw` que irá conter as imagens classificadas para teste e treinamento, ou seja, os _xml_. Atualizando noss estrutura:

```
project_name/
└─ protoc/
   ├─ bin/
   ├─ include/
   └─ readme.txt
└─ tfod_env/
   ├─ bin/
   ├─ include/
   └── …
└─ models/
   ├─ community/
   ├─ official/
   ├─ orbit/
   └── …
└─ workspace/
   └─ dataset/
      └─ raw/
         └─ train
            └─ <aquivos .xml>
         └─ test
            └─ <aquivos .xml>
```

> Como não vamos mais mexer nas pastas fora de workspace, não irei mais representalas nos diagramas.

Além de converter as imagens que estão em xml com suas _tags_ é preciso criar um arquivo _.pbtxt_ contendo as _labels_ que o nosso modelo irá tentar encontrar. __As _labels_ nesse arquivo precisão estar escritas da mesma forma que estão escritas as _tags_ no _xml_ nas imagems.__ Esse arquivo contem o _label_ com um _id_. Exemplo de aquivo:

```txt
item { 
    name:'ThumbsUp'
    id:1
}
item { 
    name:'ThumbsDown'
    id:2
}
```

Considerando que os arquivos ainda estão em xml gerados pelo _labelImg_, por exemplo, é preciso convertelos em _.record_. Para isso, vamos utilizar um script feito pelo [Nicholas Renotte](https://github.com/nicknochnack). Basta baixar ou clonar o [repositório](https://github.com/nicknochnack/GenerateTFRecord) com o script e colocalo na pasta `scripts`.

```
.
.
.
└─ workspace/
   └─ scripts
      └─ generate_tfrecord.py
   └─ dataset/
      └─ raw/
         └─ train
            └─ <aquivos .xml>
         └─ test
            └─ <aquivos .xml>
```

Com o script em mãos, basta executar:
```shell
python scripts/generate_tfrecord.py -x dataset/raw/train -l dataset/label_map.pbtxt -o dataset/train.record
python scripts/generate_tfrecord.py -x dataset/raw/test -l dataset/label_map.pbtxt -o dataset/test.record
```

Pronto, com isso criamos nosso _dataset_ de treino e de teste.

## Preparando Modelo Pretreinado

Para que reinventar a roda? O repositório TensorFlow Model Garden contem um [arquivo em _markdown_](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md) com uma analise de alguns modelos já amplamente utilizado. Você pode estudar mais e analisar os parametros para identificar a melhor rede para sua aplicação. Vale lembrar que para calcular a estimativa de frequencia de atualização de cada rede basta fazer:

```
                                          1
Frequencia de Atualização = ──────────────────────────────
                            Tempo gasto para processamento
```

Após baixar uma rede coloque-a no seu `workscape`, ficando:

```
.
.
.
└─ workspace/
   └─ scripts
      └─ ...
   └─ dataset/
      └─ ...
   └─ pre_trained_model/
      └─ <model name>
         ├─ checkpoint/
            └─ ... 
         ├─ save_model/
            └─ ... 
         └─ pipeline.config
```

O principal arquivo é o _pipeline.config_, pois é nele que iremos fazer o nosso _fine tunning_, ou seja, ele possui toda a configurações do modelo, do treinamento e da validação. Aqui que vamos ajustar alguns parametros para utilizar a rede para sua aplicação.

### pipeline.config

Esse arquivo merece uma seção dedicada a ele, mas infelizmente ainda não sou profundo conhecedor dos parametros desse aquivo. Irei citar primeiro os parametros que são fundamentais para poder rodar a rede.

Copie o arquivo e cole em uma pasta `model` no workspace, essa pasta irá conter o nosso modelo. Dentro dela, já podemos criar uma outra pasta `checkpoint` para guardar o progresso da nossa rede. A estrutura fica assim:

```
.
.
.
└─ workspace/
   └─ scripts
      └─ ...
   └─ dataset/
      └─ ...
   └─ pre_trained_model/
      └─ ...
   └─ model
      ├─ checkpoint/
      └─ pipeline.config
```

1. Classes Number `model.ssd.num_classes`: o número de _labels_ que a sua aplicação tem
1. Train Batch Size `train_config.batch_size`: tamanho do batch que será utilizado no treinamento
1. Checkpoint `train_config.fine_tune_checkpoint`: caminho dos _checkpoints_ do modelo pre treinado para ter um ponto de partida
1. Task `train_config.fine_tune_checkpoint_type`: tarefa que será executada pela rede (`detection` para detecção de objetos)
1. Train Label `train_input_reader.label_map_path`: caminho do arquivo .pbtxt com as labels do modelo
1. Train Input `train_input_reader.tf_record_input_reader.input_path[]`: caminho para o arquivo _.record_ para treinar o modelo
1. Label para Teste `eval_input_configs[].label_map_path`: caminho do arquivo .pbtxt com as labels do modelo
1. Test Input `eval_input_configs[].tf_record_input_reader.input_path[]`: caminho para o arquivo _.record_ para avaliar o modelo

## Treinamento e Validação

Agora com tudo em ordem, basta treinar o modelo. Vamos guardar nosso modelo em uma pasta chamada `model` e em `checkpoint`. Para treinar utilizamos um script em python também do TFOD. O comando fica (considerando a raiz do projeto):

```shell
python models/research/object_detection/model_main_tf2.py --model_dir=workspace/model/checkpoint --pipeline_config_path=workspace/model/pipeline.config --num_train_steps=2000
```

E para rodar a validação:
```shell
python models/research/object_detection/model_main_tf2.py --model_dir=workspace/model/checkpoint --pipeline_config_path=workspace/model/pipeline.config --checkpoint_dir=workspace/model/checkpoint
```