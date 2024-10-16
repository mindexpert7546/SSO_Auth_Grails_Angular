import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class ApiservicesService {

  constructor(private http: HttpClient, private router: Router) { }

  private apiUrl = 'http://localhost:8081/'

  getApi1(){
    return this.http.get<any>(this.apiUrl+'api1')
  }

  getApi2(){
    return this.http.get<any>(this.apiUrl+'api2')
  }

  getApi3(){
    return this.http.get<any>(this.apiUrl+'api3')
  }
}
