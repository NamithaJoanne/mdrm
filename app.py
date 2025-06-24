from flask import Flask, jsonify
from mdrm_script import run_mdrm_script

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_script():
    try:
        output_dir = run_mdrm_script()
        return jsonify({
            'status': 'MDRM update successful',
            'output_dir': output_dir
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'Script failed',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
