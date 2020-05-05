<script>
	import { onMount } from "svelte";
	import * as api from "./api";
	import Event from "./Event.svelte";
	import LoginForm from "./LoginForm.svelte";

	export let name, events;


  onMount(async () => {
    await api.listEvents()
      .then(data => {
      	console.log(data)
        events = data['results'];
      });
  })

</script>

<main>
	<LoginForm on:loginSuccess={onMount}/>


	{#if events}
  {#each events as event }
    <ul>
      <li>    
        <Event {event} />
      </li>
    </ul>
  {/each}
{:else}
  <p class="loading">loading...</p>
{/if}
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
