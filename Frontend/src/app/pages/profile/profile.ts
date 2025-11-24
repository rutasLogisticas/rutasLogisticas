import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserProfileService, SecurityQuestion, SecurityQuestionUpdate, ChangePasswordRequest } from '../../services/user-profile';
import { SECURITY_QUESTIONS } from '../../shared/security-questions';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css']
})
export class ProfileComponent implements OnInit, OnDestroy {
  loading = false;
  error: string | null = null;
  successMessage: string | null = null;

  // Modal states
  showChangePasswordModal = false;
  showSecurityQuestionsModal = false;

  // Change password form
  changePasswordForm: ChangePasswordRequest = {
    current_password: '',
    new_password: ''
  };
  confirmPassword = '';

  // Security questions
  securityQuestions: SecurityQuestion[] = [];
  availableQuestions = SECURITY_QUESTIONS;
  securityQuestionsForm: SecurityQuestionUpdate[] = [
    { question: '', answer: '' },
    { question: '', answer: '' }
  ];

  private subscriptions: Subscription[] = [];

  constructor(private userProfileService: UserProfileService) {}

  ngOnInit(): void {
    this.loadSecurityQuestions();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  loadSecurityQuestions(): void {
    const sub = this.userProfileService.getMySecurityQuestions().subscribe({
      next: (data) => {
        this.securityQuestions = data.questions;
        // Usar siempre las 2 preguntas fijas
        this.securityQuestionsForm = [
          { question: this.availableQuestions[0], answer: '' }, // "¿Cuál es el nombre de tu primera mascota?"
          { question: this.availableQuestions[1], answer: '' }  // "¿En qué ciudad naciste?"
        ];
      },
      error: (err) => {
        console.error('Error cargando preguntas de seguridad:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  // Modal management
  showChangePasswordForm(): void {
    this.changePasswordForm = { current_password: '', new_password: '' };
    this.confirmPassword = '';
    this.showChangePasswordModal = true;
    this.error = null;
    this.successMessage = null;
  }

  showSecurityQuestionsForm(): void {
    // Asegurar que las preguntas estén configuradas correctamente
    this.securityQuestionsForm = [
      { question: this.availableQuestions[0], answer: '' }, // "¿Cuál es el nombre de tu primera mascota?"
      { question: this.availableQuestions[1], answer: '' }  // "¿En qué ciudad naciste?"
    ];
    this.showSecurityQuestionsModal = true;
    this.error = null;
    this.successMessage = null;
  }

  closeModals(): void {
    this.showChangePasswordModal = false;
    this.showSecurityQuestionsModal = false;
    this.error = null;
    this.successMessage = null;
  }

  // Change password
  changePassword(): void {
    if (!this.changePasswordForm.current_password || !this.changePasswordForm.new_password) {
      this.error = 'Todos los campos son requeridos';
      return;
    }

    if (this.changePasswordForm.new_password !== this.confirmPassword) {
      this.error = 'Las contraseñas no coinciden';
      return;
    }

    if (this.changePasswordForm.new_password.length < 8) {
      this.error = 'La nueva contraseña debe tener al menos 8 caracteres';
      return;
    }

    this.loading = true;
    this.error = null;

    const sub = this.userProfileService.changePassword(this.changePasswordForm).subscribe({
      next: (response) => {
        this.successMessage = response.message || 'Contraseña actualizada exitosamente';
        this.loading = false;
        this.closeModals();
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error al cambiar contraseña';
        this.loading = false;
      }
    });
    this.subscriptions.push(sub);
  }

  // Update security questions
  updateSecurityQuestions(): void {
    // Filtrar preguntas vacías
    const validQuestions = this.securityQuestionsForm.filter(q => 
      q.question.trim() && q.answer.trim()
    );

    if (validQuestions.length === 0) {
      this.error = 'Debe proporcionar al menos una pregunta de seguridad';
      return;
    }

    this.loading = true;
    this.error = null;

    const sub = this.userProfileService.updateSecurityQuestions(validQuestions).subscribe({
      next: (response) => {
        this.successMessage = response.message || 'Preguntas de seguridad actualizadas exitosamente';
        this.loading = false;
        this.loadSecurityQuestions();
        this.closeModals();
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error al actualizar preguntas de seguridad';
        this.loading = false;
      }
    });
    this.subscriptions.push(sub);
  }

  // Utility methods
  clearMessages(): void {
    this.error = null;
    this.successMessage = null;
  }
}
