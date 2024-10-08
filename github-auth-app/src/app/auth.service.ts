import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private redirectUrl = 'http://localhost:5000/login'; // Flask OAuth URL
  private apiUrl = 'http://localhost:8080/auth/validateToken'; // Grails API URL

  constructor(private http: HttpClient, private router: Router) {}

  loginWithGitHub() {
    window.location.href = this.redirectUrl;
  }

  handleCallback(token: string): void {
    this.storeToken(token); // Store token in local storage
    this.router.navigate(['/dashboard']);
  }

  storeToken(token: string): void {
    localStorage.setItem('authToken', token);
  }

  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  validateToken(token: string): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const params = { token };
    return this.http.get(`${this.apiUrl}`, { headers, params });
  }
}
