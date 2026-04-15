from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import sys
import traceback

app = Flask(__name__)

# Global variable to cache the model
_model = None

def prediction(lst):
    global _model
    if _model is None:
        base_path = os.path.dirname(__file__)
        filename = os.path.join(base_path, 'model', 'predictor.pickle')
        with open(filename, 'rb') as file:
            _model = pickle.load(file)
    return _model.predict([lst])


@app.route('/debug')
def debug():
    """Debug endpoint to check the environment on Vercel."""
    info = {
        "python_version": sys.version,
        "numpy_version": np.__version__,
    }
    try:
        import sklearn
        info["sklearn_version"] = sklearn.__version__
    except Exception as e:
        info["sklearn_import_error"] = str(e)

    # Check if model file exists
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'model', 'predictor.pickle')
    info["model_file_exists"] = os.path.exists(model_path)
    if os.path.exists(model_path):
        info["model_file_size_bytes"] = os.path.getsize(model_path)

    # Try loading the model
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        info["model_loaded"] = True
        info["model_type"] = str(type(model))
    except Exception as e:
        info["model_loaded"] = False
        info["model_load_error"] = str(e)
        info["model_load_traceback"] = traceback.format_exc()

    return jsonify(info)


@app.route('/', methods=['POST', 'GET'])
def index():
    pred = 0
    if request.method == 'POST':
        try:
            ram = request.form['ram']
            weight = request.form['weight']
            company = request.form['company']
            typename = request.form['typename']
            opsys = request.form['opsys']
            cpu = request.form['cpuname']
            gpu = request.form['gpuname']
            touchscreen = request.form.getlist('touchscreen')
            ips = request.form.getlist('ips')

            feature_list = []
            feature_list.append(int(ram))
            feature_list.append(float(weight))
            feature_list.append(len(touchscreen))
            feature_list.append(len(ips))

            company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
            typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
            opsys_list = ['linux', 'mac', 'other', 'windows']
            cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
            gpu_list = ['amd', 'intel', 'nvidia']

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

            pred = prediction(feature_list) * 372.04
            pred = np.round(pred[0])
        except Exception as e:
            # Log the error for debugging
            print(f"ERROR during prediction: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return f"Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>", 500

    return render_template("index.html", pred=pred)

if __name__ == '__main__':
    app.run(debug=True)

app = app