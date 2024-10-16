import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
  errorMessage: string | undefined;
  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    // this.checkTokenOnLoad(); 
  }
  checkTokenOnLoad(): void {
    const token = this.authService.getToken();
    if (token) {
      this.authService.validateToken(token).subscribe(response => {
        if (response.success) {
          this.router.navigate(['/dashboard']);
        } else {
          this.authService.loginWithGitHub();
        }
      }, error => {
        this.errorMessage = 'Error validating token. Please try again.';
        console.error(error);
      });
    } else {
      // No token, prompt login with GitHub
      this.authService.loginWithGitHub();
    }
  }
}
