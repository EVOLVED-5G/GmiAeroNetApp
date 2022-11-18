# @app.get('/location_create_sub/{externalId}')
# async def root(externalId: str):
#    external_id = externalId 
#    response = location_create_sub(external_id)
#    return response

# @app.get('/location_delete_sub/')
# async def root():
#     print("Location : Delete subscriptions")
#     response = location_delete_sub()
#     return response

# def showcase_service_discovery():
#     full_path="D:\\Datas\Projets\\Evolved 5G\\GMI NetApp\\config_files\\certificates\\"
#     service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=full_path,
#                                            capif_host="capifcore",
#                                            capif_https_port=443
#                                            )
#     endpoints = service_discoverer.discover_service_apis()
#     print(endpoints)