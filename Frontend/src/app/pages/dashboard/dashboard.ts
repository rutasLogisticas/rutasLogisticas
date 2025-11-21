import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  username: string | null = null;
  showUserMenu = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    try {
      this.username = localStorage.getItem('username');
    } catch {
      this.username = null;
    }
  }

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  closeUserMenu() {
    this.showUserMenu = false;
  }

  logout() {
    this.authService.logout();
    location.assign('/login');
  }
}

