// package com.kundan
// import grails.rest.*
// import grails.converters.*
// import org.springframework.http.HttpHeaders
// import org.springframework.http.HttpEntity
// import org.springframework.http.ResponseEntity
// import org.springframework.http.HttpMethod
// import org.springframework.web.client.RestTemplate

// class AuthInterceptor {

//     AuthInterceptor() {
//         matchAll()  
//             .excludes(controller: 'auth', action: 'validateToken')
//     }

//     boolean before() {
//         String token = request.getHeader("Authorization")?.replace("Bearer ", "")

//         if (!token || !validateToken(token)) {
//             render status: 401, text: 'Unauthorized'
//             return false
//         }
//         return true
//     }

//     private boolean validateToken(String token) {
//         try {
//             String url = "https://api.github.com/user"
//             HttpHeaders headers = new HttpHeaders()
//             headers.set("Authorization", "token ${token}")
//             HttpEntity<String> entity = new HttpEntity<>(headers)
//             RestTemplate restTemplate = new RestTemplate()
//             ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, entity, Map.class)

//             if (response.statusCode.is2xxSuccessful()) {
//                 def userData = response.body
//                 if (userData && userData.login) {
//                     session.user = userData.login
//                     return true 
//                 }
//             }
//         } catch (Exception e) {
//            println "Error validating token: ${e.message}"
//         }
//         return false  
//     }

//     boolean after() { true }

//     void afterView() {
//         // no-op
//     }
// }

package com.kundan

import grails.rest.*
import grails.converters.*
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpEntity
import org.springframework.http.ResponseEntity
import org.springframework.http.HttpMethod
import org.springframework.web.client.RestTemplate

class AuthInterceptor {

    private static final String KEYCLOAK_HOST = "http://localhost:8080"  // Your Keycloak host URL
    private static final String REALM_NAME = "icoraltest"  // Your Keycloak realm name
    private static final String CLIENT_ID = "icoraltest-keycloak"  // Your Keycloak client ID
    private static final String CLIENT_SECRET = "Wfc0RTW7ZZXnJ6gB7FW9XtHzUO0PbqlM"  // Your Keycloak client secret
    // private static final String INTROSPECTION_URL = "${KEYCLOAK_HOST}/auth/realms/${REALM_NAME}/protocol/openid-connect/token/introspect"
    private static final String INTROSPECTION_URL = "${KEYCLOAK_HOST}/realms/${REALM_NAME}/protocol/openid-connect/token/introspect"

    AuthInterceptor() {
        matchAll()  
            .excludes(controller: 'auth', action: 'validateToken')
    }

    boolean before() {
        String token = request.getHeader("Authorization")?.replace("Bearer ", "")
        
        if (!token || !validateToken(token)) {
            render status: 401, text: 'Unauthorized'
            return false
        }
        return true
    }

    private boolean validateToken(String token) {
    try {
        HttpHeaders headers = new HttpHeaders()
        headers.set("Content-Type", "application/x-www-form-urlencoded")
        headers.set("Authorization", "Basic ${encodeCredentials(CLIENT_ID, CLIENT_SECRET)}") 

        String requestBody = "token=${token}"
        println "Request Body: ${requestBody}"
        
        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers)
        RestTemplate restTemplate = new RestTemplate()
        ResponseEntity<Map> response = restTemplate.exchange(INTROSPECTION_URL, HttpMethod.POST, entity, Map.class)

        println "Introspection Response Status: ${response.statusCode}"
        println "Introspection Response Body: ${response.body}"

        if (response.statusCode.is2xxSuccessful() && response.body?.active) {
            session.user = response.body.sub
            return true 
        }
    } catch (Exception e) {
        println "Error validating token: ${e.message}"
    }
    return false  
}


    // Method to encode client ID and secret for Basic Auth
    private String encodeCredentials(String clientId, String clientSecret) {
        return "${Base64.encoder.encodeToString("${clientId}:${clientSecret}".bytes)}"
    }

    boolean after() { true }

    void afterView() {
        // no-op
    }
}
