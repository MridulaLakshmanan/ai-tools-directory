import { supabase } from './supabase.js';

const LOGIN_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes
let modalInterval = null;

function showLoginModal() {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user) return;
  const modal = document.getElementById('loginModal');
  if (!modal) return;
  modal.classList.remove('hidden');
  modal.setAttribute('aria-hidden', 'false');
}

function hideLoginModal() {
  const modal = document.getElementById('loginModal');
  if (!modal) return;
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden', 'true');
}

function wireModalButtons() {
  const loginBtn = document.getElementById('modalLoginBtn');
  const signupBtn = document.getElementById('modalSignupBtn');
  const laterBtn = document.getElementById('modalLaterBtn');
  if (loginBtn) loginBtn.onclick = () => { window.location.href = 'login.html'; };
  if (signupBtn) signupBtn.onclick = () => { window.location.href = 'signup.html'; };
  if (laterBtn) laterBtn.onclick = () => { hideLoginModal(); };
}

export function startAuthModalTimer() {
  if (!modalInterval) {
    modalInterval = setInterval(() => {
      const user = JSON.parse(localStorage.getItem('user'));
      if (!user) {
        showLoginModal();
      } else {
        clearInterval(modalInterval);
        modalInterval = null;
        hideLoginModal();
      }
    }, LOGIN_INTERVAL_MS);
  }
}

export function stopAuthModalTimer() {
  if (modalInterval) {
    clearInterval(modalInterval);
    modalInterval = null;
  }
}

wireModalButtons();
startAuthModalTimer();

window.addEventListener('storage', (e) => {
  if (e.key === 'user') {
    const val = e.newValue;
    if (val) { hideLoginModal(); stopAuthModalTimer(); }
  }
});