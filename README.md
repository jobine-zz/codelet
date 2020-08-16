># Codelet

This project is built up for generating any useful codelets in order to improve coding efficiency. Any contributions and suggestions are welcome.

# Usage

## Engineering Excellence for Application

### class AppEE(self, service=None, endpoint=None, api_key=None, export=EXPORT_CLIPBOARD)

This class contains a bunch of methods to generate useful codelets for Time Series Group Applications.

#### Parameters

    <service>
    Short name for an api service host, e.g. 'sotck-exp3'.
    
    <endpoint> 
    Full name for and api service endpoint, e.g. 'https://stock-exp3-api.azurewebsites.net'.
    
    <api_key> 
    Api key for authentication.
    
    <export>
    The location where the generated codelet put.
    
 *EXPORT_CLIPBOARD* By default, the codelet will be copied to clipboard.
 
 *EXPORT_FILE* The file export is also supported, and file is located at the current work directory.

### def sql_update_parameters(self, app_uuid):

Generate PostgreSql script for updating application's parameters.

#### Parameters

    <app_uuid> The uuid of the applicatoin to generate.
    
#### Example
    from codelet.app_ee import AppEE
    
    api_key = '<Your api key here>'
    app_uuid = '<Your application UUID here>'
    
    appEE = AppEE(service='stock-exp3', api_key=api_key)
    appEE.sql_update_parameters(app_id)

### def sql_insert_final(self, app_uuid)

Generate PostgreSql script for inserting the application.

#### Parameters

    <app_uuid> The uuid of the applicatoin to generate.

#### Example

    from codelet.app_ee import AppEE
    
    api_key = '<Your api key here>'
    app_uuid = '<Your application UUID here>'
    
    appEE = AppEE(service='stock-exp3', api_key=api_key)
    appEE.sql_insert_final(app_id)
    
### def sql_insert_all(self, only_public=True)

Generate Postgresql script for inserting all applications. 

>[!Note]
>Before running this method, the caller should have super user permission.

#### Parameters
    <only_public> The boolean value stands for export only public applications or both public and private. The default value is True.
    
#### Example

    from codelet.app_ee import AppEE
    
    api_key = '<Your api key here>'
    app_uuid = '<Your application UUID here>'
    
    appEE = AppEE(service='stock-exp3', api_key=api_key)
    appEE.sql_insert_all()
    
