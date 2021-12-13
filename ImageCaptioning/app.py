from flask import Flask, render_template, url_for, request, redirect
import finalmodelcaption



# __name__ == __main__
app=Flask(__name__)
	
@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/', methods= ['POST'])
def marks():
	if request.method == 'POST':

		f = request.files['userfile']
		path = "./static/{}".format(f.filename)# ./static/example.jpg
		f.save(path) 
		caption = finalmodelcaption.yourdesc(path)
		print(caption)
		
		result_dic = {
		'example' : path,
		'caption' : caption
		}
	return render_template("index.html", your_result =result_dic)

if __name__ == '__main__':
 #app.debug = True
	# due to versions of keras we need to pass another paramter threaded = Flase to this run function
 app.run(debug = True)
 
