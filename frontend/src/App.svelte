<script>
	import { onMount } from "svelte";
	import * as api from "./api";
	import { Router, Route } from "svelte-routing";
	import NavLink from "./components/NavLink.svelte";
	
	import EventDetail from "./routes/EventDetail.svelte";
  import EventList from "./routes/EventList.svelte";
  import LoginPage from "./routes/LoginPage.svelte";


	export let name, events;
	export let url = "";


  // onMount(async () => {
  //   await api.listEvents()
  //     .then(data => {
  //     	console.log(data)
  //       events = data['results'];
  //     });
  // })

</script>

<main>
	<h1>Main page</h1>

	<Router url="{url}">
  <nav>
    <NavLink to="login">Login</NavLink>
<!--    <NavLink to="events">Event Detail</NavLink>-->
    <NavLink to="events">Events List</NavLink>
  </nav>
  <div>
    <Route path="events" component="{EventList}" />
    <Route path="events/:id" component="{EventDetail}" />
    <Route path="login" component="{LoginPage}" />
  </div>
	</Router>
<!--	<LoginForm on:loginSuccess={onMount}/>-->

	
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
