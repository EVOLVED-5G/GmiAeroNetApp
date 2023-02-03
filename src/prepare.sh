jq -r .capif_hostname=\"$CAPIF_HOSTNAME\" /code/src/capif_NetApp_registration.json >> tmp.json && mv tmp.json /code/src/capif_NetApp_registration.json
jq -r .capif_port_http=\"$CAPIF_PORT_HTTP\" /code/src/capif_NetApp_registration.json >> tmp.json && mv tmp.json /code/src/capif_NetApp_registration.json
jq -r .capif_port_https=\"$CAPIF_PORT_HTTPS\" /code/src/capif_NetApp_registration.json >> tmp.json && mv tmp.json /code/src/capif_NetApp_registration.json
jq -r .capif_callback_url=\"http://$CAPIF_CALLBACK_URL\" /code/src/capif_NetApp_registration.json >> tmp.json && mv tmp.json /code/src/capif_NetApp_registration.json

evolved5g register-and-onboard-to-capif --config_file_full_path="/code/src/capif_NetApp_registration.json"

uvicorn src.main:app --host 0.0.0.0 --port 8383