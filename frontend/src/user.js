import * as api from "./api";

export function isLoggedIn() {
  return localStorage.getItem('user') === '1';
}


export function setLoggedIn() {
  localStorage.setItem('user', '1');
}

export async function logout() {
  await api.logout();
  localStorage.setItem('user', '0');
}
