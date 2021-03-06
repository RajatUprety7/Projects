
from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageDraw, ImageFont


# extract features from each photo in the directory
def extract_features(filename):
	# load the model
	model = VGG16()
	
	# re-structure the model
	model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
	
	# load the photo
	image = load_img(filename, target_size=(224, 224))
	# convert the image pixels to a numpy array
	image = img_to_array(image)
	# reshape data for the model
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	# prepare the image for the VGG model
	image = preprocess_input(image)
	
	# get features
	feature = model.predict(image, verbose=0)
	return feature

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate a description for an image
def generate_desc( model,tokenizer, photo, max_length):
	# seed the generation process
	in_text = 'startseq'
	# iterate over the whole length of the sequence
	for i in range(max_length):
		# integer encode input sequence
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		# pad input
		sequence = pad_sequences([sequence], maxlen=max_length)
		# predict next word
		yhat = model.predict([photo,sequence], verbose=0)
		# convert probability to integer
		yhat = argmax(yhat)
		# map integer to word
		word = word_for_id(yhat, tokenizer)
		# stop if we cannot map the word
		if word is None:
			break
		# append as input for generating the next word
		in_text += ' ' + word
		# stop if we predict the end of the sequence
		if word == 'endseq':
			break
	final = in_text.split()
	final = final[1:-1]
	
	final = 'Final caption= ' + ' '.join(final)
	return final
def yourdesc(images):
	tokenizer = load(open('tokenizer.pkl', 'rb'))
	max_length = 34
	model = load_model('finalmodel.h5')
	photo = extract_features(images)
	max_length = 34
	#model = load_model('finalmodel.h5')
	description = generate_desc(model, tokenizer, photo, max_length)  
	return description



# load the tokenizer

# pre-define the max sequence length (from training)

# load and prepare the photograph
#photo = extract_features("static/example.jpg")

#font = ImageFont.truetype("arial.ttf", 20)


# generate description

#print(description)
#img=Image.open("static/example.jpg")
#d = ImageDraw.Draw(img)
#d.text((0,300), description, (0,0,0), font=font)
#img.show() 

