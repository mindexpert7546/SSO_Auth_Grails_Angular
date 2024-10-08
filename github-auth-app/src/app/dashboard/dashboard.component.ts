import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { ApiservicesService } from '../apiservices.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  response: any;
  api: any;

  constructor(
      private activatedRoute: ActivatedRoute,
      private router: Router,
      private authService: AuthService,
      private apiService: ApiservicesService
  ) {}


  ngOnInit(): void { 
    this.activatedRoute.queryParams.subscribe(params => {
      const token = params['token'];
      if (token) {
        console.log("token : " + token)
        localStorage.setItem('access_token', token);
        this.router.navigate([], { queryParams: {} });
      }
    });
  }

  getApi3(){
    this.apiService.getApi3().subscribe(res =>{
      this.api = res?.response;
    })
  }
  getApi2() {
    this.apiService.getApi2().subscribe(res =>{
      this.api = res?.response;
    })
  }
  getApi1() {
    this.apiService.getApi1().subscribe(res =>{
      this.api = res?.response;
    })
  }
}