from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET', 'POST'])
def run_script():
    try:
        result = subprocess.run(
            ['python', 'mdrm.py'],
            check=True,
            capture_output=True,
            text=True
        )

        return jsonify({
            'status': 'MDRM update successful',
            'output': result.stdout
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            'status': 'Script failed',
            'error': e.stderr
        }), 500

    except Exception as e:
        return jsonify({
            'status': 'Unknown error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
