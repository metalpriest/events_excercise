import { writable } from 'svelte/store'
import * as user from './user'

export const loggedIn = writable(user.isLoggedIn());
export const events = writable([]);
