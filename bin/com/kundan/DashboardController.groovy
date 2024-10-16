package com.kundan

import grails.rest.*
import grails.converters.*

class DashboardController {
    static responseFormats = ['json', 'xml']

    def index() {
        render([message: "Test cron", model: [user: session.user]] as JSON)
    }

    def api1() {
        render([response: "Web Technology :  ${session.user}"] as JSON)
    }

    def api2() {
        render([response: "C Programming :  ${session.user}"] as JSON)
    }

    def api3() {
        render([response: "Courses :  ${session.user}"] as JSON)
    }

    def validateToken() {
        render([message: "Token validated successfully"] as JSON)
    }
}
