import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent {
  username: string | null = null;

  ngOnInit() {
    try {
      this.username = localStorage.getItem('username');
    } catch {
      this.username = null;
    }
  }

  logout() {
    try {
      localStorage.removeItem('username');
    } catch {}
    location.assign('/login');
  }
}

