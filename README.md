# Bird sound recognition using cnn
## Downloading the data
To download the data i used [xeno.canto.org](xeno-canto.org) api where you can find bird recordings from all over the world. I used 10 species which had the most recordings recorded in Poland (to avoid problems with regional differences):
1. Parus major              (bogatka) - 266
2. Emberiza citrinella      (trznadel) - 250
3. Sylvia atricapilla       (kapturka) - 232
4. Fringilla coelebs        (zięba) - 230
5. Phylloscopus collybita   (pierwiosnek) - 224
6. Turdus philomelos        (śpiewak) - 212
7. Periparus ater           (sosnówka) - 176
8. Erithacus rubecula       (rudzik) - 176
9. Turdus merula            (kos) - 163
10. Aegolius funereus       (włochatka) - 158

## Preprocessing
### Segmenting and splitting
First i cut every file into 5 second chunks and split them across the training, validation and test dataset making sure classes were evenly represented but chunks of one recording were not present in different datasets
### Augmentation
I doubled the dataset by applying these augmentation techniques randomly to every audio file:

1. Add Gaussian noise

![](https://i.postimg.cc/XNQ97TgL/Aegolius-funereus-28-0.jpg)

![](https://i.postimg.cc/mgQDh9s4/Aegolius-funereus-28-0-aug.jpg)

2. Add short noises

![](https://i.postimg.cc/cCCyYr5X/Aegolius-funereus-156-24.jpg)

![](https://i.postimg.cc/PfVkHQPc/Aegolius-funereus-156-24-aug.jpg)

3. Pitch shift

![](https://i.postimg.cc/59zNsrPg/Parus-major-156-6.jpg)

![](https://i.postimg.cc/852k1dCL/Parus-major-156-6-aug.jpg)

4. Time shift

![](https://i.postimg.cc/MH9s75jQ/Parus-major-117-16.jpg)

![](https://i.postimg.cc/mZj6WL6g/Parus-major-117-16-aug.jpg)

5. Time mask

![](https://i.postimg.cc/F1tYB5c5/Parus-major-101-16.jpg)

![](https://i.postimg.cc/WpdSCGrX/Parus-major-101-16-aug.jpg)

6. Time stretch

![](https://i.postimg.cc/vm1LkMxD/Parus-major-109-22.jpg)

![](https://i.postimg.cc/bvKHjM1g/Parus-major-109-22-aug.jpg)

### Creating melspectrograms
Finally every file has been converted into melspectrogram

Example melspectrograms:

![](https://i.postimg.cc/GtZRCvb6/Aegolius-funereus-103-20.jpg)
Aegolius funereus (włochatka)

![](https://i.postimg.cc/9Fvtq0xb/Emberiza-citrinella-119-24.jpg)
Emberiza citrinella (trznadel)

![](https://i.postimg.cc/x1vHJRNj/Erithacus-rubecula-65-97-aug.jpg)
Erithacus rubecula (rudzik)

![](https://i.postimg.cc/wMB8J0jC/Parus-major-111-22.jpg)
Parus major (bogatka)

![](https://i.postimg.cc/N0GWZd15/Periparus-ater-32-6.jpg)
Periparus ater (sosnówka)

![](https://i.postimg.cc/441pxwtJ/Phylloscopus-collybita-45-17.jpg)
Phylloscopus collybita (pierwiosnek)

![](https://i.postimg.cc/HL5yDtd1/Sylvia-atricapilla-35-3.jpg)
Sylvia atricapilla (kapturka)

![](https://i.postimg.cc/6p47nh74/Turdus-merula-22-12.jpg)
 Turdus merula (kos)

![](https://i.postimg.cc/854sNKY9/Turdus-philomelos-94-19.jpg)
Turdus philomelos (śpiewak)

![](https://i.postimg.cc/1ztN4ZGP/Fringilla-coelebs-107-10.jpg)
Fringilla coelebs (zięba)

### CNN model

Model layers:

- convolution (32 5x5 filters, relu)
- batch normalization
- max pooling (2, 2)
- dropout (0.4)
<br/><br/>
- convolution (64 5x5 filters, relu)
- batch normalization
- max pooling (2, 2)
- dropout (0.2)
<br/><br/>
- convolution (128 5x5 filters, relu)
- batch normalization
- max pooling (2, 2)
- dropout (0.2)
<br/><br/>
- convolution (256 5x5 filters, relu)
- batch normalization
- max pooling (2, 2)
- dropout (0.2)
<br/><br/>
- flatten
- dense (512, relu)
- batch normalization
- dropout (0.5)
- dense (10, softmax)

![](https://i.postimg.cc/pTy2HGY0/model-1-10-classes.png)
Model accuracy and loss during training

### Evaluating model
The model scored 70% accuracy on test dataset

### LSTM model

Model layers:

- LSTM (128 units, l2 regularization)
- dropout (0.3)
<br/><br/>
- LSTM (64 units, l2 regularization)
- dropout (0.3)
<br/><br/>
- dense (64, relu, l2 regularization)
- dropout (0.3)
<br/><br/>
- dense (64, relu, l2 regularization)
- dropout (0.3)
<br/><br/>
- dense (10, softmax, l2 regularization)

Optimizer: Adam with 0.001 learning rate\
Loss function: sparse categorical crossentropy\
Callbacks: early stopping, learning rate reduction\

### Accuracy and loss plot

![](https://i.postimg.cc/qRTtHVmn/rnn-model-3-10-classes.png)

### Evaluation
55% accuracy
