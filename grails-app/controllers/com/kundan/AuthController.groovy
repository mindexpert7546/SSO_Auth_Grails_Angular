package com.kundan

import grails.rest.*
import grails.converters.*
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpEntity
import org.springframework.http.ResponseEntity
import org.springframework.http.HttpMethod
import org.springframework.web.client.RestTemplate

class AuthController {
    static responseFormats = ['json', 'xml']
    
    def validateToken() {
        String token = params.token
        if (token) {
            String url = "https://api.github.com/user"
            HttpHeaders headers = new HttpHeaders()
            headers.set("Authorization", "token ${token}")
            HttpEntity<String> entity = new HttpEntity<>(headers)
            RestTemplate restTemplate = new RestTemplate()
            try {
                ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, entity, Map.class)

                if (response.statusCode.is2xxSuccessful()) {
                    def userData = response.body
                    if (userData && userData.login) {
                        session.user = userData.login 
                        render([success: true, message: "Token validated successfully", user: userData.login] as JSON)
                    } else {
                        render "Invalid token", status: 401
                    }
                } else {
                    render "Failed to validate token", status: response.statusCode.value()
                }
            } catch (Exception e) {
                render "Error validating token: ${e.message}", status: 500
            }
        } else {
            render "Token is missing", status: 400
        }
    }
}
