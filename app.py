from flask import Flask, render_template, request
import pickle
import numpy as np
import os 
app = Flask(__name__)


def prediction(lst):
    # This finds the absolute path to your current folder
    base_path = os.path.dirname(__file__)
    filename = os.path.join(base_path, 'model', 'predictor.pickle')
    
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model.predict([lst])


@app.route('/', methods=['POST', 'GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        
        # Fixed: Used parentheses () instead of brackets [] for the getlist method
        ips = request.form.getlist('ips') 

        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list=['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list=['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list=['linux','mac','other','windows']
        cpu_list=['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list=['amd','intel','nvidia']



        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)


        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        pred = prediction(feature_list)*372.04
        pred =np.round(pred[0])




    
        
    # Fixed: Indented 4 spaces to align properly inside the index() function
    return render_template("index.html", pred=pred)

if __name__ == '__main__':
    app.run(debug=True)

# MOVE THIS OUTSIDE: It must be at the very edge of the left margin
app = app