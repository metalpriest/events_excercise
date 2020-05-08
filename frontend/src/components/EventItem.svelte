<script>

	export let event;

	import * as api from "../api";
	import {loggedIn, events} from '../store';
	import CreateEvent from "../components/CreateEvent.svelte";

	
	async function withdraw() {
		console.log(event);

		let res = await api.withdraw(event.id);
		if (res) {
			event.has_participation = false;
			event.participants_count -= 1;
		}
	}

	async function participate() {
		console.log(event);
		let res = await api.participate(event.id);

		if (res) {
			event.has_participation = true;
			event.participants_count += 1;
		}
	}
	
</script>

<style>
	article {
		margin: 0 0 1em 0;
	}
	h1 {
		font-size: 1.4em;
		margin: 0;
		display: block;
	}
</style>

<article>
		<h1>{event.title}</h1>
		<p>{event.description}</p>

		<small>
			Owner: <b>{event.owner_name}</b>
		</small><br/>
		<small>
			Date: <b>{event.date_start}</b>
		</small><br/>
		<small>
			Participants: <b>{event.participants_count}</b>
		</small>

	  {#if loggedIn}
		{#if event.has_participation}
			<p>You will participate</p>
			<button on:click={async () => { await withdraw() }}>
				Withdraw
			</button>
		{:else}
			<button on:click={async () => { await participate() }}>
				Participate
			</button>
		{/if}
		{:else}
			<p>Log in to participate</p>
	  {/if}
		
</article>
