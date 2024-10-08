package com.kundan
import grails.rest.*
import grails.converters.*
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpEntity
import org.springframework.http.ResponseEntity
import org.springframework.http.HttpMethod
import org.springframework.web.client.RestTemplate

class AuthInterceptor {

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
            String url = "https://api.github.com/user"
            HttpHeaders headers = new HttpHeaders()
            headers.set("Authorization", "token ${token}")
            HttpEntity<String> entity = new HttpEntity<>(headers)
            RestTemplate restTemplate = new RestTemplate()
            ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, entity, Map.class)

            if (response.statusCode.is2xxSuccessful()) {
                def userData = response.body
                if (userData && userData.login) {
                    session.user = userData.login
                    return true 
                }
            }
        } catch (Exception e) {
           println "Error validating token: ${e.message}"
        }
        return false  
    }

    boolean after() { true }

    void afterView() {
        // no-op
    }
}
