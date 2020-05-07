<script>

	export let event;
	
	function withdraw() {
		console.log(event);
		event.has_participation = false;
	}

	function participate() {
		console.log(event);
		event.has_participation = true;
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
		{#if event.has_participation}
			<p>You will participate</p>
			<button on:click={withdraw}>
				Withdraw
			</button>
		{:else}
			<button on:click={participate}>
				Participate
			</button>
		{/if}
		
</article>
