# Extracting Timestamps

## Content

The project contains two scripts. As the optical character recongnition by Tesseract is not working reliable it is recommended to use the patter matching algorithm in `ocr_simple.py`.

### Files: 

```
README.md			this file

ocr_simple.py		pattern matching algorithm
config_sample.json	configuration file for ocr_simple.py
chars/				template images 

ocr_tesseract.py optical character recongnition with Tesseract
tess.conf			Tesseract configuration  file

```




## Data

There are two time stamps in all the images. In the top left the name of the station, date and time is given. 

Example:

```
Aragats 2015/06/03 15:17:18
```

In the bottom at the left side date, time and a frame number are given. 
The text is brokwn in two lines. In the analyzed sequence one image per second is stored. Every frame has a unique time.

Example:

```
2015-06-03
15:17:19-27
```

In the Mpeg file no further per frame meta data seems to be available.



## Tesseract

Tesseract does not automatically detect all the digits right. Especially a zero is always taken as a 3. It is possible to include available apriori knowledge in tesseract. The position of the characters is known, the characters can be restricted to numbers, space, colon and minus and finally the font can be given - a 6x6 segment display is used. Preprocessing should be applied in order to have only the white characters without background.


List available languages:

```
ipekopmann2:aragats kopmann$ tesseract --list-langs
List of available languages (4):
deu-frak
deu
eng
monaco
osd
```

Web service to generate trained datasets from true type fonts:
`http://trainyourtesseract.com`

It looks like using a rough font (e.g. code 5x7) for training results in worse coding. Best results are obtained with Monaco (or deu-fraktur). 

How to generate training for own fonts? Will this simple fonts work at all with tesseract? A higher resolution cant't be achived.


### Installation of PyTesseract

Homepage https://pypi.org/project/pytesseract/

PyTesseract is a wrapper to the teseract binary. The file has to be in the PATH. 

```
brew install tesseract (only Mac)

sudo pip install pytesseract
```



## Pattern matching

Alternative: Implement an single pattern matching algorithm. The position of all digits is known, so it should be not that difficult. A check can be used, as the time and the frames can only increase.

Extracted all characters. The resolution of each characters is 12 x 14 pixel, while the characters are build out of 2x2 block. So virtually the resoltion is lower. Each character has a separation to the left and top.

For each symbol the white pixel should be added. The highest value is taken as the character with the best match.

Position of the date string in the images: 

Margin right: 10 pixel
Top margin:  24 pixel, 10 character
Bottom margin: 6 pixel, 11 character 

Bounding box: 140 x 38, 10 x 6
Pixel between the rows 4 pixel

The algorithm extracts the 21 characters from the picture and correlates with alle the character templates (ten digits, colon and minus).

The highest value is selected. 






