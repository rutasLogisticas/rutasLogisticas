import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-restricted',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './restricted.html',
  styleUrls: ['./restricted.css']
})
export class RestrictedComponent {}

