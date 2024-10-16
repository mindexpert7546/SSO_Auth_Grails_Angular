package com.kundan

class UrlMappings {

    static mappings = {
        delete "/$controller/$id(.$format)?"(action:"delete")
        get "/$controller(.$format)?"(action:"index")
        get "/$controller/$id(.$format)?"(action:"show")
        post "/$controller(.$format)?"(action:"save")
        put "/$controller/$id(.$format)?"(action:"update")
        patch "/$controller/$id(.$format)?"(action:"patch")

        "/"(controller: 'application', action:'index')
        "500"(view: '/error')
        "404"(view: '/notFound')
        // "/auth/validateToken"(controller: 'auth', action: 'validateToken')
        "/dashboard"(controller: 'dashboard', action: 'index')
        "/api1"(controller: 'dashboard', action: 'api1')
        "/api2"(controller: 'dashboard', action: 'api2')
        "/api3"(controller: 'dashboard', action: 'api3')
    }
}
