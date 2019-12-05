
class References:
    
    credencialesTokenAsApp = {
        "grant_type"        : "app",
        "app_id"            : "23623573",
        "app_token"         : "954ad1d7617643e6902d7806b0469202",
        "client_id"         : "mypodioapptest",
        "redirect_uri"      : "podio.com",
        "client_secret"     : "zkg7fgwXzKoM0slypsoAUV9z5w4oxsYUnypaFuWgXrncRsD0Z4IB21t2ch8G3NLp"
    }
    
    credencialesTokenAsUser = {
        "grant_type"        : "password",
        "username"          : "luis.rivero4@aiesec.net",
        "password"          : "23KSDLCXMA_yo",
        "client_id"         : "mypodioapptest",
        "redirect_uri"      : "podio.com",
        "client_secret"     : "zkg7fgwXzKoM0slypsoAUV9z5w4oxsYUnypaFuWgXrncRsD0Z4IB21t2ch8G3NLp"
    }
    
    references = {
        "podioLoginURL"     : "https://podio.com/oauth/token",
        "apiBaseUrl"        : "https://api.podio.com/",
        "testAPP_ID"        : "23623573",
        "coopAplic_ID"      : "21460631"
    }
    
    apiCalls = {
        "getApp"            : "app/{app_id}",
        "getItemCount"      : "item/app/{app_id}/count",
        "filterItems"       : "item/app/{app_id}/filter",
        "validateHook"      : "hook/{hook_id}/verify/validate"
    }