import shutil
import os
import tempfile
from subprocess import TimeoutExpired, Popen, PIPE
from dotenv import load_dotenv
load_dotenv()
    
def decodeResults(results):
    return (res.strip().decode('utf-8') for res in results)

def refineCode(code):
    if "```" in code: 
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python"):].strip()
    return code

def runPython(code, timeout_sec=10):
    code = refineCode(code)
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {'OPENAI_API_KEY':os.getenv('OPENAI_API_KEY')}
        python_path = shutil.which("python")
        if not python_path: # shows 'which' returns None
            python_path = sys.executable 
        process = Popen([python_path,tmp.name], env=environmental_variables,stdout=PIPE, stderr=PIPE)
        try:
            output, err = decodeResults(process.communicate(timeout=timeout_sec))
            success = len(err) == 0
        except TimeoutExpired:
            process.kill()
            success = True
            output = err = ""
        return output, err, success