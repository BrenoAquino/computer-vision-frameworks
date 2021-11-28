# OpenCV GPU

Esse tutorial vai mostrar o caminho das pedras para poder baixar, compilar e instalar o OpenCV compativel com GPU.

## Cuda

Essa primeira etapa explicará como instalar o cuda e o cudnn.

### Install NVidia Driver

Voce pode baixar a ultima versao do seu driver pelo proprio [site da NVidia](https://www.nvidia.com/download/index.aspx?lang=en-us). Se estiver usando o Ubuntu com o _Sofware & Updates_ para admistrar o driver na NVidia, selecione o driver prorpietario da propria NVidia. Se o seu S.O. estiver com uma opcao marcada com "manually" basta rodar no terminal:

```shell
sudo ubuntu-drivers autoinstall
```

Apos essa instalacao basta reiniciar o pc.

```shell
reboot
```

Para visualizar a versao do seu _driver_ e do _CUDA_ basta rodar no terminal:

```shell
nvidia-smi
```

### Install CUDA Toolkit

Agora e preciso instalar o _CUDA Toolkit_. Para isso, basta ir no [site da NVidia](https://developer.nvidia.com/cuda-toolkit-archive) e rodar os comandos informados por ela. A titulo de exemplo, escolhi o ultimo _CUDA Toolkit_ disponivel para Linux > x86_64 > Ubuntu > 20.04 > deb (local). Para esse, precisei rodar:

```shell
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
$ sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ wget https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda-repo-ubuntu2004-11-4-local_11.4.1-470.57.02-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu2004-11-4-local_11.4.1-470.57.02-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-ubuntu2004-11-4-local/7fa2af80.pub
$ sudo apt-get update
$ sudo apt-get -y install cuda
```

### Install cuDNN

> :warning: Versão atualizada: https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html

Com o _driver_ instalado e o _CUDA Toolkit_ tambem, agora precisamos instalar o _cuDNN_. Va ate o [site da NVidia](https://developer.nvidia.com/cudnn-download-survey) e escolha o _cuDNN_ da sua versao do _CUDA_. Baixe o ___cuDNN Library for Linux (x86_64)___, o ___cuDNN Runtime Library for Ubuntu20.04 x86_64___ e ___cuDNN Developer Library for Ubuntu20.04 x86_64___.

Com o ___cuDNN Library for Linux (x86_64)___ voce vai precisar mover os arquivos para onde esta a pagina do _CUDA_. Para saber onde o _CUDA_ esta instalado voce pode rodar no seu terminal:

```shell
$ whereis cuda
```

O resultado desse comendao vai mostrar o path do _CUDA_, um exemplo no meu caso seria: 
```shell
cuda: /usr/local/cuda
```


> :warning: __VOCE DEVE SUBSTITUIR TODOS OS /usr/local/cuda A SEGUIR PELO SEU _PATH___


Agora com o _path_ do _CUDA_ em mao voce vai mover os arquivos do ___cuDNN Library for Linux (x86_64)___ para ele. Voce fara isso por meio dos comandos:

```shell
$ tar -xvzf cudnn-10.1-linux-x64-v7.6.5.32.tgz
$ sudo cp cuda/include/cudnn.h /usr/local/cuda/include/
$ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64/
```

Apos isso e preciso dar permissao para os novos arquivos adicionados

```shell
$ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
```

Agora vamos instalar o ___cuDNN Runtime Library for Ubuntu20.04 x86_64___ e ___cuDNN Developer Library for Ubuntu20.04 x86_64___. Para isso va ate o pacote _.deb_ de cada um deles e instale. Para o _runtime_:

```shell
$ sudo dpkg -i ./cuDNN Runtime\ Library\ for\ Ubuntu20.04\ x86_64
```

e para o _developer_:


```shell
$ sudo dpkg -i ./cuDNN\ Developer\ Library\ for\ Ubuntu20.04\ x86_64
```

Para evitar erros podemos atualizar a veriavel de ambiente com o _path_ das ferramentas.

```shell
$ echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
$ echo 'export LD_LIBRARY_PATH=/usr/local/cuda/include:$LD_LIBRARY_PATH' >> ~/.bashrc
```

Rode novamente o `.bashrc` para carregar a nova variavel de ambiente.

```shell
$ source ~/.bashrc
```

### Possiveis errors

Na minha instalacao ele reclamou que nao achou um `libcusolver.so.10` em `$LD_LIBRARY_PATH`. Para resolver isso voce pode fazer um hard link com o comando:

```shell
$ sudo ln /usr/local/cuda/lib64/libcusolver.so.11 /usr/local/cuda/lib64/libcusolver.so.10
```

## OpenCV

Agora vamos para a instalação do OpenCV. Nesse tutorial irei utilizar um ambiente virtual do python (_virtualenv_) para a instalação do OpenCV. Considere que essa criação do ambiente ja foi feita com o _venv_ e o caminho dele será na raiz do projeto na pasta _.venv_. Assumimos também que já estamos na pasta do projeto.

### Dependencias

Para poder compilar o OpenCV é preciso ter algumas ferramentas instaladas. Muitas delas já vem instaladas em ambientes Linux, mas não custa nada validar se já estão instaladas. Essas são:

```shell
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install build-essential cmake unzip pkg-config
$ sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
$ sudo apt-get install libv4l-dev libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk-3-dev
$ sudo apt-get install libatlas-base-dev gfortran
$ sudo apt-get install python3-dev
```

Além da dependencia de ferramentos no S.O., precisamos instalar o _NumPy_ no nosso ambiente também, para isso:

```shell
$ pip install numpy
```

### Download OpenCV

Agora vamos baixar o código do OpenCV para podermos fazer algumas alterações para utilizar a GPU e compila-lo. Para isso, bastar baixar diretamente do repositório do [OpenCV](https://github.com/opencv/opencv) (nos comandos está com a versão 4.5.4, mas você pode botar a mais atual no momento):

```shell
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.4.zip
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.4.zip
$ unzip opencv.zip
$ unzip opencv_contrib.zip
$ mv opencv-4.2.0 opencv
$ mv opencv_contrib-4.2.0 opencv_contrib
```

### Arquitetura da GPU

Nós precisaremos fornecer o valor que representa a arquitetura da GPU no processo de compilação, para isso, será necessário saber qual é sua GPU.

Caso não saiba qual a sua GPU, bastar ir no terminal e digitar:

```shell
$ nvidia-smi
```

O output será algo semelhante a isso:

```shell
Fri Nov 26 10:35:46 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.00       Driver Version: 510.06       CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:01:00.0  On |                  N/A |
| 10%   55C    P0    49W / 215W |   1059MiB /  8192MiB |     N/A      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

Você pode pegar o nome na linha _NVIDIA GeForce [...]_. Guarde o nome da sua GPU.

Agora para descobrir o número que representa a arquitetura basta acessa o [site da NVidia](https://developer.nvidia.com/cuda-gpus) que lista as GPUs com o seu valor. Basta selecionar o tipo da sua GPU (Tesla, Quadto, GeForce etc) e anotar o valor que estará na coluna _Compute Capability_ da sua GPU.

### Configuração de Build

Agora vamos configurar o OpenCV para poder compilar, para isso, vamo usar o _cmake_. Entre na pasta dos arquivos baixados do _OpenCV_ e crie uma pasta chamada _build_ para concentrar todos os arquivos de compilação. Ou seja:

```shell
$ cd opencv
$ mkdir build
$ cd build
```

Pronto, agora vamos configurar o _build_. É necessário ter atenção em alguns campos:
- _CMAKE_INSTALL_PREFIX_: caminho do _cmake_ instalado
- _CUDNN_INCLUDE_DIR_ : caminho para os arquivos do _cudnn_
- _CUDNN_LIBRARY_: caminho do _.so_ do _cudnn_, o número no final representa a versão (major) do _cudnn_ instalada
- _CUDNN_VERSION_: versão do _cudnn_ instalada
- _CUDA_ARCH_BIN_: valor obtido do _step_ passado que representa sua GPU
- _PYTHON_DEFAULT_EXECUTABLE_: caminho do python a ser utilizado
- _OPENCV_EXTRA_MODULES_PATH_: caminho onde tem os modulos dentro do _opencv_contrib_ baixado
- _OPENCV_PYTHON3_INSTALL_PATH_: caminho onde o OpenCV será instalado para python
- _PYTHON_EXECUTABLE_: caminho do python a ser utilizado

```shell
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local/ \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D WITH_CUDA=ON \
	-D WITH_CUDNN=ON \
	-D OPENCV_DNN_CUDA=ON \
        -D CUDNN_INCLUDE_DIR=/usr/local/cuda/include \
        -D CUDNN_LIBRARY=/usr/local/cuda/lib64/libcudnn.so.8 \
        -D CUDNN_VERSION=8.2.4 \
	-D ENABLE_FAST_MATH=1 \
	-D CUDA_FAST_MATH=1 \
	-D CUDA_ARCH_BIN=7.5 \
        -D BUILD_NEW_PYTHON_SUPPORT=ON \
        -D BUILD_opencv_python3=ON \
        -D HAVE_opencv_python3=ON \
        -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
	-D WITH_CUBLAS=1 \
	-D OPENCV_EXTRA_MODULES_PATH=/home/breno/developer/charles/eyes/opencv-gpu/opencv_contrib/modules \
        -D OPENCV_PYTHON3_INSTALL_PATH=~/developer/charles/eyes/opencv-gpu/.venv/lib/python3.8/site-packages \
	-D HAVE_opencv_python3=ON \
	-D PYTHON_EXECUTABLE=/home/breno/developer/charles/eyes/opencv-gpu/.venv/bin/python \
	-D BUILD_EXAMPLES=ON ..
```

As ultimas linhas indicará se deu certo ou não, lá dirá caso tenha acontecido algum erro e exibirá 2 arquivos de _log_. Ao final, ele também exibirá um resumo da configuração, você precisa verificar se o _cudnn_ está habilitado, se o número da arquitetura está correto (aqui o número é exibido sem o ".") e se o _cuda_ está habilitado tbm. Algo semelhante a:

```shell=
...
--   NVIDIA CUDA:                   YES (ver 11.4, CUFFT CUBLAS FAST_MATH)
--     NVIDIA GPU arch:             75
--     NVIDIA PTX archs:
-- 
--   cuDNN:                         YES (ver 8.2.4)
...
```

Também recomendo checar se todos os caminhos e versões estão certas na seção de Python. Seria algo semelhante a isso, mas com os seus caminhos:

```shell
--   Python 3:
--     Interpreter:                 /home/breno/developer/charles/eyes/opencv-gpu/.venv/bin/python3 (ver 3.8.10)
--     Libraries:                   /usr/lib/x86_64-linux-gnu/libpython3.8.so (ver 3.8.10)
--     numpy:                       /home/breno/developer/charles/eyes/opencv-gpu/.venv/lib/python3.8/site-packages/numpy/core/include (ver 1.21.4)
--     install path:                /home/breno/developer/charles/eyes/opencv-gpu/.venv/bin/python3
```

# Compilação e Instalação

Agora vamos compilar o OpenCV. Para isso, podemos passara como parametro a quatidade de núcleos do processador, para agilizar o processo. Caso você não saiba, basta executar:

```shell
$ nproc
```

O número exibido será a quantidade de núcleos que você tem disponivel. Agora vamos compilar. O número após o _j_ deve ser o número de núclos que você possui, no meu caso, 6 (esse processo leva um tempo):

```shell
$ make -j6
```

Agora com tudo compilado, basta instlar com:

```shell
$ sudo make install
$ sudo ldconfig
```

Por ultimo, agora vamos criar um link para o ambiente python:

```shell=
ln -s ~/developer/charles/eyes/opencv-gpu/.venv/lib/python3.8/site-packages/cv2/python-3.8/cv2.cpython-35m-x86_64-linux-gnu.so ~/developer/charles/eyes/opencv-gpu/.venv/lib/python3.8/site-packages/cv2.so
```

Pronto, OpenCV com suporte a GPU instalado.

### Verificação

Você pode verificar a versão com:

```python
>>> import cv2
>>> cv2.__version__
```

e obter as configurações de _build_:

```python
>>> import cv2
>>> print(cv2.getBuildInformation())
```

### Possiveis errors

Na minha instalacao ele reclamou que nao achou um `libcudnn` em `$LD_LIBRARY_PATH`. Para resolver isso eu tive que procurar ele com o:

```shell
$ sudo find /usr/ -name "*libcudnn*"
```

e criei um _link_ e _$LD_LIBRARY_PATH_ 

```shell
$ sudo ln /path/to/libcusolver.so.8 /usr/local/cuda/lib64/libcudnn.so
```

## Referências:
- [How to use OpenCV’s “dnn” module with NVIDIA GPUs, CUDA, and cuDNN](https://www.pyimagesearch.com/2020/02/03/how-to-use-opencvs-dnn-module-with-nvidia-gpus-cuda-and-cudnn)
- [How to install Cuda 11.4 + Cudnn 8.2 + OpenCV 4.5 on Ubuntu 20.04](https://medium.com/@pydoni/how-to-install-cuda-11-4-cudnn-8-2-opencv-4-5-on-ubuntu-20-04-65c4aa415a7b)
