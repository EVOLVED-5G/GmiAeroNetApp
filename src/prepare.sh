evolved5g register-and-onboard-to-capif --config_file_full_path="/code/src/capif_NetApp_registration.json"

uvicorn src.main:app --host 0.0.0.0 --port 8383
