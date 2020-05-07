<script>
	import { onMount } from "svelte";
	import * as api from "./api";
	import * as user from "./user";
	import { Router, Route } from "svelte-routing";
	import {createEventDispatcher} from "svelte";

	import NavLink from "./components/NavLink.svelte";
  import EventList from "./routes/EventList.svelte";
  import LoginPage from "./routes/LoginPage.svelte";
  import { get } from 'svelte/store';
  import { loggedIn } from './store';


	export let name, events;
	export let url = "";

  onMount(async () => {
    let response = await api.checkSession();
		if (!response.is_authenticated && get(loggedIn) === true) {
			await logout()
		}
	})

	async function logout() {
  	await user.logout();
		loggedIn.set(false);
	}

</script>

<main>
	<h1>Main page</h1>

	<Router url="{url}">
  <nav>
		{#if $loggedIn}
			<a on:click={async () => { await logout() }}>Logout</a>
		{:else}
			<NavLink to="sign-up">Sign up</NavLink>
			<NavLink to="login">Login</NavLink>
		{/if}
    <NavLink to="events">Events List</NavLink>
  </nav>
  <div>
    <Route path="events" component="{EventList}" />
    <Route path="login" component="{LoginPage}" />
		<Route path="sign-up" let:params>
			<LoginPage isLoginPage={false}/>
		</Route>
  </div>
	</Router>

	
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
